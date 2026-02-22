---
title: REST API with JWT
description: A go-zero HTTP service protected with JWT authentication.
sidebar:
  order: 3
---

# REST API with JWT

This example demonstrates building a secure REST API with JWT-based authentication using go-zero.

## API Definition

```text
type LoginReq {
    Username string `json:"username"`
    Password string `json:"password"`
}

type LoginResp {
    Token string `json:"token"`
}

type UserInfoReq {}
type UserInfoResp {
    Id   int64  `json:"id"`
    Name string `json:"name"`
}

service user-api {
    @handler Login
    post /user/login (LoginReq) returns (LoginResp)

    @jwt Auth
    @handler UserInfo
    get /user/info (UserInfoReq) returns (UserInfoResp)
}
```

## Generate Code

```bash
goctl api go -api user.api -dir .
```

## Implement Login Logic

```go title="internal/logic/loginlogic.go"
func (l *LoginLogic) Login(req *types.LoginReq) (resp *types.LoginResp, err error) {
    // 1. Validate credentials
    // 2. Generate JWT token
    token, err := generateToken(l.svcCtx.Config.Auth.Secret, req.Username)
    if err != nil {
        return nil, err
    }
    return &types.LoginResp{Token: token}, nil
}
```

## Configuration

```yaml title="etc/user-api.yaml"
Name: user-api
Host: 0.0.0.0
Port: 8888
Auth:
  AccessSecret: your-secret-key
  AccessExpire: 86400
```
