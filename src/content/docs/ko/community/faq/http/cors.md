---
title: CORS 설정
description: go-zero REST 서버에서 CORS를 설정하는 방법입니다.
sidebar:
  order: 2
---


`go-zero`는 CORS 처리를 위한 세 가지 옵션을 제공합니다.

- `rest.WithCors(origin ...string)`
  - 교차 출처 요청에 허용할 origin을 설정합니다.
- `rest.WithCorsHeaders(headers ...string)`
  - 교차 출처 요청에 허용할 헤더를 설정합니다.
- `rest.WithCustomCors(...)`
  - 복잡한 CORS 요구 사항을 직접 구성합니다.

## CORS 헤더를 커스터마이징하려면?

`rest.WithCorsHeaders(headers ...string)`를 사용해 교차 출처 요청에 허용할 헤더를 추가할 수 있습니다.

예제 코드:

```go
package main

import (
	"fmt"
	"net/http"

	"github.com/zeromicro/go-zero/core/conf"
	"github.com/zeromicro/go-zero/core/logx"
	"github.com/zeromicro/go-zero/rest"
	"github.com/zeromicro/go-zero/rest/httpx"
)

func main() {
	var c rest.RestConf
	conf.MustLoad("config.yaml", &c)

	server := rest.MustNewServer(c, rest.WithCorsHeaders("UserHeader1", "UserHeader2"))
	defer server.Stop()

	server.AddRoutes(
		[]rest.Route{
			{
				Method: http.MethodPost,
				Path:   "/test",
				Handler: func(w http.ResponseWriter, r *http.Request) {
					logx.Info("Request received")
					httpx.OkJsonCtx(r.Context(), w, "1")
				},
			},
		},
	)

	fmt.Printf("Starting server at %s:%d...\n", c.Host, c.Port)
	server.Start()
}
```

> go-zero 버전: >= v1.7.1

## CORS 도메인을 커스터마이징하려면?

`rest.WithCors`에 허용할 origin을 전달합니다.

예제 코드:

```go
package main

import (
	"fmt"
	"net/http"

	"github.com/zeromicro/go-zero/core/conf"
	"github.com/zeromicro/go-zero/core/logx"
	"github.com/zeromicro/go-zero/rest"
	"github.com/zeromicro/go-zero/rest/httpx"
)

func main() {
	var c rest.RestConf
	conf.MustLoad("config.yaml", &c)

	// 교차 출처 요청에 허용할 origin을 설정합니다.
	server := rest.MustNewServer(c, rest.WithCors("example.com"))
	defer server.Stop()

	server.AddRoutes(
		[]rest.Route{
			{
				Method: http.MethodPost,
				Path:   "/test",
				Handler: func(w http.ResponseWriter, r *http.Request) {
					logx.Info("Request received")
					httpx.OkJsonCtx(r.Context(), w, "1")
				},
			},
		},
	)

	fmt.Printf("Starting server at %s:%d...\n", c.Host, c.Port)
	server.Start()
}
```

## 복잡한 CORS 설정을 커스터마이징하려면?

`rest.WithCustomCors`를 사용해 응답 헤더를 직접 설정합니다.

예제 코드:

```go
package main

import (
	"fmt"
	"net/http"

	"github.com/zeromicro/go-zero/core/conf"
	"github.com/zeromicro/go-zero/core/logx"
	"github.com/zeromicro/go-zero/rest"
	"github.com/zeromicro/go-zero/rest/httpx"
)

func main() {
	var c rest.RestConf
	conf.MustLoad("config.yaml", &c)

	server := rest.MustNewServer(c, rest.WithCustomCors(func(header http.Header) {
		header.Set("Access-Control-Allow-Origin", "*")
		header.Add("Access-Control-Allow-Headers", "UserHeader1, UserHeader2")
		header.Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH")
		header.Set("Access-Control-Expose-Headers", "Content-Length, Content-Type")
	}, nil, "*"))
	defer server.Stop()

	server.AddRoutes(
		[]rest.Route{
			{
				Method: http.MethodPost,
				Path:   "/test",
				Handler: func(w http.ResponseWriter, r *http.Request) {
					logx.Info("Request received")
					httpx.OkJsonCtx(r.Context(), w, "1")
				},
			},
		},
	)

	fmt.Printf("Starting server at %s:%d...\n", c.Host, c.Port)
	server.Start()
}
```
