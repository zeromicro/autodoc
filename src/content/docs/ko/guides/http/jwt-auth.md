---
title: JWT 인증
description: JSON Web Token 인증으로 go-zero HTTP 엔드포인트를 보호하는 방법입니다.
sidebar:
  order: 5

---


go-zero는 JWT 인증을 기본 지원합니다. API DSL의 `@server` 블록에서 `jwt`를 선언하면 프레임워크가 해당 블록의 엔드포인트에 token 검증 미들웨어를 자동으로 주입합니다. 이 가이드는 token 생성, claim 추출, refresh token, role 기반 접근 제어를 다룹니다.

## API Spec

```text
service user-api {
    // 공개 엔드포인트
    @handler Login
    post /user/login (LoginReq) returns (LoginResp)

    @handler RefreshToken
    post /user/refresh (RefreshReq) returns (LoginResp)
}

// 보호된 엔드포인트: jwt: Auth가 token 검증 미들웨어를 활성화합니다.
// Auth는 YAML 설정 파일의 JWT 설정 키와 매핑됩니다.
@server (
    jwt: Auth
)
service user-api {
    @handler GetProfile
    get /user/profile (ProfileReq) returns (ProfileResp)

    @handler UpdateProfile
    put /user/profile (UpdateProfileReq) returns (UpdateProfileResp)
}
```

## 설정

```yaml title="etc/user-api.yaml"
Auth:
  AccessSecret: "your-256-bit-secret-keep-this-safe"
  AccessExpire: 86400      # access token TTL: 24시간
RefreshSecret: "different-random-secret"
RefreshExpire: 604800      # refresh token TTL: 7일
```

설정 구조체를 매핑합니다.

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

## Access token 생성

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

## Refresh token

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

## 보호된 로직에서 claim 읽기

검증에 성공하면 go-zero는 모든 JWT claim을 request context에 저장합니다.

```go title="internal/logic/getprofilelogic.go"
func (l *GetProfileLogic) GetProfile(req *types.ProfileReq) (*types.ProfileResp, error) {
    // claim은 context를 통해 사용할 수 있습니다
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

## token 폐기

JWT는 설계상 stateless입니다. logout이나 token revocation을 지원하려면 Redis blocklist를 유지합니다.

```go
func (l *LogoutLogic) Logout(req *types.LogoutReq) error {
    // 검증 없이 parsing해 exp claim을 추출합니다
    token, _, _ := new(jwt.Parser).ParseUnverified(req.Token, jwt.MapClaims{})
    claims := token.Claims.(jwt.MapClaims)
    exp := int64(claims["exp"].(float64))
    ttl := time.Until(time.Unix(exp, 0))
    if ttl <= 0 {
        return nil  // 이미 만료되었습니다
    }
    // 자연 만료 시점까지 Redis에 저장합니다
    return l.svcCtx.Redis.Setex("jwt:revoked:"+req.Token, "1", int(ttl.Seconds()))
}
```

JWT 미들웨어가 실행되기 전에 blocklist를 확인하는 사용자 정의 미들웨어를 추가합니다.

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

## 테스트

```bash
# 1. 로그인
TOKEN=$(curl -s -X POST http://localhost:8888/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}' | jq -r .accessToken)

# 2. 보호된 엔드포인트 접근
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8888/user/profile

# 3. 갱신
NEW_TOKEN=$(curl -s -X POST http://localhost:8888/user/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\":\"$REFRESH\"}" | jq -r .accessToken)
```

## 보안 모범 사례

- 단일 서비스 시나리오에서는 32 byte 이상의 secret과 함께 **HS256**(HMAC-SHA256)을 사용하세요. 여러 서비스가 token을 공유한다면 **RS256**을 권장합니다.
- `AccessExpire`는 짧게 유지하고(15분–24시간), 오래 유지되는 session에는 refresh token을 사용하세요.
- `AccessSecret`은 plain YAML이 아니라 Vault, AWS Secrets Manager 같은 secret manager에 저장하세요.
- `exp`, `iat`, `iss` claim을 항상 검증하세요. go-zero의 내장 validator는 `exp`를 자동으로 처리합니다.
