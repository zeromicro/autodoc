---
title: 템플릿 커스터마이징
description: go-zero의 템플릿 커스터마이징에 대해 설명합니다.
sidebar:
  order: 2
---


## 개요


위한 템플릿 명령 usage, see [goctl 템플릿](../cli-guide/template.md).

## 샘플

## 사용 장면

Implementing unified 본문 응답, 다음：

```json
{
  "code": 0,
  "msg": "OK",
  "data": {} // ①
}
```

① Actual 응답 데이터

:::tip
`go-zero`생성된 코드 아님 handled
:::

### 준비

我们提前在 `module` 为 `greet` 的工程下的 `response` 包中写一个 `Response` 方法，目录树类似如下：

```text
greet
├── response
│   └── response.go
└── xxx...
```

Code:

```go
package response

import (
    "net/http"

    "github.com/zeromicro/go-zero/rest/httpx"
)

type Body struct {
    Code int         `json:"code"`
    Msg  string      `json:"msg"`
    Data interface{} `json:"data,omitempty"`
}

func Response(w http.ResponseWriter, resp interface{}, err error) {
    var body Body
    if err != nil {
        body.Code = -1
        body.Msg = err.Error()
    } else {
        body.Msg = "OK"
        body.Data = resp
    }
    httpx.OkJson(w, body)
}
```

### Edit `handler` 템플릿

```shell
$ vim ~/.goctl/${goctl_version}/api/handler.tpl
```

Replace 템플릿 사용하여 다음

```go
package handler

import (
    "net/http"
    "greet/response"// ①
    {{.ImportPackages}}
)

func {{.HandlerName}}(svcCtx *svc.ServiceContext) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        {{if .HasRequest}}var req types.{{.RequestType}}
        if err := httpx.Parse(r, &req); err != nil {
            httpx.Error(w, err)
            return
        }{{end}}

        l := logic.New{{.LogicType}}(r.Context(), svcCtx)
        {{if .HasResp}}resp, {{end}}err := l.{{.Call}}({{if .HasRequest}}&req{{end}})
        {{if .HasResp}}response.Response(w, resp, err){{else}}response.Response(w, nil, err){{end}}//②

    }
}
```

① Replace 사용하여 your real`response`패키지 name, information

② Custom 템플릿 Content

:::tip

```bash
goctl template init
```
:::

### Compare 템플릿 전에과 후에

- Modify 전에

```go
func GreetHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        var req types.Request
        if err := httpx.Parse(r, &req); err != nil {
            httpx.Error(w, err)
            return
        }

        l := logic.NewGreetLogic(r.Context(), svcCtx)
        resp, err := l.Greet(&req)
        // 以下内容将被自定义模板替换
        if err != nil {
            httpx.Error(w, err)
        } else {
            httpx.OkJson(w, resp)
        }
    }
}
```

- Modified

```go
func GreetHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        var req types.Request
        if err := httpx.Parse(r, &req); err != nil {
            httpx.Error(w, err)
            return
        }

        l := logic.NewGreetLogic(r.Context(), svcCtx)
        resp, err := l.Greet(&req)
        response.Response(w, resp, err)
    }
}
```

### Modify 응답 본문 comparison 전에과 후에 템플릿

- Modify 전에

```json
{
  "message": "Hello go-zero!"
}
```

- Modified

```json
{
  "code": 0,
  "msg": "OK",
  "data": {
    "message": "Hello go-zero!"
  }
}
```

## 템플릿 Custom Rules

2. Adding 템플릿 파일 is 아님 supported
3. Variable changes 아님 supported

## 참조

- [goctl 템플릿](../cli-guide/template.md)
- [text/template](https://golang.org/pkg/text/template/)
