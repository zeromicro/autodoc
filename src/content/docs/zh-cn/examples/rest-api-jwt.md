---
title: REST API + JWT 鉴权
description: 使用 go-zero 构建基于 JWT 认证的 HTTP 服务。
sidebar:
  order: 3
---

# REST API + JWT 鉴权

本示例演示如何使用 go-zero 构建带 JWT 认证的安全 REST API。

## API 定义

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

## 生成代码

```bash
goctl api go -api user.api -dir .
```

## 实现登录逻辑

```go title="internal/logic/loginlogic.go"
func (l *LoginLogic) Login(req *types.LoginReq) (resp *types.LoginResp, err error) {
    // 1. 验证用户名密码
    // 2. 生成 JWT Token
    token, err := generateToken(l.svcCtx.Config.Auth.Secret, req.Username)
    if err != nil {
        return nil, err
    }
    return &types.LoginResp{Token: token}, nil
}
```

## 配置文件

```yaml title="etc/user-api.yaml"
Name: user-api
Host: 0.0.0.0
Port: 8888
Auth:
  AccessSecret: your-secret-key
  AccessExpire: 86400
```
