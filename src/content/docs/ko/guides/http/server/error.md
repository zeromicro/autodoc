---
title: 오류 처리
description: go-zero HTTP 서비스에서 오류를 처리하고 포맷하는 방법입니다.
sidebar:
  order: 4

---


## 개요

여기서 말하는 오류 처리는 stack 처리나 오류 관리 전반이 아니라 HTTP 응답 오류 처리 방식을 의미합니다.

## 예제

오류가 `*errors.CodeMsg`일 때 `code-msg` 형식으로 응답하는 예제를 만들어 보겠습니다.

```go
package main

import (
    "net/http"

    "github.com/zeromicro/go-zero/rest"
    "github.com/zeromicro/go-zero/rest/httpx"
    "github.com/zeromicro/x/errors"
    xhttp "github.com/zeromicro/x/http"
)

func main() {
    srv := rest.MustNewServer(rest.RestConf{
        Port: 8080,
    })
    srv.AddRoute(rest.Route{
        Method:  http.MethodPost,
        Path:    "/hello",
        Handler: handle,
    })
    defer srv.Stop()
    // httpx.SetErrorHandler는 httpx.Error로 응답을 처리할 때만 적용됩니다.
    httpx.SetErrorHandler(func(err error) (int, any) {
        switch e := err.(type) {
        case *errors.CodeMsg:
            return http.StatusOK, xhttp.BaseResponse[struct{}]{
                Code: e.Code,
                Msg:  e.Msg,
            }
        default:
            return http.StatusInternalServerError, nil
        }
    })
    srv.Start()
}

type HelloRequest struct {
    Name string `json:"name"`
}

type HelloResponse struct {
    Msg string `json:"msg"`
}

func handle(w http.ResponseWriter, r *http.Request) {
    var req HelloRequest
    if err := httpx.Parse(r, &req); err != nil {
        httpx.Error(w, err)
        return
    }

    if req.Name == "error" {
        // 매개변수 오류를 흉내 냅니다
        httpx.Error(w, errors.New(400, "dummy error"))
        return
    }

    httpx.OkJson(w, HelloResponse{
        Msg: "hello " + req.Name,
    })
}

```

```shell
$ curl --location '127.0.0.1:8080/hello' \
--header 'Content-Type: application/json' \
--data '{
    "name":"go-zero"
}'
{"msg":"hello go-zero"}

$ curl --location '127.0.0.1:8080/hello' \
--header 'Content-Type: application/json' \
--data '{
    "name":"error"
}'
{"code":400,"msg":"dummy error","data":{}}
```

:::tip
이 예제는 `httpx.SetErrorHandler`만 보여 줍니다. 전체 unified response pattern은 [통합 응답 형식](./response-ext.md)을 참고하세요.
:::
