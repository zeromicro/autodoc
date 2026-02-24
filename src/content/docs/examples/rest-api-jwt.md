---
title: REST API with JWT
description: A go-zero HTTP service protected with JWT authentication.
sidebar:
  order: 3

---

# REST API with JWT

This example demonstrates building a secure REST API with JWT-based authentication, a MySQL-backed user store, and Redis session management using go-zero.

## Project Layout

```bash
# Scaffold the project
goctl api go -api user.api -dir .
```

```
user-api/
├── user.api            # API definition
├── etc/user-api.yaml   # configuration
├── user.go             # entry point
└── internal/
    ├── config/
    ├── handler/          # HTTP handlers (generated)
    ├── logic/
    │   ├── loginlogic.go
    │   ├── refreshtokenlogic.go
    │   └── userinfologic.go
    ├── model/            # MySQL model (goctl generated)
    ├── svc/
    └── types/            # request/response structs
```

## API Definition

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

## Configuration

```yaml title="etc/user-api.yaml"
Name: user-api
Host: 0.0.0.0
Port: 8888

Auth:
  AccessSecret: "change-me-to-a-random-256-bit-value"
  AccessExpire: 86400

RefreshSecret: "another-different-random-secret"
RefreshExpire: 604800

DataSource: "root:password@tcp(127.0.0.1:3306)/userdb?parseTime=true"
CacheRedis:
  - Host: 127.0.0.1:6379
    Type: node
```

## ServiceContext

```go title="internal/svc/servicecontext.go"
type ServiceContext struct {
    Config    config.Config
    UserModel model.UserModel
    Redis     *redis.Redis
}

func NewServiceContext(c config.Config) *ServiceContext {
    conn := sqlx.NewMysql(c.DataSource)
    return &ServiceContext{
        Config:    c,
        UserModel: model.NewUserModel(conn, c.CacheRedis),
        Redis:     redis.MustNewRedis(c.CacheRedis[0].RedisConf),
    }
}
```

## Login Logic

```go title="internal/logic/loginlogic.go"
func (l *LoginLogic) Login(req *types.LoginReq) (*types.LoginResp, error) {
    user, err := l.svcCtx.UserModel.FindOneByUsername(l.ctx, req.Username)
    if errors.Is(err, model.ErrNotFound) {
        return nil, errorx.NewCodeError(401, "invalid credentials")
    }
    if err != nil {
        return nil, err
    }
    if !checkPasswordHash(req.Password, user.Password) {
        return nil, errorx.NewCodeError(401, "invalid credentials")
    }

    now := time.Now()
    accessSecret := l.svcCtx.Config.Auth.AccessSecret
    accessExpire := l.svcCtx.Config.Auth.AccessExpire

    accessToken, err := jwtx.GenerateToken(accessSecret, now.Unix(), accessExpire,
        map[string]any{"userId": user.Id, "role": user.Role})
    if err != nil {
        return nil, err
    }

    refreshSecret := l.svcCtx.Config.RefreshSecret
    refreshExpire := l.svcCtx.Config.RefreshExpire
    refreshToken, err := jwtx.GenerateToken(refreshSecret, now.Unix(), refreshExpire,
        map[string]any{"userId": user.Id})
    if err != nil {
        return nil, err
    }

    return &types.LoginResp{
        AccessToken:  accessToken,
        RefreshToken: refreshToken,
        ExpiresIn:    accessExpire,
    }, nil
}

// jwtx helper (add to internal/jwtx/token.go)
func GenerateToken(secretKey string, iat, seconds int64, payloads map[string]any) (string, error) {
    claims := make(jwt.MapClaims)
    for k, v := range payloads {
        claims[k] = v
    }
    claims["exp"] = iat + seconds
    claims["iat"] = iat
    return jwt.NewWithClaims(jwt.SigningMethodHS256, claims).
        SignedString([]byte(secretKey))
}
```

## User Info (Protected)

```go title="internal/logic/userinfologic.go"
func (l *UserInfoLogic) UserInfo() (*types.UserInfoResp, error) {
    // Claims injected by go-zero JWT middleware
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

## Full Test Flow

```bash
# 1. Start the service
go run user.go -f etc/user-api.yaml

# 2. Register (if you have a /user/register endpoint)
curl -s -X POST http://localhost:8888/user/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}'

# 3. Login — capture tokens
RESP=$(curl -s -X POST http://localhost:8888/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}')

ACCESS=$(echo $RESP | jq -r .accessToken)
REFRESH=$(echo $RESP | jq -r .refreshToken)

# 4. Call protected endpoint
curl -H "Authorization: Bearer $ACCESS" \
  http://localhost:8888/user/info
# {"id":1,"username":"alice","role":"user"}

# 5. Refresh when access token expires
NEW=$(curl -s -X POST http://localhost:8888/user/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\":\"$REFRESH\"}")

echo $NEW | jq .accessToken
```

## What This Example Teaches

| Topic | Where |
|-------|-------|
| `@jwt` DSL annotation | `user.api` |
| JWT generation with custom claims | `loginlogic.go` |
| Refresh token pattern | `refreshtokenlogic.go` |
| Reading claims from context | `userinfologic.go` |
| goctl model with Redis cache | `internal/model/` |
| ServiceContext dependency injection | `internal/svc/` |
