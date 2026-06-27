---
title: API JWT 인증
description: go-zero의 API JWT 인증에 대해 설명합니다.
sidebar:
  order: 8

---

## 개요


## JWT


위한 more 문서화 소개 JWT:

1. [JSON Web Tokens](./index.md)
2. [JWT 인증 가이드](https://jwt.io/)

Let's see how 로 declare JWT 인증 에서 api 파일

```go {27}
syntax = "v1"

type LoginReq {
    Username string `json:"username"`
    Password string `json:"password"`
}

type LoginResp {
    ID string `json:"id"`
    Name string `json:"name"`
}

type UserInfoReq {
    ID string `json:"id"`
}

type UserInfoResp {
    Name string `json:"name"`
}

service user-api {
    @handler login
    post /user/login (LoginReq) returns (LoginResp)
}

@server (
    jwt: Auth // 활성화
)
service user-api {
    @handler userInfo
    post /user/info (UserInfoReq) returns (UserInfoResp)
}

```


Below look briefly at 생성된 JWT code：

**설정.go**
```go {7-10}
package config

import "github.com/zeromicro/go-zero/rest"

type Config struct {
    rest.RestConf
    Auth struct {// JWT 서명 키
        AccessSecret string
        AccessExpire int64
    }
}
```


**라우트.go**
```go {31}
// 이 코드는 직접 수정하지 마세요
package handler

import (
    "net/http"

    "go-zero-demo/user/internal/svc"

    "github.com/zeromicro/go-zero/rest"
)

func RegisterHandlers(server *rest.Server, serverCtx *svc.ServiceContext) {
    server.AddRoutes(
        []rest.Route{
            {
                Method:  http.MethodPost,
                Path:    "/user/login",
                Handler: loginHandler(serverCtx),
            },
        },
    )

    server.AddRoutes(
        []rest.Route{
            {
                Method:  http.MethodPost,
                Path:    "/user/info",
                Handler: userInfoHandler(serverCtx),
            },
        },
        rest.WithJwt(serverCtx.Config.Auth.AccessSecret),
    )
}
```


:::caution takes 참고 의
:::
