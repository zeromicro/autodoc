---
title: go-zero 的 Proto 语法
description: 用于 RPC 服务的 protobuf 语法与 go-zero 约定。
sidebar:
  order: 7
---

# go-zero 的 Proto 语法

go-zero 使用标准的 **protobuf 3** 语法来定义 RPC 服务。

## 最简示例

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

## go_package 约定

goctl 要求设置 `option go_package`，其值为生成的 Go 文件的相对输出路径：

```proto
option go_package = "./user";   // 生成到 ./user 目录
```

## 标量类型

| Proto 类型 | Go 类型 |
|---|---|
| `string` | `string` |
| `int32` | `int32` |
| `int64` | `int64` |
| `bool` | `bool` |
| `float` | `float32` |
| `double` | `float64` |
| `bytes` | `[]byte` |

## 重复字段（切片）

```proto
message ListUsersResponse {
    repeated UserInfo users = 1;
    int64 total = 2;
}
```

## 枚举

```proto
enum UserStatus {
    ACTIVE   = 0;
    INACTIVE = 1;
    BANNED   = 2;
}
```

## 生成 Go 代码

```bash
goctl rpc protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user \
    --zrpc_out=.
```

## 命名规范

| 内容 | 规范 | 示例 |
|---|---|---|
| 服务名 | PascalCase | `UserService` |
| RPC 方法 | PascalCase | `GetUserById` |
| 消息名 | PascalCase | `GetUserRequest` |
| 字段名 | snake_case | `user_id` |
| 包名 | 小写 | `package user` |

## 下一步

[Hello World →](../quickstart/hello-world)
