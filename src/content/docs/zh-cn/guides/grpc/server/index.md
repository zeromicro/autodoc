---
title: gRPC 服务端开发
description: 通过 Proto 与 goctl 构建 gRPC 服务端。
sidebar:
  order: 2

---

go-zero 在标准 gRPC 服务端之上封装了弹性治理、服务注册和链路追踪能力。

## 定义 Proto

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

## 生成代码

```bash
goctl rpc protoc greeter.proto --go_out=. --go-grpc_out=. --zrpc_out=.
```

生成的目录结构：

```text
greeter/
├── etc/greeter.yaml
├── internal/
│   ├── config/config.go
│   ├── logic/sayhellologic.go
│   ├── server/greeterserver.go
│   └── svc/servicecontext.go
├── greeter/        # protobuf 生成文件
└── greeter.go
```

## 实现业务逻辑

```go title="internal/logic/sayhellologic.go"
func (l *SayHelloLogic) SayHello(in *greeter.SayHelloReq) (*greeter.SayHelloResp, error) {
    return &greeter.SayHelloResp{Message: "Hello " + in.Name}, nil
}
```

## 配置

```yaml title="etc/greeter.yaml"
Name: greeter.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts: [127.0.0.1:2379]
  Key: greeter.rpc
```

## 运行

```bash
go run greeter.go
```
