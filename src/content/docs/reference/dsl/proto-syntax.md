---
title: Proto Syntax for go-zero
description: Common protobuf syntax and go-zero conventions for RPC services.
sidebar:
  order: 7
---


go-zero uses standard **protobuf 3** syntax for RPC services. This page covers the patterns goctl expects and good conventions to follow.

## Minimal Example

```proto
syntax = "proto3";

package user;
option go_package = "./user";

service User {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}

message GetUserRequest {
    int64 id = 1;
}

message GetUserResponse {
    int64  id   = 1;
    string name = 2;
}

message CreateUserRequest {
    string name  = 1;
    string email = 2;
}

message CreateUserResponse {
    int64 id = 1;
}
```

## go_package Convention

goctl requires `option go_package` to be set. The value is the relative output path for generated Go files:

```proto
option go_package = "./user";   // generates to ./user directory
```

## Scalar Types

| Proto type | Go type |
|---|---|
| `string` | `string` |
| `int32` | `int32` |
| `int64` | `int64` |
| `bool` | `bool` |
| `float` | `float32` |
| `double` | `float64` |
| `bytes` | `[]byte` |

## Repeated Fields (slices)

```proto
message ListUsersResponse {
    repeated UserInfo users = 1;
    int64 total = 2;
}

message UserInfo {
    int64  id   = 1;
    string name = 2;
}
```

## Nested Messages

```proto
message CreateOrderRequest {
    int64   user_id = 1;
    Address address = 2;
}

message Address {
    string street = 1;
    string city   = 2;
    string zip    = 3;
}
```

## Enums

```proto
enum UserStatus {
    ACTIVE   = 0;
    INACTIVE = 1;
    BANNED   = 2;
}

message UserInfo {
    int64      id     = 1;
    string     name   = 2;
    UserStatus status = 3;
}
```

## Multiple Services

goctl generates a separate zRPC service for each `service` block. Keep one service per `.proto` file.

## Generating Go Code

```bash
# Using goctl (recommended — handles plugin flags automatically)
goctl rpc protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user \
    --zrpc_out=.

# Or call protoc directly
protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user
```

## Naming Conventions

| What | Convention | Example |
|---|---|---|
| Service name | PascalCase | `UserService` |
| RPC method | PascalCase | `GetUserById` |
| Message name | PascalCase | `GetUserRequest` |
| Field name | snake_case | `user_id` |
| Package name | lowercase | `package user` |

Following these conventions ensures correct Go identifier generation.

## Next Step

[Run Hello World →](../../guides/quickstart/hello-world)
