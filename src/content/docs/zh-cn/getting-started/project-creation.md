---
title: 项目创建方式
description: 使用 goctl 脚手架和创建 go-zero 项目的所有方式。
sidebar:
  order: 4

---

# 项目创建方式

goctl 根据你的起点提供多种创建项目的方式。

## 从零开始（交互式脚手架）

最快的全新服务启动方式：

```bash
# HTTP API 服务
goctl api new myservice
cd myservice && go mod tidy

# gRPC 服务
goctl rpc new myservice
cd myservice && go mod tidy
```

## 从已有 DSL 文件生成

当你已有 `.api` 或 `.proto` 文件（例如团队共享的）：

```bash
# 从 .api 文件
mkdir myservice && cd myservice
go mod init myservice
goctl api go -api myservice.api -dir .
go mod tidy

# 从 .proto 文件
mkdir myservice && cd myservice
go mod init myservice
goctl rpc protoc myservice.proto \
    --go_out=./pb \
    --go-grpc_out=./pb \
    --zrpc_out=.
go mod tidy
```

## 重新生成已有项目

修改 `.api` 或 `.proto` 文件后，重新生成而不覆盖业务逻辑：

```bash
# API：重新生成，保留 internal/logic/
goctl api go -api myservice.api -dir .

# RPC：重新生成，保留 internal/logic/
goctl rpc protoc myservice.proto \
    --go_out=./pb \
    --go-grpc_out=./pb \
    --zrpc_out=.
```

goctl 永远不会写入 `internal/logic/`，其他所有文件（处理器、路由、类型、配置结构体）都会被重新生成。

## 使用自定义模板

对于需要统一规范（日志配置、错误码、CI 配置）的团队，goctl 支持自定义模板：

```bash
# 初始化默认模板目录
goctl template init
# 模板保存到：~/.goctl/

# 编辑模板，例如 logic 文件模板
vim ~/.goctl/api/logic.tpl

# 生成时自动使用模板
goctl api go -api myservice.api -dir .
```

## 生成周边文件

```bash
# Dockerfile
goctl docker -go main.go

# Kubernetes 部署清单
goctl kube deploy \
    -name myservice \
    -namespace prod \
    -image myregistry/myservice:v1.0.0 \
    -o deployment.yaml

# 从 SQL DDL 生成数据库模型
goctl model mysql ddl \
    -src schema.sql \
    -dir internal/model
```

## 总结

| 方式 | 适用场景 |
|---|---|
| `goctl api new` / `rpc new` | 全新服务，从零开始 |
| `goctl api go` / `rpc protoc` | 已有 DSL 文件 |
| 重新生成 | 修改 `.api` 或 `.proto` 后 |
| 自定义模板 | 统一团队级约定 |
| `goctl docker` / `kube` | 生成部署文件 |
