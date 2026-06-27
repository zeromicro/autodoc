---
title: API 라우트 접두사
description: go-zero의 API 라우트 접두사에 대해 설명합니다.
sidebar:
  order: 4

---


## 개요


## 라우트 접두사


```
https://example.com/v1/users
https://example.com/v2/users
```


```go {12,20}
syntax = "v1"

type UserV1 {
    Name string `json:"name"`
}

type UserV2 {
    Name string `json:"name"`
}

@server (
    prefix: /v1
)
service user-api {
    @handler usersv1
    get /users returns ([]UserV1)
}

@server (
    prefix: /v2
)
service user-api {
    @handler usersv2
    get /users returns ([]UserV2)
}


```


Below look briefly at 생성된 routing code：

```go {10,21}
func RegisterHandlers(server *rest.Server, serverCtx *svc.ServiceContext) {
    server.AddRoutes(
        []rest.Route{
            {
                Method:  http.MethodGet,
                Path:    "/users",
                Handler: usersv1Handler(serverCtx),
            },
        },
        rest.WithPrefix("/v1"),
    )

    server.AddRoutes(
        []rest.Route{
            {
                Method:  http.MethodGet,
                Path:    "/users",
                Handler: usersv2Handler(serverCtx),
            },
        },
        rest.WithPrefix("/v2"),
    )
}
```
