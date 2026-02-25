---
title: RPC 代码生成
description: goctl rpc 命令参考 — 从 proto 文件生成 gRPC 服务脚手架。
sidebar:
  order: 4

---

`goctl rpc protoc` 读取标准 `.proto` 文件，生成完整的 zrpc 服务以及 Go protobuf 绑定。

## 前置条件

```bash
# 安装 protoc
brew install protobuf

# 安装 Go 插件
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# 验证
goctl env check --install
```

## 命令

```bash
goctl rpc protoc \
  greeter.proto \
  --go_out=. \
  --go-grpc_out=. \
  --zrpc_out=. \
  -m              # 生成多服务
```

## Proto 文件要求

```protobuf
syntax = "proto3";

package greeter;
option go_package = "./greeter";  // 必需

message SayHelloReq  { string name    = 1; }
message SayHelloResp { string message = 1; }

service Greeter {
    rpc SayHello(SayHelloReq) returns(SayHelloResp);
}
```

## 生成的目录结构

```text
greeter/
├── etc/greeter.yaml        # 配置模板
├── internal/
│   ├── config/config.go
│   ├── logic/sayhellologic.go
│   ├── server/greeterserver.go
│   └── svc/servicecontext.go
├── greeter/                # protobuf 生成文件
│   ├── greeter.pb.go
│   └── greeter_grpc.pb.go
└── greeter.go              # 主入口
```

## 客户端配置

```yaml
GreeterRpc:
  Etcd:
    Hosts: [etcd:2379]
    Key: greeter.rpc
  Timeout: 2000
```
