---
title: JWT를 사용하는 REST API
description: JWT 인증, MySQL 모델, Redis 캐시를 사용하는 go-zero REST API 예제입니다.
sidebar:
  order: 3

---


이 예제는 go-zero로 로그인, 토큰 갱신, 보호된 사용자 정보 조회를 제공하는 REST API를 구성하는 방법을 보여 줍니다.

## 프로젝트 구조

```bash
# API 코드 생성
goctl api go -api user.api -dir .
```

```
user-api/
├── user.api            # API 정의
├── etc/user-api.yaml   # 설정 파일
├── user.go             # 서비스 진입점
└── internal/
    ├── config/
    ├── handler/        # HTTP 핸들러
    ├── logic/
    │   ├── loginlogic.go
    │   ├── refreshtokenlogic.go
    │   └── userinfologic.go
    ├── model/          # MySQL 모델
    ├── svc/
    └── types/          # 요청/응답 타입
```

## API 정의

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

## 설정

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

## 로그인 로직

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

// jwtx 헬퍼(internal/jwtx/token.go에 추가)
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

## 사용자 정보 조회(보호된 엔드포인트)

```go title="internal/logic/userinfologic.go"
func (l *UserInfoLogic) UserInfo() (*types.UserInfoResp, error) {
    // go-zero JWT 미들웨어가 주입한 Claims입니다
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

## 전체 테스트 흐름

```bash
# 서비스 시작
go run user.go -f etc/user-api.yaml

# 사용자 등록
curl -s -X POST http://localhost:8888/user/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}'

# 로그인
RESP=$(curl -s -X POST http://localhost:8888/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}')

ACCESS=$(echo $RESP | jq -r .accessToken)
REFRESH=$(echo $RESP | jq -r .refreshToken)

# 보호된 엔드포인트 호출
curl -H "Authorization: Bearer $ACCESS" \
  http://localhost:8888/user/info
# {"id":1,"username":"alice","role":"user"}

# 토큰 갱신
NEW=$(curl -s -X POST http://localhost:8888/user/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\":\"$REFRESH\"}")

echo $NEW | jq .accessToken
```

## 이 예제가 보여 주는 것

| 주제 | 위치 |
|-------|-------|
| `@jwt` DSL annotation | `user.api` |
| 사용자 정의 claims를 포함한 JWT 생성 | `loginlogic.go` |
| Refresh 토큰 패턴 | `refreshtokenlogic.go` |
| 컨텍스트에서 claims 읽기 | `userinfologic.go` |
| goctl 모델과 Redis 캐시 | `internal/model/` |
| ServiceContext 의존성 주입 | `internal/svc/` |
