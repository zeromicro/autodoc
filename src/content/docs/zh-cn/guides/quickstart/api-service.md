---
title: 构建 API 服务
description: 从自定义 DSL 定义创建一个完整的 HTTP API 服务。
sidebar:
  order: 9
---

本指南构建一个包含登录和用户信息接口的简单**用户服务**。你将编写 `.api` DSL 文件，生成项目，然后填充业务逻辑。

## 第一步：编写 API DSL

创建目录并编写 DSL：

```bash
mkdir user-api && cd user-api
```

创建 `user.api`：

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

## 第二步：生成服务

```bash
goctl api go -api user.api -dir .
go mod init user-api
go mod tidy
```

生成的目录结构：

```
user-api/
├── etc/
│   └── user-api.yaml
├── internal/
│   ├── config/config.go
│   ├── handler/
│   │   ├── loginhandler.go         # 自动生成，不要编辑
│   │   ├── getuserinfohandler.go   # 自动生成，不要编辑
│   │   └── routes.go
│   ├── logic/
│   │   ├── loginlogic.go           # ← 在这里实现
│   │   └── getuserinfologic.go     # ← 在这里实现
│   ├── svc/servicecontext.go
│   └── types/types.go             # 从 DSL 自动生成
└── user.go
```

## 第三步：实现逻辑

编辑 `internal/logic/loginlogic.go`：

```go
func (l *LoginLogic) Login(req *types.LoginReq) (resp *types.LoginResp, err error) {
    // 生产环境：对照数据库验证凭据，签发真实 JWT
    if req.Username == "admin" && req.Password == "secret" {
        return &types.LoginResp{
            Token: "mock-jwt-token-for-" + req.Username,
        }, nil
    }
    return nil, errors.New("invalid credentials")
}
```

编辑 `internal/logic/getuserinfologic.go`：

```go
func (l *GetUserInfoLogic) GetUserInfo(req *types.UserInfoReq) (resp *types.UserInfoResp, err error) {
    // 生产环境：通过 l.svcCtx.DB 从数据库查询
    return &types.UserInfoResp{
        Id:       req.Id,
        Username: "alice",
        Email:    "alice@example.com",
    }, nil
}
```

## 第四步：运行和测试

```bash
go run user.go
```

在另一个终端中：

```bash
# 登录
curl -s -X POST http://localhost:8888/user/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"secret"}'
# {"token":"mock-jwt-token-for-admin"}

# 查询用户信息
curl http://localhost:8888/user/1
# {"id":1,"username":"alice","email":"alice@example.com"}
```

## DSL 变更后重新生成

每次修改 `user.api` 后，重新生成但不会覆盖你的逻辑文件：

```bash
goctl api go -api user.api -dir .
```

goctl 只会覆盖它管理的文件（`handler/`、`types/`、`routes.go`）。你的 `logic/` 文件会被保留。

## 下一步

- 添加 [JWT 中间件](../http/server/middleware) 保护接口
- 连接[数据库模型](../database/mysql)
- [构建 RPC 服务 →](./rpc-service)
