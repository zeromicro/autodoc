---
title: Create an API Service
description: Build a complete HTTP API service from a custom DSL definition.
sidebar:
  order: 9
---


This guide builds a simple **user service** with login and profile endpoints. You will write a `.api` DSL file, generate the project, and fill in the business logic.

## Step 1 — Write the API DSL

Create a directory and write the DSL:

```bash
mkdir user-api && cd user-api
```

Create `user.api`:

```go
syntax = "v1"

type (
    LoginReq {
        Username string `json:"username"`
        Password string `json:"password"`
    }

    LoginResp {
        Token string `json:"token"`
    }

    UserInfoReq {
        Id int64 `path:"id"`
    }

    UserInfoResp {
        Id       int64  `json:"id"`
        Username string `json:"username"`
        Email    string `json:"email"`
    }
)

service user-api {
    @handler Login
    post /user/login (LoginReq) returns (LoginResp)

    @handler GetUserInfo
    get /user/:id (UserInfoReq) returns (UserInfoResp)
}
```

## Step 2 — Generate the Service

```bash
goctl api go -api user.api -dir .
go mod init user-api
go mod tidy
```

The generated layout:

```
user-api/
├── etc/
│   └── user-api.yaml
├── internal/
│   ├── config/config.go
│   ├── handler/
│   │   ├── loginhandler.go         # auto-generated, do not edit
│   │   ├── getuserinfohandler.go   # auto-generated, do not edit
│   │   └── routes.go
│   ├── logic/
│   │   ├── loginlogic.go           # ← implement this
│   │   └── getuserinfologic.go     # ← implement this
│   ├── svc/servicecontext.go
│   └── types/types.go             # auto-generated from DSL
└── main.go
```

## Step 3 — Implement Logic

Edit `internal/logic/loginlogic.go`:

```go
func (l *LoginLogic) Login(req *types.LoginReq) (resp *types.LoginResp, err error) {
    // In production: verify credentials against DB, issue a real JWT
    if req.Username == "admin" && req.Password == "secret" {
        return &types.LoginResp{
            Token: "mock-jwt-token-for-" + req.Username,
        }, nil
    }
    return nil, errors.New("invalid credentials")
}
```

Edit `internal/logic/getuserinfologic.go`:

```go
func (l *GetUserInfoLogic) GetUserInfo(req *types.UserInfoReq) (resp *types.UserInfoResp, err error) {
    // In production: query from DB using l.svcCtx.DB
    return &types.UserInfoResp{
        Id:       req.Id,
        Username: "alice",
        Email:    "alice@example.com",
    }, nil
}
```

## Step 4 — Run and Test

```bash
go run main.go
```

In another terminal:

```bash
# Login
curl -s -X POST http://localhost:8888/user/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"secret"}'
# {"token":"mock-jwt-token-for-admin"}

# Get user info
curl http://localhost:8888/user/1
# {"id":1,"username":"alice","email":"alice@example.com"}
```

## Regenerating After DSL Changes

Whenever you change `user.api`, regenerate without overwriting your logic files:

```bash
goctl api go -api user.api -dir .
```

goctl only overwrites files it owns (`handler/`, `types/`, `routes.go`). Your `logic/` files are preserved.

## Next Steps

- Add [JWT middleware](../../guides/http/server/middleware) to protect endpoints
- Connect a [database model](../../guides/database/mysql)
- [Create an RPC service →](./rpc-service)
