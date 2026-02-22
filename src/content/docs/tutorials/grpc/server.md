---
title: gRPC Server
description: Build a gRPC server with go-zero using protobuf and goctl.
sidebar:
  order: 1
---

# gRPC Server

go-zero wraps the standard gRPC server with resilience, service registration, and tracing built in.

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

## Generate Code

```bash
goctl rpc protoc greeter.proto --go_out=. --go-grpc_out=. --zrpc_out=.
```

Generated layout:

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

## Implement Logic

```go title="internal/logic/sayhellologic.go"
func (l *SayHelloLogic) SayHello(in *greeter.SayHelloReq) (*greeter.SayHelloResp, error) {
    return &greeter.SayHelloResp{Message: "Hello " + in.Name}, nil
}
```

## Configuration

```yaml title="etc/greeter.yaml"
Name: greeter.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts: [127.0.0.1:2379]
  Key: greeter.rpc
```

## Run

```bash
go run greeter.go
```
