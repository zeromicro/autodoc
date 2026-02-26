---
title: Create an RPC Service
description: Build a gRPC service with go-zero and connect it to an API gateway.
sidebar:
  order: 10
---


This guide creates a **user RPC service** that an API gateway can call over gRPC.

## Prerequisites

- `protoc` installed
- `protoc-gen-go` and `protoc-gen-go-grpc` installed

Not installed? See [Install protoc](../../../getting-started/installation/protoc).

## Step 1 — Scaffold the Service

```bash
goctl rpc new user
cd user
go mod tidy
```

Goctl creates a `.proto` file and the full service skeleton:

```
user/
├── etc/
│   └── user.yaml
├── internal/
│   ├── config/config.go
│   ├── logic/
│   │   └── getuserlogic.go      # ← implement this
│   ├── server/userserver.go   # gRPC server adapter
│   └── svc/servicecontext.go
├── user/
│   └── user.pb.go             # generated protobuf types
│   └── user_grpc.pb.go        # generated gRPC stubs
├── user.go                  # entrypoint
└── user.proto               # source of truth
```

## Step 2 — The Generated Proto

Open `user.proto`:

```proto
syntax = "proto3";

package user;
option go_package = "./user";

service User {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
}

message GetUserRequest {
    int64 id = 1;
}

message GetUserResponse {
    int64 id = 1;
    string name = 2;
}
```

## Step 3 — Implement Business Logic

Edit `internal/logic/getuserlogic.go`:

```go
func (l *GetUserLogic) GetUser(in *user.GetUserRequest) (*user.GetUserResponse, error) {
    // In production: query your DB via l.svcCtx
    return &user.GetUserResponse{
        Id:   in.Id,
        Name: "alice",
    }, nil
}
```

## Step 4 — Configure and Run

Open `etc/user.yaml` — the default port is `8080`:

```yaml
Name: user.rpc
ListenOn: 0.0.0.0:8080
```

Run the RPC server:

```bash
go run user.go
# Starting rpc server at 0.0.0.0:8080...
```

## Step 5 — Call It from an API Service

Generate the RPC client stub that your API gateway will use:

```bash
goctl rpc protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user \
    --zrpc_out=./client
```

In your API service's `servicecontext.go`:

```go
UserRpc userclient.User  // inject the generated client
```

Then call it from a logic file:

```go
resp, err := l.svcCtx.UserRpc.GetUser(l.ctx, &user.GetUserRequest{Id: 1})
```

go-zero handles connection pooling, load balancing, and circuit breaking automatically.

## Regenerating After Proto Changes

```bash
goctl rpc protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user \
    --zrpc_out=.
```

## Next Steps

- [Service discovery with etcd](../microservice/service-discovery)
- [Circuit breaker configuration](../../../components/resilience/circuit-breaker)
- [Project creation patterns](../../../getting-started/project-creation)
