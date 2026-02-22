---
title: API DSL Syntax
description: Complete reference for the goctl API DSL used to define HTTP services.
sidebar:
  order: 6
---

# API DSL Syntax

The goctl API DSL is a concise language for describing HTTP services. A `.api` file is the single source of truth: running `goctl api go` regenerates all handlers, routes, and type definitions from it.

## File Structure

```go
syntax = "v1"         // required version declaration

info (                 // optional metadata block
    title: "User API"
    version: "1.0"
)

import "shared.api"   // import other .api files

type (...)             // type definitions

service name-api {     // service block
    @server (...)
    @handler HandlerName
    method /path (RequestType) returns (ResponseType)
}
```

## Type Definitions

Types map directly to Go structs. Use standard Go struct tags:

```go
type (
    LoginReq {
        Username string `json:"username"`
        Password string `json:"password"`
    }

    LoginResp {
        Token   string `json:"token"`
        Expires int64  `json:"expires"`
    }

    // Path parameter: /user/:id
    UserReq {
        Id int64 `path:"id"`
    }

    // Query parameter: /search?keyword=foo&page=1
    SearchReq {
        Keyword string `form:"keyword"`
        Page    int    `form:"page,default=1"`
    }
)
```

### Tag Types

| Tag | Source | Example |
|---|---|---|
| `json` | Request/response body (POST/PUT) | `json:"username"` |
| `path` | URL path parameter | `path:"id"` |
| `form` | URL query string (GET) | `form:"page,default=1"` |
| `header` | HTTP request header | `header:"Authorization"` |

### Optional Fields

Append `,optional` to make a field optional (zero value used if absent):

```go
type SearchReq {
    Keyword string `form:"keyword"`
    Page    int    `form:"page,optional"`
    Size    int    `form:"size,default=20"`
}
```

## Service Blocks

```go
service user-api {
    @server (
        jwt:         Auth             // enable JWT middleware, config key = Auth
        middleware:  AccessLog,Cors   // apply named middleware
        prefix:      /v1              // URL prefix for all routes in this block
        timeout:     3s               // per-request timeout
    )

    @handler Login
    post /user/login (LoginReq) returns (LoginResp)

    @handler GetUser
    get /user/:id (UserReq) returns (UserResp)

    @handler DeleteUser
    delete /user/:id (UserReq)        // no response body
}
```

### HTTP Methods

`get` / `post` / `put` / `patch` / `delete` / `head`

### Multiple Service Blocks

Group routes by auth requirement:

```go
service user-api {
    // Public routes
    @handler Login
    post /user/login (LoginReq) returns (LoginResp)
}

service user-api {
    @server (
        jwt: Auth
    )

    // Private routes (JWT required)
    @handler GetProfile
    get /user/profile () returns (ProfileResp)
}
```

## Imports

Split large APIs across files:

```go
// main.api
syntax = "v1"

import (
    "user.api"
    "order.api"
)
```

All imported files must use `syntax = "v1"` and must not contain a `service` block (or only one service name across all imports).

## Complete Example

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

    UserInfoReq {
        Id int64 `path:"id"`
    }

    UserInfoResp {
        Id       int64  `json:"id"`
        Username string `json:"username"`
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

Generate:

```bash
goctl api go -api user.api -dir .
```

## Next Step

[Proto DSL syntax →](./proto-syntax)
