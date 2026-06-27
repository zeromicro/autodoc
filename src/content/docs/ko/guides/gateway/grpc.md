---
title: gRPC 게이트웨이
description: go-zero Gateway로 HTTP 요청을 gRPC 서비스에 매핑하는 방법입니다.
sidebar:
  order: 3
---

## 개요

go-zero Gateway는 HTTP 요청을 gRPC 호출로 변환해 RESTful 인터페이스처럼 노출할 수 있게 합니다. 기존 gRPC 서비스를 외부 HTTP client에 공개하거나, API gateway 계층에서 여러 gRPC 서비스를 통합할 때 사용할 수 있습니다.

## go-zero gRPC Gateway 동작 방식

1. proto 파일에서 gRPC 서비스 정의를 읽습니다.
2. 설정 파일에서 HTTP-to-gRPC mapping rule을 읽습니다.
3. 각 gRPC 메서드에 대응하는 HTTP handler를 생성합니다.
4. HTTP 서버를 시작하고 들어오는 요청을 받습니다.
5. 각 HTTP 요청을 gRPC 요청으로 변환합니다.
6. gRPC 응답을 HTTP 응답으로 변환합니다.
7. HTTP 응답을 호출자에게 반환합니다.

전체 gateway source는 [go-zero/gateway](https://github.com/zeromicro/go-zero/tree/master/gateway)를 참고하세요.

## 설정 소개

```go
type (
    GatewayConf struct {
        rest.RestConf
        Upstreams []Upstream
        Timeout   time.Duration `json:",default=5s"`
    }

    RouteMapping struct {
        Method string
        Path string
        RpcPath string
    }

    Upstream struct {
        Name string `json:",optional"`
        Grpc zrpc.RpcClientConf
        ProtoSets []string `json:",optional"`
        Mappings []RouteMapping `json:",optional"`
    }
)
```

### GatewayConf

| <img width={100} /> 이름 | 설명 | 타입 | 필수 여부 | 예시 |
| ---------------------------------------- | -------------------------- | ---------- | --------- | ---------------------------------- |
| RestConf | REST 서비스 설정 | RestConf | 예 | [기본 서비스 설정](../../reference/configuration/service-config) 참고 |
| Upstreams | gRPC 서비스 설정 | []Upstream | 예 | |
| Timeout | timeout 시간 | duration | 아니요 | `5s` |

### Upstream

| <img width={100} /> 이름 | 설명 | 타입 | 필수 여부 | 예시 |
| ---------------------------------------- | ---------------------------------------------------- | -------------- | --------- | ---------------------------------- |
| Name | 서비스 이름 | string | 아니요 | `demo1-gateway` |
| Grpc | gRPC 서비스 설정 | RpcClientConf | 예 | [RPC 설정](../grpc/server/configuration) 참고 |
| ProtoSets | proto descriptor 파일 목록 | []string | 아니요 | `["hello.pb"]` |
| Mappings | 라우트 mapping입니다. 비워 두면 기본 gRPC 경로를 사용합니다. | []RouteMapping | 아니요 | |

### RouteMapping

| <img width={100} /> 이름 | 설명 | 타입 | 필수 여부 | 예시 |
| ---------------------------------------- | ------------ | -------- | --------- | ------------------ |
| Method | HTTP 메서드 | string | 예 | `get` |
| Path | HTTP 경로 | string | 예 | `/ping` |
| RpcPath | gRPC 경로 | string | 예 | `hello.Hello/Ping` |

## 예제

go-zero에서 gRPC gateway를 사용하는 방법은 두 가지입니다. 하나는 proto descriptor를 사용하는 방식이고, 다른 하나는 gRPC reflection을 사용하는 방식입니다.

### proto descriptor 방식

proto descriptor 방식은 `protoc`으로 생성한 descriptor 파일(`.pb`)을 gateway 설정에 지정합니다.

:::tip
reflection을 켜기 어려운 운영 환경이나, gateway가 proto 정보를 파일로만 받아야 하는 경우에 적합합니다.
:::

1. `demo1` 프로젝트를 만들고 `demo1` 디렉터리에 `hello.proto` 파일을 작성합니다.

```protobuf
syntax = "proto3";

package hello;

option go_package = "./hello";

message Request {
}

message Response {
  string msg = 1;
}

service Hello {
  rpc Ping(Request) returns(Response);
}
```

2. `demo1` 디렉터리 아래에 `gateway` 디렉터리를 만들고, `demo1` 디렉터리에서 다음 명령으로 proto descriptor를 생성합니다.

```bash
$ protoc --descriptor_set_out=gateway/hello.pb hello.proto
```

3. `demo1` 디렉터리에서 다음 명령으로 gRPC 서비스 코드를 생성합니다.

```bash
$ goctl rpc protoc hello.proto --go_out=server --go-grpc_out=server --zrpc_out=server
```

`demo1/server/internal/logic/pinglogic.go`의 `Ping` 메서드 로직을 채웁니다.

```go
func (l *PingLogic) Ping(in *hello.Request) (*hello.Response, error) {
    return &hello.Response{
        Msg: "pong",
    }, nil
}
```

4. `demo1/server/etc/hello.yaml` 설정 파일을 다음처럼 수정합니다.

```yaml
Name: hello.rpc
ListenOn: 0.0.0.0:8080
```

5. `demo1/gateway` 디렉터리로 이동해 `etc` 디렉터리를 만들고 `gateway.yaml` 설정 파일을 추가합니다.

```yaml
Name: demo1-gateway
Host: localhost
Port: 8888
Upstreams:
  - Grpc:
      Target: localhost:8080
    # proto descriptor 파일입니다
    ProtoSets:
      - hello.pb
    # HTTP 경로와 gRPC 메서드 매핑입니다
    Mappings:
      - Method: get
        Path: /ping
        RpcPath: hello.Hello/Ping
```

6. `demo1/gateway` 디렉터리에 `gateway.go` 파일을 만들고 다음 내용을 작성합니다.

```go
package main

import (
    "flag"

    "github.com/zeromicro/go-zero/core/conf"
    "github.com/zeromicro/go-zero/gateway"
)

var configFile = flag.String("f", "etc/gateway.yaml", "config file")

func main() {
    flag.Parse()

    var c gateway.GatewayConf
    conf.MustLoad(*configFile, &c)
    gw := gateway.MustNewServer(c)
    defer gw.Stop()
    gw.Start()
}
```

RPC 서버를 실행합니다.

```bash
$ go run hello.go
Starting rpc server at 0.0.0.0:8080...
```

Gateway를 실행합니다.

```bash
$ go run gateway.go
```

HTTP 요청으로 확인합니다.

```bash
$ curl http://localhost:8888/ping
{"msg":"pong"}%
```

### gRPC reflection 방식

1. `demo2` 프로젝트를 만들고 `demo2` 디렉터리에 `hello.proto` 파일을 작성합니다.

```protobuf
syntax = "proto3";

package hello;

option go_package = "./hello";

message Request {
}

message Response {
  string msg = 1;
}

service Hello {
  rpc Ping(Request) returns(Response);
}
```

2. `demo2` 디렉터리 아래에 `gateway` 디렉터리를 만듭니다.

3. `demo2` 디렉터리에서 다음 명령으로 gRPC 서비스 코드를 생성합니다.

```bash
$ goctl rpc protoc hello.proto --go_out=server --go-grpc_out=server --zrpc_out=server
```

`demo2/server/internal/logic/pinglogic.go`의 `Ping` 메서드 로직을 채웁니다.

```go
func (l *PingLogic) Ping(in *hello.Request) (*hello.Response, error) {
    return &hello.Response{
        Msg: "pong",
    }, nil
}
```

`demo2/server/etc/hello.yaml` 설정 파일을 다음처럼 수정합니다.

```yaml {3}
Name: hello.rpc
ListenOn: 0.0.0.0:8080
Mode: dev
```

:::tip
reflection 방식은 gRPC reflection이 활성화되어 있어야 합니다. 위 예제에서는 `Mode: dev`로 reflection을 켭니다.
:::

4. `demo2/gateway` 디렉터리로 이동해 `etc` 디렉터리를 만들고 `gateway.yaml` 설정 파일을 추가합니다.

```yaml
Name: demo1-gateway
Host: localhost
Port: 8888
Upstreams:
  - Grpc:
      Target: localhost:8080
    # HTTP 경로와 gRPC 메서드 매핑입니다
    Mappings:
      - Method: get
        Path: /ping
        RpcPath: hello.Hello/Ping
```

5. `demo2/gateway` 디렉터리에 `gateway.go` 파일을 만들고 다음 내용을 작성합니다.

```go
package main

import (
    "flag"

    "github.com/zeromicro/go-zero/core/conf"
    "github.com/zeromicro/go-zero/gateway"
)

var configFile = flag.String("f", "etc/gateway.yaml", "config file")

func main() {
    flag.Parse()

    var c gateway.GatewayConf
    conf.MustLoad(*configFile, &c)
    gw := gateway.MustNewServer(c)
    defer gw.Stop()
    gw.Start()
}
```

RPC 서버를 실행합니다.

```bash
$ go run hello.go
Starting rpc server at 0.0.0.0:8080...
```

Gateway를 실행합니다.

```bash
$ go run gateway.go
```

HTTP 요청으로 확인합니다.

```bash
$ curl http://localhost:8888/ping
{"msg":"pong"}%
```

## `WithDialer`로 사용자 정의 gRPC 클라이언트 사용하기(v1.10.0부터)

```go
package main

import (
    "flag"

    "github.com/zeromicro/go-zero/core/conf"
    "github.com/zeromicro/go-zero/gateway"
    "github.com/zeromicro/go-zero/zrpc"
    "google.golang.org/grpc"
)

var configFile = flag.String("f", "etc/gateway.yaml", "config file")

func main() {
    flag.Parse()

    var c gateway.GatewayConf
    conf.MustLoad(*configFile, &c)

    gw := gateway.MustNewServer(c,
        gateway.WithDialer(func(conf zrpc.RpcClientConf) zrpc.Client {
            return zrpc.MustNewClient(conf,
                zrpc.WithDialOption(grpc.MaxCallRecvMsgSize(50*1024*1024)),
                zrpc.WithDialOption(grpc.MaxCallSendMsgSize(50*1024*1024)),
            )
        }),
    )
    defer gw.Stop()
    gw.Start()
}
```

| 사용 사례 | Dial 옵션 |
|----------|------------|
| 수신 메시지 크기 늘리기 | `grpc.MaxCallRecvMsgSize(n)` |
| 송신 메시지 크기 늘리기 | `grpc.MaxCallSendMsgSize(n)` |
| 사용자 정의 TLS | `grpc.WithTransportCredentials(creds)` |
| Keep-alive | `grpc.WithKeepaliveParams(params)` |

## 참조

- [go-zero • gateway](https://github.com/zeromicro/go-zero/tree/master/gateway)
- [기본 서비스 설정](../../reference/configuration/service-config)
- [gRPC 서버 설정](../grpc/server/configuration)
