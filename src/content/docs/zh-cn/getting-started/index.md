---
title: 入门指南
description: go-zero 学习路径全览，从安装到运行第一个微服务。
sidebar:
  order: 1
---

# 入门指南

欢迎使用 **go-zero**——一个内置弹性设计的 Go 微服务框架，让你更快、更轻松地构建可靠的服务。

## 60 秒快速体验

```bash
# 1. 安装 goctl（代码生成工具）
go install github.com/zeromicro/go-zero/tools/goctl@latest

# 2. 脚手架生成一个 API 服务
goctl api new greet

# 3. 拉取依赖并运行
cd greet && go mod tidy && go run greet.go -f etc/greet-api.yaml
```

在浏览器中打开 `http://localhost:8888/from/world`，即可看到响应。

## 学习路径

| 阶段 | 内容 | 预计时间 |
|---|---|---|
| 环境准备 | 安装 Go、goctl、protoc 和 IDE | 约 15 分钟 |
| 快速上手 | Hello World、API 服务、RPC 服务 | 约 30 分钟 |
| 深入理解 | API/Proto DSL 语法 | 约 20 分钟 |

## 前置条件

| 工具 | 最低版本 | 用途 |
|---|---|---|
| Go | 1.19+ | 编译运行服务 |
| goctl | 最新版 | 代码生成 |
| protoc | 3.x | gRPC 服务 |

## goctl 生成的结构

```
greet/
├── etc/
│   └── greet-api.yaml     # 运行时配置（端口、超时等）
├── internal/
│   ├── config/            # 配置结构体
│   ├── handler/           # HTTP 处理器（路由绑定）
│   ├── logic/             # 业务逻辑（你需要填写的地方）
│   ├── svc/               # 服务上下文（依赖注入）
│   └── types/             # 请求/响应结构体
├── greet.go               # 程序入口
└── greet.api              # API DSL 定义文件
```

每次修改 `.api` 文件后重新运行 `goctl api go`，`internal/logic/` 不会被覆盖。

## 下一步

[安装 Go →](./installation/golang)
