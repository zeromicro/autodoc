---
title: API 代码生成
description: goctl api 命令参考 — 从 .api 文件生成 HTTP 服务脚手架。
sidebar:
  order: 3

---

`goctl api go` 读取 `.api` 定义文件并生成完整的 go-zero HTTP 服务脚手架。

## 命令

```bash
goctl api go \
  -api service.api \
  -dir ./service \
  -style gozero
```

## .api 文件语法参考

### 顶层结构

```text
syntax = "v1"

info (
    title:   "My Service"
    author:  "Your Name"
    version: "1.0"
)

// type definitions
// service block
```

### 类型定义

```text
type CreateUserReq {
    Username string `json:"username"`
    Password string `json:"password"`
    Age      int    `json:"age,optional"`
}

type CreateUserResp {
    Id int64 `json:"id"`
}
```

### 服务块

```text
@server (
    group:      user
    middleware: Auth
    prefix:     /v1
)
service user-api {
    @doc "Create a new user"
    @handler CreateUser
    post /users (CreateUserReq) returns (CreateUserResp)

    @jwt Auth
    @handler GetUser
    get /users/:id (GetUserReq) returns (GetUserResp)
}
```

### 支持的注解

| 注解 | 说明 |
|------|------|
| `@jwt <name>` | 启用 JWT 验证 |
| `@middleware <name>` | 挂载中间件 |
| `@group <name>` | 子目录分组 |
| `@prefix <path>` | URL 路径前缀 |
| `@doc <text>` | Swagger 描述 |

## 生成的目录结构

```text
service/
├── etc/service-api.yaml    # 配置模板
├── internal/
│   ├── config/             # 配置结构体
│   ├── handler/            # HTTP handler
│   ├── logic/              # 业务逻辑桩代码
│   ├── svc/                # 服务上下文
│   └── types/              # 请求/响应类型
└── service.go              # 主入口
```
