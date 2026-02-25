---
title: Hello World
description: 用五步创建并运行第一个 go-zero HTTP API 服务。
sidebar:
  order: 8
---

# Hello World

五步构建并运行你的第一个 go-zero HTTP 服务。

## 第一步：生成服务脚手架

```bash
goctl api new greet
cd greet
```

## 第二步：查看 API DSL 文件

```bash
cat greet.api
```

```go
syntax = "v1"

type Request {
    Name string `path:"name,options=you|me"`
}

type Response {
    Message string `json:"message"`
}

service greet-api {
    @handler Greethandler
    get /from/:name (Request) returns (Response)
}
```

## 第三步：拉取依赖并运行

```bash
go mod tidy
go run greet.go -f etc/greet-api.yaml
```

```
Starting server at 0.0.0.0:8888...
```

## 第四步：测试

```bash
curl http://localhost:8888/from/world
# 输出：{"message":""}
```

## 第五步：添加业务逻辑

打开 `internal/logic/greetlogic.go`，填写 `Greet` 函数：

```go
func (l *GreetLogic) Greet(req *types.Request) (resp *types.Response, err error) {
    return &types.Response{
        Message: "Hello, " + req.Name + "!",
    }, nil
}
```

重启服务并重新测试：

```bash
curl http://localhost:8888/from/world
# 输出：{"message":"Hello, world!"}
```

## 请求流转过程

```
HTTP GET /from/world
  → main.go（注册路由）
  → handler/greethandler.go（解析请求 → types.Request）
  → logic/greetlogic.go  ← 你的业务代码
  → 返回 types.Response（序列化为 JSON）
```

## 下一步

[构建完整 API 服务 →](./api-service)
