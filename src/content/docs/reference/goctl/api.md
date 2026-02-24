---
title: API Generation
description: Reference for goctl api — generate HTTP service scaffolding from .api files.
sidebar:
  order: 3

---

# API Generation

`goctl api go` reads a `.api` definition file and generates a complete go-zero HTTP service scaffold.

## Command

```bash
goctl api go \
  -api service.api \
  -dir ./service \
  -style gozero
```

## .api File Syntax Reference

### Top-Level Structure

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

### Types

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

### Service

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

### Supported Annotations

| Annotation | Description |
|-----------|-------------|
| `@jwt <name>` | Enable JWT validation |
| `@middleware <name>` | Attach middleware |
| `@group <name>` | Sub-directory grouping |
| `@prefix <path>` | URL path prefix |
| `@doc <text>` | Swagger description |

## Generated Layout

```text
service/
├── etc/service-api.yaml    # config template
├── internal/
│   ├── config/             # config struct
│   ├── handler/            # HTTP handlers
│   ├── logic/              # business logic stubs
│   ├── middleware/         # middleware stubs
│   ├── svc/                # service context
│   └── types/              # request/response types
└── service.go              # main entry point
```
