---
title: 프로젝트 구조
description: go-zero의 프로젝트 구조에 대해 설명합니다.
sidebar:
  order: 6

---


goctl은 모든 프로젝트에 일관된 디렉터리 구조를 생성합니다. 이 구조를 이해하는 것이 어떤 go-zero 코드베이스에서도 빠르게 생산성을 내는 가장 좋은 방법입니다.

## API 서비스

`goctl api go -api user.api -dir .`로 생성됩니다.

```text
user-api/
├── etc/
│   └── user-api.yaml        # 런타임, DB, RPC 설정
├── internal/
│   ├── config/
│   │   └── config.go        # YAML 설정 타입
│   ├── handler/
│   │   ├── routes.go        # 자동 생성 코드
│   │   └── loginhandler.go  # 엔드포인트별 파일
│   ├── logic/
│   │   └── loginlogic.go    # 비즈니스 로직
│   ├── svc/
│   │   └── servicecontext.go # 공유 DB/RPC 의존성
│   └── types/
│       └── types.go         # 자동 생성 코드
└── user-api.go              # 서버 진입점
```

## RPC 서비스

`goctl rpc protoc user.proto --zrpc_out=.`로 생성됩니다.

```text
user-rpc/
├── etc/
│   └── user-rpc.yaml        # ListenOn, Etcd, DB 설정
├── internal/
│   ├── config/
│   │   └── config.go
│   ├── logic/
│   │   └── getuserlogic.go  # One, RPC 예시입니다
│   ├── server/
│   │   └── userserver.go    # 예시입니다
│   └── svc/
│       └── servicecontext.go
├── pb/
│   └── user/                # protoc-generated .pb.go and _grpc.pb.go
├── userclient/
│   └── user.go              # 예시입니다
└── user.go                  # 서버 진입점
```

## 계층별 책임

| 계층 | 패키지 | 책임 | 비즈니스 로직 포함 여부 |
|---|---|---|---|
| Handler | `internal/handler` | HTTP 요청 파싱과 검증, 로직 호출, 응답 작성 | 아니요 |
| Logic | `internal/logic` | 유스케이스 구현, DB/cache/RPC 호출 조율 | **예** |
| ServiceContext | `internal/svc` | 시작 시 공유 의존성을 한 번 생성하고 보관 | 아니요 |
| Config | `internal/config` | YAML 필드를 타입이 있는 Go 구조체에 매핑 | 아니요 |
| Model | `internal/model` | 데이터 접근 계층(`goctl model`로 생성) | 아니요 |

## 다중 서비스 프로젝트 구조

여러 서비스를 포함하는 저장소에서는 보통 다음 구조를 사용합니다.

```text
project-root/
├── service/
│   ├── user/
│   │   ├── api/             # user-api
│   │   └── rpc/             # user-rpc
│   ├── order/
│   │   ├── api/
│   │   └── rpc/
│   └── payment/
│       └── rpc/
├── common/                  # 공유 패키지
└── deploy/
    ├── docker-compose.yaml
    └── k8s/
```

## 권장 사례

- **얇은 핸들러** — 핸들러는 요청을 디코딩하고 하나의 로직 메서드를 호출한 뒤 응답을 인코딩하는 일만 해야 합니다.
- **유스케이스당 하나의 로직 파일** — `CreateOrderLogic`, `GetOrderLogic`, `CancelOrderLogic`은 메서드가 작더라도 별도 파일로 둡니다.
- **ServiceContext는 유일한 생성자** — `svc.NewServiceContext` 밖에서 `sql.Open`이나 `redis.NewClient`를 직접 호출하지 않습니다.
- **코드보다 설정** — 타임아웃, 기능 플래그, 다운스트림 주소처럼 조정 가능한 값은 하드코딩하지 말고 `etc/*.yaml`에 둡니다.
- **모델 계층은 생성 코드, 로직 계층은 사용자 코드** — 모델은 자유롭게 재생성할 수 있습니다. 비즈니스 코드는 goctl이 덮어쓰지 않는 로직 계층에 둡니다.
