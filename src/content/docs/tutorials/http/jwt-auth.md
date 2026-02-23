---
title: JWT Authentication
description: Protect go-zero HTTP endpoints with JSON Web Token authentication.
sidebar:
  order: 3
---

# JWT Authentication

go-zero supports JWT auth natively — declare `@jwt` in your API spec and the framework handles token validation automatically. This guide covers token generation, claim extraction, refresh tokens, and role-based access.

## API Spec

```text
service user-api {
    // Public endpoints
    @handler Login
    post /user/login (LoginReq) returns (LoginResp)

    @handler RefreshToken
    post /user/refresh (RefreshReq) returns (LoginResp)

    // Protected endpoints — @jwt injects token validation middleware
    @jwt Auth
    @handler GetProfile
    get /user/profile (ProfileReq) returns (ProfileResp)

    @jwt Auth
    @handler UpdateProfile
    put /user/profile (UpdateProfileReq) returns (UpdateProfileResp)
}
```

## Configuration

```yaml title="etc/user-api.yaml"
Auth:
  AccessSecret: "your-256-bit-secret-keep-this-safe"
  AccessExpire: 86400      # access token TTL: 24 hours
RefreshSecret: "different-random-secret"
RefreshExpire: 604800      # refresh token TTL: 7 days
```

Map the config struct:

```go title="internal/config/config.go"
type Config struct {
    rest.RestConf
    Auth struct {
        AccessSecret string
        AccessExpire int64
    }
    RefreshSecret string
    RefreshExpire int64
}
```

## Generate Access Token

```go title="internal/logic/loginlogic.go"
import (
    "time"
    "github.com/golang-jwt/jwt/v4"
)

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
        return nil, errorx.NewCodeError(401, "invalid credentials")
    }
    if !checkPassword(req.Password, user.Password) {
        return nil, errorx.NewCodeError(401, "invalid credentials")
    }

    accessToken, err := generateAccessToken(
        l.svcCtx.Config.Auth.AccessSecret, user.Id, user.Role)
    if err != nil {
        return nil, err
    }

    refreshToken, err := generateRefreshToken(
        l.svcCtx.Config.RefreshSecret, user.Id)
    if err != nil {
        return nil, err
    }

    return &types.LoginResp{
        AccessToken:  accessToken,
        RefreshToken: refreshToken,
        ExpiresIn:    l.svcCtx.Config.Auth.AccessExpire,
    }, nil
}
```

## Refresh Token

```go title="internal/logic/refreshtokenlogic.go"
func generateRefreshToken(secret string, userId int64) (string, error) {
    claims := jwt.MapClaims{
        "userId": userId,
        "exp":    time.Now().Add(7 * 24 * time.Hour).Unix(),
    }
    return jwt.NewWithClaims(jwt.SigningMethodHS256, claims).
        SignedString([]byte(secret))
}

func (l *RefreshTokenLogic) RefreshToken(req *types.RefreshReq) (*types.LoginResp, error) {
    token, err := jwt.ParseWithClaims(req.RefreshToken, jwt.MapClaims{},
        func(t *jwt.Token) (any, error) {
            return []byte(l.svcCtx.Config.RefreshSecret), nil
        })
    if err != nil || !token.Valid {
        return nil, errorx.NewCodeError(401, "invalid or expired refresh token")
    }

    claims := token.Claims.(jwt.MapClaims)
    userId := int64(claims["userId"].(float64))

    user, err := l.svcCtx.UserModel.FindOne(l.ctx, userId)
    if err != nil {
        return nil, err
    }

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

## Read Claims in Protected Logic

After successful validation, go-zero stores all JWT claims in the request context:

```go title="internal/logic/getprofilelogic.go"
func (l *GetProfileLogic) GetProfile(req *types.ProfileReq) (*types.ProfileResp, error) {
    // Claims are available via context
    userId, _ := l.ctx.Value("userId").(json.Number).Int64()
    role, _ := l.ctx.Value("role").(string)

    if role != "admin" && userId != req.TargetId {
        return nil, errorx.NewCodeError(403, "forbidden")
    }

    user, err := l.svcCtx.UserModel.FindOne(l.ctx, userId)
    if err != nil {
        return nil, err
    }
    return &types.ProfileResp{Id: user.Id, Name: user.Username}, nil
}
```

## Token Revocation

JWT is stateless by design. To support logout / revocation, maintain a Redis blocklist:

```go
func (l *LogoutLogic) Logout(req *types.LogoutReq) error {
    // Parse without validation to extract exp claim
    token, _, _ := new(jwt.Parser).ParseUnverified(req.Token, jwt.MapClaims{})
    claims := token.Claims.(jwt.MapClaims)
    exp := int64(claims["exp"].(float64))
    ttl := time.Until(time.Unix(exp, 0))
    if ttl <= 0 {
        return nil  // already expired
    }
    // Store in Redis until natural expiry
    return l.svcCtx.Redis.Setex("jwt:revoked:"+req.Token, "1", int(ttl.Seconds()))
}
```

Add a custom middleware that checks the blocklist before the JWT middleware runs:

```go
func RevocationMiddleware(rdb *redis.Redis) rest.Middleware {
    return func(next http.HandlerFunc) http.HandlerFunc {
        return func(w http.ResponseWriter, r *http.Request) {
            raw := strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
            if raw != "" {
                if val, _ := rdb.Get("jwt:revoked:" + raw); val == "1" {
                    httpx.WriteJson(w, http.StatusUnauthorized,
                        map[string]string{"msg": "token revoked"})
                    return
                }
            }
            next(w, r)
        }
    }
}
```

## Test

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8888/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}' | jq -r .accessToken)

# 2. Access protected endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8888/user/profile

# 3. Refresh
NEW_TOKEN=$(curl -s -X POST http://localhost:8888/user/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\":\"$REFRESH\"}" | jq -r .accessToken)
```

## Security Best Practices

- Use **HS256** (HMAC-SHA256) with a secret ≥32 bytes for single-service scenarios; prefer **RS256** for multi-service token sharing.
- Keep `AccessExpire` short (15 min – 24 h) and use refresh tokens for long-lived sessions.
- Store `AccessSecret` in a secret manager (Vault, AWS Secrets Manager), not in plain YAML.
- Always validate `exp`, `iat`, and `iss` claims; go-zero's built-in validator handles `exp` automatically.
