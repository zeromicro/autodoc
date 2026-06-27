---
title: HTTP 게이트웨이
description: go-zero Gateway로 HTTP 요청을 HTTP 백엔드 서비스에 프록시하는 방법입니다.
sidebar:
  order: 2
---


**작성자**: Kevin Wan
**날짜**: 2025년 1월 27일

## 기능 개요

HTTP-to-HTTP gateway 기능을 사용하면 다음 작업을 수행할 수 있습니다.

- HTTP 요청을 HTTP 백엔드 서비스로 라우팅
- 백엔드 서비스별 URL path prefix 설정
- upstream별 요청 timeout 설정

## 설정

Gateway 설정에서 HTTP upstream은 다음처럼 구성합니다.

```yaml
Upstreams:
  - Name: userservice  # 선택 사항입니다. 지정하지 않으면 target을 사용합니다
    Http:
      Target: localhost:8080
      Prefix: /api/v1  # 선택 사항입니다
      Timeout: 3000    # 밀리초 단위, 기본값 3000
    Mappings:
      - Method: GET
        Path: /users
      - Method: POST
        Path: /users/create
```

비교를 위해 gRPC upstream 설정은 다음과 같습니다.

```yaml
Upstreams:
  - Name: orderservice
    Grpc:
      Target: localhost:9000
      Timeout: 3000
    ProtoSets:
      - order.pb
    Mappings:
      - Method: GET
        Path: /orders
        RpcPath: order.OrderService/GetOrders
```

## 사용 예제

HTTP-to-HTTP routing을 설정하는 전체 예제를 살펴보겠습니다.

```go
package main

import (
    "github.com/zeromicro/go-zero/gateway"
    "github.com/zeromicro/go-zero/rest"
)

func main() {
    var c gateway.GatewayConf
    conf.MustLoad("gateway.yaml", &c)

    gw := gateway.MustNewServer(c)
    defer gw.Stop()

    gw.Start()
}
```

다음 `gateway.yaml`을 사용합니다.

```yaml
Name: gateway
Host: 0.0.0.0
Port: 8888
Upstreams:
  - Name: userapi
    Http:
      Target: localhost:8080
      Prefix: /api
    Mappings:
      - Method: GET
        Path: /users
      - Method: POST
        Path: /users
      - Method: GET
        Path: /users/:id
```

## 주요 기능

1. **유연한 라우팅**
   - 같은 gateway에서 HTTP와 gRPC backend를 모두 지원
   - prefix를 지원하는 path 기반 라우팅
   - HTTP method 기반 라우팅(GET, POST, PUT, DELETE 등)

2. **설정 옵션**
   - upstream별 timeout 설정
   - path rewriting을 위한 선택적 URL prefix
   - HTTP 설정과 gRPC 설정의 명확한 분리

3. **오류 처리**
   - HTTP 상태 코드의 올바른 전파
   - 백엔드 서비스 timeout 처리

4. **헤더 관리**
   - request/response header 보존
   - content type 자동 처리

## 구현 세부 사항

구현은 관심사를 명확히 분리하며 기존 gateway 기능과 자연스럽게 통합됩니다.

- 설정에서 HTTP upstream과 gRPC upstream은 서로 배타적입니다.
- 요청 전달 시 원래 HTTP method와 header를 보존합니다.
- 응답 상태 코드와 header를 보존합니다.
- timeout 처리는 go-zero의 기존 패턴과 일관됩니다.

## 성능 고려 사항

HTTP-to-HTTP gateway는 성능을 고려해 설계되었습니다.

- 효율적인 요청 전달
- 라우팅 계층의 최소 overhead

## 모범 사례

HTTP-to-HTTP gateway 기능을 사용할 때는 다음을 권장합니다.

1. upstream마다 적절한 timeout을 설정합니다.
2. 관측 가능성을 높이기 위해 upstream에 의미 있는 이름을 붙입니다.
3. path 충돌을 피하기 위해 URL prefix 사용을 고려합니다.
4. 배포 전에 설정을 검증합니다.

## 결론

HTTP-to-HTTP 지원이 추가되면서 go-zero Gateway는 더 다양한 마이크로서비스 아키텍처에 적합해졌습니다. gRPC 서비스, HTTP 서비스 또는 둘 다를 사용하더라도 하나의 gateway로 모든 routing 요구 사항을 관리할 수 있습니다.

자세한 내용은 다음 자료를 참고하세요.

- 전체 문서: [go-zero docs](https://go-zero.dev)
- 소스 코드: [GitHub PR #4605](https://github.com/zeromicro/go-zero/pull/4605)
- 예제: [go-zero examples](https://github.com/zeromicro/zero-examples)

go-zero 커뮤니티는 이 기능을 더 개선하기 위한 피드백과 기여를 환영합니다.
