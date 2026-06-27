---
title: API 서비스 만들기
description: 사용자 정의 DSL 정의에서 완전한 HTTP API 서비스를 만듭니다.
sidebar:
  order: 9
---


이 가이드는 로그인과 프로필 엔드포인트가 있는 간단한 **user service**를 만듭니다. `.api` DSL 파일을 작성하고, 프로젝트를 생성한 뒤, 비즈니스 로직을 채웁니다.

## 1단계 — API DSL 작성

디렉터리를 만들고 DSL을 작성합니다.

```bash
mkdir user-api && cd user-api
```

`user.api`를 만듭니다.

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

## 2단계 — 서비스 생성

```bash
goctl api go -api user.api -dir .
go mod init user-api
go mod tidy
```

생성되는 구조는 다음과 같습니다.

```
user-api/
├── etc/
│   └── user-api.yaml
├── internal/
│   ├── config/config.go
│   ├── handler/
│   │   ├── loginhandler.go         # 예시입니다
│   │   ├── getuserinfohandler.go   # 예시입니다
│   │   └── routes.go
│   ├── logic/
│   │   ├── loginlogic.go           # 예시입니다
│   │   └── getuserinfologic.go     # 예시입니다
│   ├── svc/servicecontext.go
│   └── types/types.go             # DSL 예시입니다
└── user.go
```

## 3단계 — 로직 구현

`internal/logic/loginlogic.go`를 수정합니다.

```go
func (l *LoginLogic) Login(req *types.LoginReq) (resp *types.LoginResp, err error) {
    // In, DB, JWT 예시입니다
    if req.Username == "admin" && req.Password == "secret" {
        return &types.LoginResp{
            Token: "mock-jwt-token-for-" + req.Username,
        }, nil
    }
    return nil, errors.New("invalid credentials")
}
```

`internal/logic/getuserinfologic.go`도 수정합니다.

```go
func (l *GetUserInfoLogic) GetUserInfo(req *types.UserInfoReq) (resp *types.UserInfoResp, err error) {
    // In, DB 예시입니다
    return &types.UserInfoResp{
        Id:       req.Id,
        Username: "alice",
        Email:    "alice@example.com",
    }, nil
}
```

## 4단계 — 실행과 테스트

```bash
go run user.go
```

다른 터미널에서 호출합니다.

```bash
# Login
curl -s -X POST http://localhost:8888/user/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"secret"}'
# 예시입니다

# 가져옵니다
curl http://localhost:8888/user/1
# 예시입니다
```

## DSL 변경 후 다시 생성하기

`user.api`를 변경할 때마다 로직 파일을 덮어쓰지 않고 다시 생성할 수 있습니다.

```bash
goctl api go -api user.api -dir .
```

goctl은 자신이 소유한 파일(`handler/`, `types/`, `routes.go`)만 덮어씁니다. `logic/` 파일은 보존됩니다.

## 다음 단계

- 엔드포인트 보호를 위해 [JWT 미들웨어](../../http/server/middleware) 추가
- [데이터베이스 모델](../../database/mysql) 연결
- [RPC 서비스 만들기 →](../rpc-service)
