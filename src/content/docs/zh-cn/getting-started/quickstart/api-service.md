---
title: 构建 API 服务
description: 创建一个包含登录和个人信息接口的完整用户 HTTP API 服务。
sidebar:
  order: 9
---

# 构建 API 服务

本节创建一个包含**登录**和**查询个人信息**的用户服务。

## 创建项目

```bash
mkdir user-api && cd user-api
go mod init user-api
```

## 编写 API DSL

新建 `user.api` 文件：

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
}

service user-api {
    @server (
        jwt: Auth
    )

    @handler GetUserInfo
    get /user/:id (UserInfoReq) returns (UserInfoResp)
}
```

## 生成代码

```bash
goctl api go -api user.api -dir .
go mod tidy
```

生成的目录结构：

```
user-api/
├── etc/
│   └── user-api.yaml
├── internal/
│   ├── config/
│   │   └── config.go
│   ├── handler/
│   │   ├── loginhandler.go
│   │   └── getuserinfohandler.go
│   ├── logic/
│   │   ├── loginlogic.go        ← 需要填写
│   │   └── getuserinfologic.go  ← 需要填写
│   ├── svc/
│   │   └── servicecontext.go
│   └── types/
│       └── types.go
└── user.go
```

## 实现登录逻辑

打开 `internal/logic/loginlogic.go`：

```go
func (l *LoginLogic) Login(req *types.LoginReq) (resp *types.LoginResp, err error) {
    if req.Username != "admin" || req.Password != "secret" {
        return nil, errors.New("invalid credentials")
    }
    return &types.LoginResp{
        Token: "mock-jwt-token",
    }, nil
}
```

## 运行服务

```bash
go run user.go -f etc/user-api.yaml
```

## 测试

```bash
# 登录
curl -X POST http://localhost:8888/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"secret"}'
```

## 下一步

[构建 RPC 服务 →](./rpc-service)
