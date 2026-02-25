---
title: 构建 RPC 服务
description: 使用 goctl 和 protobuf 构建完整的 gRPC 服务。
sidebar:
  order: 10
---

# 构建 RPC 服务

本节创建一个**用户 gRPC 服务**，并展示如何在另一个服务中调用它。

## 环境准备

确保已安装 protoc 和相关插件，参考 [安装 protoc](../../getting-started/installation/protoc)。

## 创建项目

```bash
mkdir user-rpc && cd user-rpc
go mod init user-rpc
```

## 编写 Proto 文件

新建 `user.proto`：

```proto
syntax = "proto3";

package user;
option go_package = "./pb";

service User {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}

message GetUserRequest {
    int64 id = 1;
}

message GetUserResponse {
    int64  id       = 1;
    string username = 2;
    string email    = 3;
}

message CreateUserRequest {
    string username = 1;
    string email    = 2;
}

message CreateUserResponse {
    int64 id = 1;
}
```

## 生成代码

```bash
goctl rpc protoc user.proto \
    --go_out=./pb \
    --go-grpc_out=./pb \
    --zrpc_out=.
go mod tidy
```

## 实现业务逻辑

打开 `internal/logic/getuserlogic.go`：

```go
func (l *GetUserLogic) GetUser(in *pb.GetUserRequest) (*pb.GetUserResponse, error) {
    return &pb.GetUserResponse{
        Id:       in.Id,
        Username: "admin",
        Email:    "admin@example.com",
    }, nil
}
```

## 运行服务

```bash
go run user.go -f etc/user.yaml
```

## 下一步

[API DSL 语法参考 →](../../reference/dsl/api-syntax)
