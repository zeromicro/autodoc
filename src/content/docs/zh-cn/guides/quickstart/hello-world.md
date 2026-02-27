---
title: Hello World
description: 用五步创建并运行第一个 go-zero HTTP API 服务。
sidebar:
  order: 8
---

本页将带你从零开始创建、运行和测试第一个 go-zero HTTP 服务，整个过程大约 5 分钟。

## 前置条件

- 已安装 Go 1.21+（`go version`）
- 已安装 goctl（`goctl --version`）

未安装？参见[安装 Go](../../../getting-started/installation/golang) 和[安装 goctl](../../../getting-started/installation/goctl)。

## 第一步：生成服务脚手架

```bash
goctl api new greet
cd greet
go mod tidy
```

生成的项目结构：

```
greet/
├── etc/
│   └── greet-api.yaml        # 配置：端口、日志等
├── internal/
│   ├── config/
│   │   └── config.go          # 配置结构体
│   ├── handler/
│   │   ├── greethandler.go    # HTTP handler（自动生成）
│   │   └── routes.go          # 路由注册
│   ├── logic/
│   │   └── greetlogic.go      # ← 编辑这里：你的业务逻辑
│   └── svc/
│       └── servicecontext.go  # 共享依赖（DB、缓存等）
└── greet.go                   # 主入口
```

## 第二步：查看 API DSL 文件

打开 `greet.api`：

```go
type Request {
    Name string `path:"name,options=you|me"`
}

type Response {
    Message string `json:"message"`
}

service greet-api {
    @handler Greet
    get /from/:name (Request) returns (Response)
}
```

这个文件是唯一的源定义。`goctl` 从它生成了所有 Go 代码。

## 第三步：运行服务

```bash
go run greet.go
```

预期输出：

```
Starting server at 0.0.0.0:8888...
```

## 第四步：测试

打开新终端：

```bash
curl http://localhost:8888/from/you
```

预期响应：

```json
{"message":"Hello you"}
```

## 第五步：添加业务逻辑

打开 `internal/logic/greetlogic.go`，你会看到：

```go
func (l *GreetLogic) Greet(req *types.Request) (resp *types.Response, err error) {
    // todo: add your logic here and delete this line
    return
}
```

替换为：

```go
func (l *GreetLogic) Greet(req *types.Request) (resp *types.Response, err error) {
    return &types.Response{
        Message: fmt.Sprintf("Hello %s, welcome to go-zero!", req.Name),
    }, nil
}
```

如果需要，在文件顶部添加 `fmt` 的 import。保存并重新运行：

```bash
go run greet.go
```

```bash
curl http://localhost:8888/from/alice
# {"message":"Hello alice, welcome to go-zero!"}
```

## 请求流转过程

```
curl /from/alice
  → routes.go         （路由匹配）
  → greethandler.go   （解析 + 校验请求）
  → greetlogic.go     （你的业务逻辑）
  → greethandler.go   （序列化响应）
  → {"message":"..."}
```

你只需编写逻辑代码。go-zero 自动处理路由、解析、校验、序列化和错误包装。

## 下一步

- [构建完整 API 服务 →](../api-service)
- [构建 RPC 服务 →](../rpc-service)
