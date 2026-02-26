---
title: CORS Configuration
description: Configure Cross-Origin Resource Sharing in go-zero HTTP services.
sidebar:
  order: 2
---


`go-zero` offers three ways to handle CORS:
- `rest.WithCors(origin ...string)`
    - Sets the allowed origins for cross-origin requests.
- `rest.WithCorsHeaders(headers ...string)`
    - Sets the allowed headers for cross-origin requests.
- `rest.WithCustomCors(middlewareFn func(header http.Header), notAllowedFn func(http.ResponseWriter),
  origin ...string)`
    - Configures complex CORS requirements.

## How to Customize CORS Headers?

You can add allowed headers for cross-origin requests using `go-zero`'s `rest.WithCorsHeaders(headers ...string)`.

Example code:

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

> go-zero version: >= v1.7.1

## How to Customize CORS Domains?

You can set allowed origins for cross-origin requests using go-zero’s rest.WithCors(origins ...string).

Example code:

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

	// Set allowed origins for cross-origin requests
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

## How to Customize Complex CORS Settings?

You can configure complex CORS behavior using go-zero’s rest.WithCustomCors.

Example code:

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