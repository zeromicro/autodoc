---
title: gRPC 서버 예제
description: go-zero의 gRPC 서버 예제에 대해 설명합니다.
sidebar:
  order: 3

---

## 개요

go-zero 제공합니다 gRPC 서버 that 제공합니다：

1. 서비스 디스커버리 capability (etcd 로서 registration centre)
2. 부하 Balancer(p2c algorithms)
3. Node Affinity
4. Multi-node direct 연결 mode
5. 타임아웃 processing
6. Traffic limiting, breaking
7. 인증 capacity
8. Exception Capture

## 예제


:::tip Tips
Quickly 생성과 시작 goctl gRPC 서비스 예제 — see [빠른 시작 Microservice](../../../reference/cli-guide/quickstart.md).
:::

We're here 로 생성 전체 gRPC 서비스 사용하여 proto.

### 1. 생성 서비스 디렉터리과 initialize go 모듈 프로젝트

```shell
$ mkdir demo && cd demo
$ go mod init demo
```

### 2. Quickly 생성 proto 파일

```protobuf
$ goctl rpc -o greet.proto
```

### 3. Proto 생성 gRPC 서비스

```shell
$ goctl rpc protoc greet.proto --go_out=.  --go-grpc_out=.  --zrpc_out=.
```

:::tip Tips

1. 위한 goctl 설치, see [Goctl 설치](../../../getting-started/installation/goctl.md).
1. 위한 rpc 코드 생성 명령, see [goctl rpc](../../../reference/cli-guide/rpc.md).
1. 위한 proto-related 질문, see [Proto Code Generating FAQ](../../../reference/proto-dsl/faq.md).
:::

### 4. 구조

```text
demo
├── etc
│   └── greet.yaml
├── go.mod
├── greet
│   ├── greet.pb.go
│   └── greet_grpc.pb.go
├── greet.go
├── greet.proto
├── greetclient
│   └── greet.go
└── internal
    ├── config
    │   └── config.go
    ├── logic
    │   └── pinglogic.go
    ├── server
    │   └── greetserver.go
    └── svc
        └── servicecontext.go

8 directories, 11 files

```

:::tip hint
위한 서비스 디렉터리 structure, see [프로젝트 Structure](../../../concepts/project-structure.md).
:::

### 5. Discovery/direct 서비스 mode


:::tip hint
위한 gRPC 서비스 설정, see [gRPC 서비스 설정](./configuration.md).

:::

**etcd Service Registration**
로 사용 [etcd](https://github.com/zeromicro/zero-contrib/tree/main/zrpc/registry) 로서 레지스트리, simply 추가 etcd 설정 로 static 설정 파일:

```yaml title=demo/etc/greet.yaml {3-6}
Name: greet.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts:
  - 127.0.0.1:2379
  Key: greet.rpc
```

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

```shell
$ etcdctl get --prefix greet.rpc
greet.rpc/7587870460981677828
192.168.72.53:8080
```


**Direct 연결 Mode**

```yaml title=demo/etc/greet.yaml {3-6}
Name: greet.rpc
ListenOn: 0.0.0.0:8080
```

### Stubi implementation


```go title=demo/internal/server/greetserver.go
// 이 코드는 직접 수정하지 마세요
// 소스: greet.proto

package server

import (
    "context"

    "demo/greet"
    "demo/internal/logic"
    "demo/internal/svc"
)

type GreetServer struct {
    svcCtx *svc.ServiceContext
    greet.UnimplementedGreetServer
}

func NewGreetServer(svcCtx *svc.ServiceContext) *GreetServer {
    return &GreetServer{
        svcCtx: svcCtx,
    }
}

func (s *GreetServer) Ping(ctx context.Context, in *greet.Request) (*greet.Response, error) {
    l := logic.NewPingLogic(ctx, s.svcCtx)
    return l.Ping(in)
}

```

### Writing business code


```go title=demo/internal/logic/pinglogic.go {28}
package logic

import (
    "context"

    "demo/greet"
    "demo/internal/svc"

    "github.com/zeromicro/go-zero/core/logx"
)

type PingLogic struct {
    ctx    context.Context
    svcCtx *svc.ServiceContext
    logx.Logger
}

func NewPingLogic(ctx context.Context, svcCtx *svc.ServiceContext) *PingLogic {
    return &PingLogic{
        ctx:    ctx,
        svcCtx: svcCtx,
        Logger: logx.WithContext(ctx),
    }
}

func (l *PingLogic) Ping(in *greet.Request) (*greet.Response, error) {
    return &greet.Response{
        Pong: "pong",
    }, nil
}

```

### 8. 활성화 gRPC debug switch


**demo/greet.go**
```go {13-15}
package main
...
func main() {
    flag.Parse()

    var c config.Config
    conf.MustLoad(*configFile, &c)
    ctx := svc.NewServiceContext(c)

    s := zrpc.MustNewServer(c.RpcServerConf, func(grpcServer *grpc.Server) {
        greet.RegisterGreetServer(grpcServer, server.NewGreetServer(ctx))

        if c.Mode == service.DevMode || c.Mode == service.TestMode {
            reflection.Register(grpcServer)
        }
    })
    ...
}

```

**demo/etc/greet.yaml**
```yaml {3}
Name: greet.rpc
ListenOn: 0.0.0.0:8080
Mode: dev
Etcd:
  Hosts:
  - 127.0.0.1:2379
  Key: greet.rpc

```

### 9. 미들웨어 Usage

#### Built 미들웨어


- StreamAuthorizeInterceptor|UnaryAuthorizeInterceptor
- StreamBreakerInterceptor|UnaryBreakerInterceptor
- UnaryPrometheusInterceptor
- StreamRecoverInterceptor|UnaryRecoverInterceptor
- UnarySheddingInterceptor
- UnaryStatInterceptor
- UnaryTimeoutInterceptor
- StreamTraceInterceptor|UnaryTraceInterceptor


#### Custom 미들웨어

```go {21-22,28-35}
package main
...
var configFile = flag.String("f", "etc/greet.yaml", "the config file")

func main() {
    flag.Parse()

    var c config.Config
    conf.MustLoad(*configFile, &c)
    ctx := svc.NewServiceContext(c)

    s := zrpc.MustNewServer(c.RpcServerConf, func(grpcServer *grpc.Server) {
        greet.RegisterGreetServer(grpcServer, server.NewGreetServer(ctx))

        if c.Mode == service.DevMode || c.Mode == service.TestMode {
            reflection.Register(grpcServer)
        }
    })
    defer s.Stop()

    s.AddUnaryInterceptors(exampleUnaryInterceptor)
    s.AddStreamInterceptors(exampleStreamInterceptor)

    fmt.Printf("Starting rpc server at %s...\n", c.ListenOn)
    s.Start()
}

func exampleUnaryInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (resp interface{}, err error) {
    // TODO: 여기에 로직을 작성하세요
    return handler(ctx, req)
}
func exampleStreamInterceptor(srv interface{}, ss grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
    // TODO: 여기에 로직을 작성하세요
    return handler(srv, ss)
}
```

### 10. Metadata transfer

참고: [gRPC Metadata](https://etcd.io/) 위한 참조.
