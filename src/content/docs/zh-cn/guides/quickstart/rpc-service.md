---
title: 构建 RPC 服务
description: 使用 go-zero 构建 gRPC 服务并将其连接到 API 网关。
sidebar:
  order: 10
---

本指南创建一个**用户 RPC 服务**，API 网关可通过 gRPC 调用它。

## 前置条件

- 已安装 `protoc`
- 已安装 `protoc-gen-go` 和 `protoc-gen-go-grpc`

未安装？参见[安装 protoc](../../../getting-started/installation/protoc)。

## 第一步：创建项目

```bash
goctl rpc new user
cd user
go mod tidy
```

goctl 会创建 `.proto` 文件和完整的服务骨架：

```
user/
├── etc/
│   └── user.yaml
├── internal/
│   ├── config/config.go
│   ├── logic/
│   │   └── getuserlogic.go      # ← 在这里实现
│   ├── server/userserver.go   # gRPC 服务端适配器
│   └── svc/servicecontext.go
├── user/
│   └── user.pb.go             # 生成的 protobuf 类型
│   └── user_grpc.pb.go        # 生成的 gRPC 桩代码
├── user.go                  # 主入口
└── user.proto               # 源定义
```

## 第二步：查看生成的 Proto

打开 `user.proto`：

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

## 第三步：实现业务逻辑

编辑 `internal/logic/getuserlogic.go`：

```go
func (l *GetUserLogic) GetUser(in *user.GetUserRequest) (*user.GetUserResponse, error) {
    // 生产环境：通过 l.svcCtx 查询数据库
    return &user.GetUserResponse{
        Id:   in.Id,
        Name: "alice",
    }, nil
}
```

## 第四步：配置并运行

打开 `etc/user.yaml` — 默认端口为 `8080`：

```yaml
Name: user.rpc
ListenOn: 0.0.0.0:8080
```

运行 RPC 服务：

```bash
go run user.go
# Starting rpc server at 0.0.0.0:8080...
```

## 第五步：从 API 服务中调用

生成 API 网关使用的 RPC 客户端桩代码：

```bash
goctl rpc protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user \
    --zrpc_out=./client
```

在 API 服务的 `servicecontext.go` 中：

```go
UserRpc userclient.User  // 注入生成的客户端
```

然后在 logic 文件中调用：

```go
resp, err := l.svcCtx.UserRpc.GetUser(l.ctx, &user.GetUserRequest{Id: 1})
```

go-zero 自动处理连接池、负载均衡和熔断。

## Proto 变更后重新生成

```bash
goctl rpc protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user \
    --zrpc_out=.
```

## 下一步

- [使用 etcd 进行服务发现](../microservice/service-discovery)
- [熔断器配置](../../../components/resilience/circuit-breaker)
- [项目创建模式](../../../getting-started/project-creation)
