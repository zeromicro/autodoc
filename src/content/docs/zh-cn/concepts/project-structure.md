---
title: 项目结构
description: 标准 go-zero 项目目录及职责说明。
sidebar:
  order: 6

---

# 项目结构

goctl 为每个项目生成一致的目录结构，熟悉它是快速上手任何 go-zero 代码库的最佳途径。

## API 服务

由 `goctl api go -api user.api -dir .` 生成：

```text
user-api/
├── etc/
│   └── user-api.yaml        # 运行时配置（host、port、DB、RPC 地址）
├── internal/
│   ├── config/
│   │   └── config.go        # 映射 YAML 的强类型结构体
│   ├── handler/
│   │   ├── routes.go        # 自动生成的路由注册
│   │   └── loginhandler.go  # 每个 @handler 一个文件——绑定请求、调用 logic
│   ├── logic/
│   │   └── loginlogic.go    # 业务逻辑——通常只需修改此处
│   ├── svc/
│   │   └── servicecontext.go # 共享依赖：DB、RPC 客户端、Redis 等
│   └── types/
│       └── types.go         # 自动生成的请求/响应结构体
└── user-api.go              # main()——启动 rest.Server
```

## RPC 服务

由 `goctl rpc protoc user.proto --zrpc_out=.` 生成：

```text
user-rpc/
├── etc/
│   └── user-rpc.yaml        # ListenOn、Etcd 注册、DB 配置
├── internal/
│   ├── config/
│   │   └── config.go
│   ├── logic/
│   │   └── getuserlogic.go  # 每个 RPC 方法一个文件
│   ├── server/
│   │   └── userserver.go    # gRPC Server 实现——委托给 logic 层
│   └── svc/
│       └── servicecontext.go
├── pb/
│   └── user/                # protoc 生成的 .pb.go 与 _grpc.pb.go
├── userclient/
│   └── user.go              # go-zero 生成的类型安全客户端封装
└── user.go                  # main()——启动 zrpc.Server
```

## 各层职责

| 层 | 包 | 职责 | 是否包含业务逻辑 |
|---|---|---|---|
| Handler | `internal/handler` | 解析并校验 HTTP 请求，调用 logic，写响应 | 否 |
| Logic | `internal/logic` | 实现业务用例，编排 DB/缓存/RPC 调用 | **是** |
| ServiceContext | `internal/svc` | 启动时初始化并持有共享依赖 | 否 |
| Config | `internal/config` | 将 YAML 字段映射为强类型 Go 结构体 | 否 |
| Model | `internal/model` | 数据访问层（由 `goctl model` 生成） | 否 |

## 多服务项目布局

对于包含多个服务的仓库，推荐如下约定：

```text
project-root/
├── service/
│   ├── user/
│   │   ├── api/             # user-api
│   │   └── rpc/             # user-rpc
│   ├── order/
│   │   ├── api/
│   │   └── rpc/
│   └── payment/
│       └── rpc/
├── common/                  # 公共工具（错误码、中间件等）
└── deploy/
    ├── docker-compose.yaml
    └── k8s/
```

## 推荐实践

- **Handler 保持精简** — handler 只做请求解码、调用 logic、编码响应，不堆业务代码。
- **每个用例一个 logic 文件** — `CreateOrderLogic`、`GetOrderLogic`、`CancelOrderLogic` 各自独立，即使方法很小。
- **ServiceContext 是唯一的构造入口** — 不要在 `svc.NewServiceContext` 之外调用 `sql.Open` 或 `redis.NewClient`。
- **配置优于硬编码** — 超时时间、功能开关、下游地址等所有可调参数都放入 `etc/*.yaml`。
- **Model 层自动生成，Logic 层归你所有** — 可以随时重新生成 model；logic 层是你的业务代码所在地，goctl 永远不会覆盖它。
