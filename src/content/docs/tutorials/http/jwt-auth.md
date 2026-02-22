---
title: JWT Authentication
description: Protect go-zero HTTP endpoints with JSON Web Token authentication.
sidebar:
  order: 3
---

# JWT Authentication

go-zero supports JWT auth natively — declare `@jwt` in your API spec and the framework handles token validation automatically.

## API Spec

```text
service user-api {
    // public
    @handler Login
    post /user/login (LoginReq) returns (LoginResp)

    // protected
    @jwt Auth
    @handler GetProfile
    get /user/profile (ProfileReq) returns (ProfileResp)
}
```

## Configuration

```yaml title="etc/user-api.yaml"
Auth:
  AccessSecret: "your-256-bit-secret"
  AccessExpire: 86400
```

## Generate a Token

```go title="internal/logic/loginlogic.go"
import (
    "time"
    "github.com/golang-jwt/jwt/v4"
)

func generateToken(secret string, userId int64) (string, error) {
    claims := jwt.MapClaims{
        "userId": userId,
        "exp":    time.Now().Add(24 * time.Hour).Unix(),
    }
    return jwt.NewWithClaims(jwt.SigningMethodHS256, claims).SignedString([]byte(secret))
}
```

## Read Claims in Logic

```go
userId, _ := l.ctx.Value("userId").(json.Number).Int64()
```

## Test

```bash
TOKEN=$(curl -s -X POST http://localhost:8888/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}' | jq -r .token)

curl -H "Authorization: Bearer $TOKEN" http://localhost:8888/user/profile
```
