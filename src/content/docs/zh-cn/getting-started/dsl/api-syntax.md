---
title: API DSL 语法
description: goctl API DSL 完整参考，用于定义 HTTP 服务。
sidebar:
  order: 6
---

# API DSL 语法

goctl API DSL 是一种用于描述 HTTP 服务的简洁语言，`.api` 文件是唯一的事实来源。

## 文件结构

```go
syntax = "v1"         // 必须的版本声明

info (                // 可选元数据块
    title: "用户 API"
    version: "1.0"
)

import "shared.api"   // 导入其他 .api 文件

type (...)             // 类型定义

service name-api {     // 服务块
    @server (...)
    @handler HandlerName
    method /path (RequestType) returns (ResponseType)
}
```

## 类型定义

类型直接映射为 Go 结构体，使用标准的 Go 结构体标签：

```go
type (
    LoginReq {
        Username string `json:"username"`
        Password string `json:"password"`
    }

    // 路径参数：/user/:id
    UserReq {
        Id int64 `path:"id"`
    }

    // 查询参数：/search?keyword=foo&page=1
    SearchReq {
        Keyword string `form:"keyword"`
        Page    int    `form:"page,default=1"`
    }
)
```

### 标签类型

| 标签 | 来源 | 示例 |
|---|---|---|
| `json` | 请求/响应体（POST/PUT） | `json:"username"` |
| `path` | URL 路径参数 | `path:"id"` |
| `form` | URL 查询字符串（GET） | `form:"page,default=1"` |
| `header` | HTTP 请求头 | `header:"Authorization"` |

### 可选字段

追加 `,optional` 将字段设为可选（缺失时使用零值）：

```go
type SearchReq {
    Keyword string `form:"keyword"`
    Page    int    `form:"page,optional"`
    Size    int    `form:"size,default=20"`
}
```

## 服务块

```go
service user-api {
    @server (
        jwt:         Auth             // 启用 JWT 中间件
        middleware:  AccessLog,Cors   // 应用命名中间件
        prefix:      /v1              // URL 前缀
        timeout:     3s               // 超时时间
    )

    @handler Login
    post /user/login (LoginReq) returns (LoginResp)

    @handler GetUser
    get /user/:id (UserReq) returns (UserResp)
}
```

### HTTP 方法

`get` / `post` / `put` / `patch` / `delete` / `head`

## 完整示例

```go
syntax = "v1"

type (
    RegisterReq {
        Username string `json:"username"`
        Password string `json:"password"`
        Email    string `json:"email"`
    }

    RegisterResp {
        Id int64 `json:"id"`
    }
)

service user-api {
    @handler Register
    post /user/register (RegisterReq) returns (RegisterResp)
}

service user-api {
    @server (
        jwt:    Auth
        prefix: /api/v1
    )

    @handler GetUserInfo
    get /user/:id (UserInfoReq) returns (UserInfoResp)
}
```

生成代码：

```bash
goctl api go -api user.api -dir .
```

## 下一步

[Proto DSL 语法 →](./proto-syntax)
