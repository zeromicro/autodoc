---
title: API 미들웨어 선언
description: go-zero의 API 미들웨어 선언에 대해 설명합니다.
sidebar:
  order: 7

---

## 개요


## 미들웨어 declaration


```go {14}
syntax = "v1"

type UserInfoRequest {
    Id int64 `path:"id"`
}
type UserInfoResponse {
    Id   int64  `json:"id"`
    Name string `json:"name"`
    Age  int32  `json:"age"`
}

@server(
    // LogMiddleware 미들웨어 선언
    middleware: UserAgentMiddleware
)
service user {
    @handler userinfo
    get /user/info/:id (UserInfoRequest) returns (UserInfoResponse)
}
```


디렉터리 Structure

```bash
.
├── etc
│   └── user.yaml
├── internal
│   ├── config
│   │   └── config.go
│   ├── handler
│   │   ├── routes.go
│   │   └── userinfohandler.go
│   ├── logic
│   │   └── userinfologic.go
│   ├── middleware # 예시입니다
│   │   └── useragentmiddleware.go
│   ├── svc
│   │   └── servicecontext.go
│   └── types
│       └── types.go
├── user.api
└── user.go

8 directories, 10 files
```

미들웨어 code (없음 fill 로직)

**useragentmiddleware.go**
```go
package middleware

import "net/http"

type UserAgentMiddleware struct {
}

func NewUserAgentMiddleware() *UserAgentMiddleware {
    return &UserAgentMiddleware{}
}

func (m *UserAgentMiddleware) Handle(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // TODO: 필요한 로직을 작성하세요

        // 다음 핸들러로 전달
        next(w, r)
    }
}
```

**servicecontext.go**
```go {17}
package svc

import (
    "demo/user/internal/config"
    "demo/user/internal/middleware"
    "github.com/zeromicro/go-zero/rest"
)

type ServiceContext struct {
    Config              config.Config
    UserAgentMiddleware rest.Middleware
}

func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:              c,
        UserAgentMiddleware: middleware.NewUserAgentMiddleware().Handle,
    }
}

```

**라우트.go**
```go {15}
// 이 코드는 직접 수정하지 마세요
package handler

import (
    "net/http"

    "demo/user/internal/svc"

    "github.com/zeromicro/go-zero/rest"
)

func RegisterHandlers(server *rest.Server, serverCtx *svc.ServiceContext) {
    server.AddRoutes(
        rest.WithMiddlewares(
            []rest.Middleware{serverCtx.UserAgentMiddleware},
            []rest.Route{
                {
                    Method:  http.MethodGet,
                    Path:    "/user/info/:id",
                    Handler: userinfoHandler(serverCtx),
                },
            }...,
        ),
    )
}

```


```go {17-20}
package middleware

import (
    "context"
    "net/http"
)

type UserAgentMiddleware struct {
}

func NewUserAgentMiddleware() *UserAgentMiddleware {
    return &UserAgentMiddleware{}
}

func (m *UserAgentMiddleware) Handle(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        val := r.Header.Get("User-Agent")
        reqCtx := r.Context()
        ctx := context.WithValue(reqCtx, "User-Agent", val)
        newReq := r.WithContext(ctx)
        next(w, newReq)
    }
}
```
