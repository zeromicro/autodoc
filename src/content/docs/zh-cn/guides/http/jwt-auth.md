---
title: JWT 认证
description: 在 API 服务中启用 JWT 鉴权。
sidebar:
  order: 5

---

# JWT 认证

go-zero 原生支持 JWT 认证——在 API DSL 中声明 `@jwt`，框架自动注入 Token 验证中间件。

## API 规范

```text
service user-api {
    // 公开接口
    @handler Login
    post /user/login (LoginReq) returns (LoginResp)

    @handler RefreshToken
    post /user/refresh (RefreshReq) returns (LoginResp)

    // 受保护接口，@jwt 自动注入 Token 验证
    @jwt Auth
    @handler GetProfile
    get /user/profile (ProfileReq) returns (ProfileResp)
}
```

## 配置

```yaml title="etc/user-api.yaml"
Auth:
  AccessSecret: "your-256-bit-secret"
  AccessExpire: 86400        # Access Token 有效期：24 小时
RefreshSecret: "another-random-secret"
RefreshExpire: 604800        # Refresh Token 有效期：7 天
```

## 生成 Access Token

```go title="internal/logic/loginlogic.go"
func generateAccessToken(secret string, userId int64, role string) (string, error) {
    now := time.Now()
    claims := jwt.MapClaims{
        "userId": userId,
        "role":   role,
        "iat":    now.Unix(),
        "exp":    now.Add(24 * time.Hour).Unix(),
    }
    return jwt.NewWithClaims(jwt.SigningMethodHS256, claims).
        SignedString([]byte(secret))
}

func (l *LoginLogic) Login(req *types.LoginReq) (*types.LoginResp, error) {
    user, err := l.svcCtx.UserModel.FindOneByUsername(l.ctx, req.Username)
    if err != nil {
        return nil, errorx.NewCodeError(401, "用户名或密码错误")
    }
    if !checkPassword(req.Password, user.Password) {
        return nil, errorx.NewCodeError(401, "用户名或密码错误")
    }

    accessToken, _ := generateAccessToken(
        l.svcCtx.Config.Auth.AccessSecret, user.Id, user.Role)
    refreshToken, _ := generateRefreshToken(
        l.svcCtx.Config.RefreshSecret, user.Id)

    return &types.LoginResp{
        AccessToken:  accessToken,
        RefreshToken: refreshToken,
        ExpiresIn:    l.svcCtx.Config.Auth.AccessExpire,
    }, nil
}
```

## 刷新 Token

```go title="internal/logic/refreshtokenlogic.go"
func (l *RefreshTokenLogic) RefreshToken(req *types.RefreshReq) (*types.LoginResp, error) {
    token, err := jwt.ParseWithClaims(req.RefreshToken, jwt.MapClaims{},
        func(t *jwt.Token) (any, error) {
            return []byte(l.svcCtx.Config.RefreshSecret), nil
        })
    if err != nil || !token.Valid {
        return nil, errorx.NewCodeError(401, "Refresh Token 已失效或非法")
    }
    claims := token.Claims.(jwt.MapClaims)
    userId := int64(claims["userId"].(float64))

    user, _ := l.svcCtx.UserModel.FindOne(l.ctx, userId)
    newAccess, _ := generateAccessToken(
        l.svcCtx.Config.Auth.AccessSecret, userId, user.Role)
    newRefresh, _ := generateRefreshToken(
        l.svcCtx.Config.RefreshSecret, userId)

    return &types.LoginResp{
        AccessToken:  newAccess,
        RefreshToken: newRefresh,
        ExpiresIn:    l.svcCtx.Config.Auth.AccessExpire,
    }, nil
}
```

## 在受保护逻辑中读取 Claims

go-zero 验证成功后将所有 JWT Claims 存入请求上下文：

```go title="internal/logic/getprofilelogic.go"
func (l *GetProfileLogic) GetProfile(req *types.ProfileReq) (*types.ProfileResp, error) {
    userId, _ := l.ctx.Value("userId").(json.Number).Int64()
    role, _ := l.ctx.Value("role").(string)

    if role != "admin" && userId != req.TargetId {
        return nil, errorx.NewCodeError(403, "无权访问")
    }
    // ...
}
```

## Token 吐销

利用 Redis 维护黑名单，实现登出 / Token 吹销：

```go
func (l *LogoutLogic) Logout(req *types.LogoutReq) error {
    token, _, _ := new(jwt.Parser).ParseUnverified(req.Token, jwt.MapClaims{})
    claims := token.Claims.(jwt.MapClaims)
    exp := int64(claims["exp"].(float64))
    ttl := time.Until(time.Unix(exp, 0))
    if ttl <= 0 {
        return nil
    }
    return l.svcCtx.Redis.Setex(
        "jwt:revoked:"+req.Token, "1", int(ttl.Seconds()))
}
```

## 测试

```bash
# 1. 登录
RESP=$(curl -s -X POST http://localhost:8888/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}')
ACCESS=$(echo $RESP | jq -r .accessToken)

# 2. 访问受保护接口
curl -H "Authorization: Bearer $ACCESS" \
  http://localhost:8888/user/profile
```

## 安全建议

- 使用长度 ≥32 字节的随机密钥，存储到密钥管理服务（Vault / KMS）中。
- `AccessExpire` 建议设为 15 分钟到24 小时，配合 Refresh Token 维持会话。
- 多服务共享 Token 时推荐改用 RS256。
