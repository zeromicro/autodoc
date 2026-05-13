---
title: Request Signing
description: go-zero의 Request Signing에 대해 설명합니다.
sidebar:
  order: 9

---


## 개요


## 서명 스위치


```
https://example.com/sign/demo
```

Its api language follows：

```go {13}
syntax = "v1"

type (
    SignDemoReq {
        Msg string `json:"msg"`
    }
    SignDemoResp {
        Msg string `json:"msg"`
    }
)

@server (
    signature: true // 通过 signature 关键字开启签名功能
)
service sign-api {
    @handler SignDemo
    post /sign/demo (SignDemoReq) returns (SignDemoResp)
}


```


```go {10}
func RegisterHandlers(server *rest.Server, serverCtx *svc.ServiceContext) {
    server.AddRoutes(
        []rest.Route{
            {
                Method:  http.MethodPost,
                Path:    "/sign/demo",
                Handler: SignDemoHandler(serverCtx),
            },
        },
        rest.WithSignature(serverCtx.Config.Signature),
    )
}
```
