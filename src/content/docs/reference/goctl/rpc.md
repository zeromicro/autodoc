---
title: RPC Generation
description: Reference for goctl rpc — generate gRPC service scaffolding from proto files.
sidebar:
  order: 4

---


`goctl rpc protoc` reads a standard `.proto` file and generates a complete zrpc service alongside the Go protobuf bindings.

## Prerequisites

```bash
# Install protoc
brew install protobuf

# Install Go plugins
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Verify
goctl env check --install
```

## Command

```bash
goctl rpc protoc \
  greeter.proto \
  --go_out=. \
  --go-grpc_out=. \
  --zrpc_out=. \
  -m              # generate multiple services
```

## Proto File Requirements

```protobuf
syntax = "proto3";

package greeter;
option go_package = "./greeter";  // required

message SayHelloReq  { string name    = 1; }
message SayHelloResp { string message = 1; }

service Greeter {
    rpc SayHello(SayHelloReq) returns(SayHelloResp);
}
```

## Generated Layout

```text
greeter/
├── etc/greeter.yaml        # config template
├── internal/
│   ├── config/config.go
│   ├── logic/sayhellologic.go
│   ├── server/greeterserver.go
│   └── svc/servicecontext.go
├── greeter/                # protobuf generated files
│   ├── greeter.pb.go
│   └── greeter_grpc.pb.go
└── greeter.go              # main entry point
```

## Client Configuration

```yaml
GreeterRpc:
  Etcd:
    Hosts: [etcd:2379]
    Key: greeter.rpc
  Timeout: 2000
```
