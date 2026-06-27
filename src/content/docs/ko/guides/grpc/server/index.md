---
title: gRPC 서버
description: go-zero의 gRPC 서버에 대해 설명합니다.
sidebar:
  order: 2

---


go-zero wraps 표준 gRPC 서버 사용하여 탄력성, 서비스 registration,과 추적 built 에서.

## Define Proto

```protobuf title="greeter.proto"
syntax = "proto3";
package greeter;
option go_package = "./greeter";

message SayHelloReq  { string name    = 1; }
message SayHelloResp { string message = 1; }

service Greeter {
    rpc SayHello(SayHelloReq) returns(SayHelloResp);
}
```

## 코드 생성

```bash
goctl rpc protoc greeter.proto --go_out=. --go-grpc_out=. --zrpc_out=.
```

생성된 구조:

```text
greeter/
├── etc/greeter.yaml
├── internal/
│   ├── config/config.go
│   ├── logic/sayhellologic.go
│   ├── server/greeterserver.go
│   └── svc/servicecontext.go
├── greeter/        # protobuf generated
└── greeter.go
```

## 로직 구현

```go title="internal/logic/sayhellologic.go"
func (l *SayHelloLogic) SayHello(in *greeter.SayHelloReq) (*greeter.SayHelloResp, error) {
    return &greeter.SayHelloResp{Message: "Hello " + in.Name}, nil
}
```

## 설정

```yaml title="etc/greeter.yaml"
Name: greeter.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts: [127.0.0.1:2379]
  Key: greeter.rpc
```

## 실행

```bash
go run greeter.go
```
