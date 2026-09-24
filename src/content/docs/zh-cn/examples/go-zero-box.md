---
title: go-zero-box 工程模板
description: 集成 API、异步队列、定时任务与 CLI 的 go-zero 工程模板。
sidebar:
  order: 6
---

go-zero-box 是社区维护的 go-zero 工程模板，适合在基础 API 示例之上学习业务分层、依赖注入和多种服务的组织方式。项目基于 go-zero v1.9.4，可将 API、队列和定时任务合并运行，也可按服务分别部署。

项目地址：[go-zero-box](https://github.com/prf16/go-zero-box)

## 能力

| 能力 | 实现方式 |
| --- | --- |
| API 服务 | 按模块拆分 API DSL，提供登录、注册和 JWT 鉴权示例 |
| 异步队列与定时任务 | 使用 asynq 处理队列任务与计划任务 |
| 命令行工具 | 使用 Cobra 注册和执行自定义命令 |
| 依赖管理 | 使用 Wire 生成依赖注入代码，通过 ServiceContext 聚合依赖 |
| 开发工具 | 通过 Makefile 组织构建、API 代码生成和依赖注入代码生成 |

## 获取代码

```bash
git clone https://github.com/prf16/go-zero-box.git
cd go-zero-box
go mod download
```

## 运行准备

Go 1.23.5 或更高版本、MySQL 5.7 或更高版本、Redis。

根据本地环境修改 `app/etc/app.yaml` 中的 `Database`、`Redis` 和 `Asynqx` 配置；使用鉴权示例前设置自己的 `JwtAuth.AccessSecret`。数据库结构参考 `deploy/sql/v1.sql`，完整初始化步骤见项目 README。

## 启动服务

在项目根目录启动 API 服务：

```bash
go run . server:api
```

默认配置下，可访问 Hello 接口和 Swagger 文档：

```bash
curl http://localhost:8001/api/hello
```

[Swagger](http://localhost:8001/api/doc)

### 其他运行方式

| 命令 | 用途 |
| --- | --- |
| `go run . server:queue` | 启动队列消费者 |
| `go run . server:scheduler` | 启动定时任务服务 |
| `go run . server:all` | 同时启动 API、队列和定时任务 |
| `go run . hello:world` | 执行示例命令 |

## RPC 扩展

RPC 服务由配套项目 [go-zero-box-rpc](https://github.com/prf16/go-zero-box-rpc) 提供。接入时需配置 `UserRpc`，并检查 `pkg/rpc/client.go` 中的客户端初始化；当前示例代码尚未启用该初始化，RPC 接口需要完成连接配置后再调用。

## 核心知识点

- 按业务模块组织 API 定义、handler、logic 和 service。
- 用 Wire 与 ServiceContext 管理依赖。
- 复用业务服务处理 HTTP 请求、队列任务和命令行任务。
