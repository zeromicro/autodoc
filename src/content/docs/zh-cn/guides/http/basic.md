---
title: HTTP 基础开发
description: 了解 go-zero HTTP 服务的基本开发流程。
sidebar:
  order: 2

---

本指南将带你使用 go-zero 的 API 框架创建一个最简 HTTP 服务。

## 定义 API

创建 `hello.api`：

```text
syntax = "v1"

type HelloReq {
    Name string `path:"name,options=you|me"`
}

type HelloReply {
    Message string `json:"message"`
}

service hello-api {
    @handler HelloHandler
    get /hello/:name (HelloReq) returns (HelloReply)
}
```

## 生成代码

```bash
goctl api go -api hello.api -dir ./hello
```

生成的目录结构：

```text
hello/
├── etc/hello-api.yaml
├── internal/
│   ├── config/config.go
│   ├── handler/hellohandler.go
│   ├── logic/hellologic.go
│   ├── svc/servicecontext.go
│   └── types/types.go
└── hello.go
```

## 实现业务逻辑

```go title="internal/logic/hellologic.go"
func (l *HelloLogic) Hello(req *types.HelloReq) (resp *types.HelloReply, err error) {
    return &types.HelloReply{
        Message: "Hello " + req.Name,
    }, nil
}
```

## 配置

```yaml title="etc/hello-api.yaml"
Name: hello-api
Host: 0.0.0.0
Port: 8888
```

## 启动服务

```bash
cd hello && go mod tidy && go run hello.go
```

## 测试

```bash
curl http://localhost:8888/hello/world
# {"message":"Hello world"}
```

## 错误处理

```go
import "github.com/zeromicro/go-zero/rest/httpx"

httpx.Error(w, errorx.NewCodeError(400, "invalid name"))
```
