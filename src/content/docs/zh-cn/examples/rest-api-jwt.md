---
title: REST API + JWT 鉴权
description: 使用 go-zero 构建基于 JWT 认证的 HTTP 服务。
sidebar:
  order: 3

---

# REST API + JWT 鉴权

本示例演示如何使用 go-zero 构建带 JWT 认证的安全 REST API，包含 MySQL 用户存储和 Refresh Token 机制。

## 项目结构

```bash
goctl api go -api user.api -dir .
```

```
user-api/
├── user.api
├── etc/user-api.yaml
├── user.go
└── internal/
    ├── handler/
    ├── logic/
    │   ├── loginlogic.go
    │   ├── refreshtokenlogic.go
    │   └── userinfologic.go
    ├── model/
    ├── svc/
    └── types/
```

## API 定义

```text title="user.api"
type (
    LoginReq {
        Username string `json:"username"`
        Password string `json:"password"`
    }
    LoginResp {
        AccessToken  string `json:"accessToken"`
        RefreshToken string `json:"refreshToken"`
        ExpiresIn    int64  `json:"expiresIn"`
    }
    RefreshReq {
        RefreshToken string `json:"refreshToken"`
    }
    UserInfoResp {
        Id       int64  `json:"id"`
        Username string `json:"username"`
        Role     string `json:"role"`
    }
)

service user-api {
    @handler Login
    post /user/login (LoginReq) returns (LoginResp)

    @handler RefreshToken
    post /user/refresh (RefreshReq) returns (LoginResp)

    @jwt Auth
    @handler UserInfo
    get /user/info returns (UserInfoResp)
}
```

## 配置文件

```yaml title="etc/user-api.yaml"
Name: user-api
Host: 0.0.0.0
Port: 8888

Auth:
  AccessSecret: "change-me-to-random-256-bit-value"
  AccessExpire: 86400

RefreshSecret: "another-different-random-secret"
RefreshExpire: 604800

DataSource: "root:password@tcp(127.0.0.1:3306)/userdb?parseTime=true"
CacheRedis:
  - Host: 127.0.0.1:6379
    Type: node
```

## 登录逻辑

```go title="internal/logic/loginlogic.go"
func (l *LoginLogic) Login(req *types.LoginReq) (*types.LoginResp, error) {
    user, err := l.svcCtx.UserModel.FindOneByUsername(l.ctx, req.Username)
    if errors.Is(err, model.ErrNotFound) {
        return nil, errorx.NewCodeError(401, "用户名或密码错误")
    }
    if !checkPasswordHash(req.Password, user.Password) {
        return nil, errorx.NewCodeError(401, "用户名或密码错误")
    }

    now := time.Now()
    accessToken, _ := jwtx.GenerateToken(
        l.svcCtx.Config.Auth.AccessSecret,
        now.Unix(),
        l.svcCtx.Config.Auth.AccessExpire,
        map[string]any{"userId": user.Id, "role": user.Role},
    )
    refreshToken, _ := jwtx.GenerateToken(
        l.svcCtx.Config.RefreshSecret,
        now.Unix(),
        l.svcCtx.Config.RefreshExpire,
        map[string]any{"userId": user.Id},
    )
    return &types.LoginResp{
        AccessToken:  accessToken,
        RefreshToken: refreshToken,
        ExpiresIn:    l.svcCtx.Config.Auth.AccessExpire,
    }, nil
}
```

## 获取用户信息（受保护）

```go title="internal/logic/userinfologic.go"
func (l *UserInfoLogic) UserInfo() (*types.UserInfoResp, error) {
    // go-zero JWT 中间件将 Claims 存入上下文
    userId, _ := l.ctx.Value("userId").(json.Number).Int64()
    role, _ := l.ctx.Value("role").(string)

    user, err := l.svcCtx.UserModel.FindOne(l.ctx, userId)
    if err != nil {
        return nil, err
    }
    return &types.UserInfoResp{
        Id:       user.Id,
        Username: user.Username,
        Role:     role,
    }, nil
}
```

## 完整测试流程

```bash
# 1. 启动服务
go run user.go -f etc/user-api.yaml

# 2. 登录
RESP=$(curl -s -X POST http://localhost:8888/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}')
ACCESS=$(echo $RESP | jq -r .accessToken)
REFRESH=$(echo $RESP | jq -r .refreshToken)

# 3. 访问受保护接口
curl -H "Authorization: Bearer $ACCESS" \
  http://localhost:8888/user/info
# {"id":1,"username":"alice","role":"user"}

# 4. 刷新 Token
NEW=$(curl -s -X POST http://localhost:8888/user/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\":\"$REFRESH\"}")
echo $NEW | jq .accessToken
```

## 本示例涉及的知识点

| 主题 | 位置 |
|------|------|
| `@jwt` DSL 注解 | `user.api` |
| JWT 生成与自定义 Claims | `loginlogic.go` |
| Refresh Token 模式 | `refreshtokenlogic.go` |
| 从上下文读取 Claims | `userinfologic.go` |
| goctl model 带 Redis 缓存 | `internal/model/` |
