---
title: CORS 配置
description: 在 go-zero HTTP 服务中配置跨域资源共享。
sidebar:
  order: 2
---


`go-zero` 针对跨域提供了三种用法：
- `rest.WithCors(origin ...string)`
  - 设置允许跨域的域名
- `rest.WithCorsHeaders(headers ...string)`
  - 设置允许跨域的 `header`
- `rest.WithCustomCors(middlewareFn func(header http.Header), notAllowedFn func(http.ResponseWriter),
  origin ...string)`
  - 设置复杂的跨域需求

## 如何自定义跨域 `header`？

可以通过 `go-zero` 的 `rest.WithCorsHeaders(headers ...string)` 增加允许跨域的 `header`。

示例代码如下：

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
					logx.Info("请求进来了")
					httpx.OkJsonCtx(r.Context(), w, "1")
				},
			},
		},
	)

	fmt.Printf("Starting server at %s:%d...\n", c.Host, c.Port)
	server.Start()
}
```

> go-zero 版本：>= v1.7.1

## 如何自定义跨域 `domain`?

可以通过 `go-zero` 的 `rest.WithCors(origins ...string)` 设置允许跨域的域名。

示例代码如下：

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

	// 设置允许跨域的域名
	server := rest.MustNewServer(c, rest.WithCors("example.com"))
	defer server.Stop()

	server.AddRoutes(
		[]rest.Route{
			{
				Method: http.MethodPost,
				Path:   "/test",
				Handler: func(w http.ResponseWriter, r *http.Request) {
					logx.Info("请求进来了")
					httpx.OkJsonCtx(r.Context(), w, "1")
				},
			},
		},
	)

	fmt.Printf("Starting server at %s:%d...\n", c.Host, c.Port)
	server.Start()
}
```

## 如何自定义复杂的跨域设置?

可以通过 `go-zero` 的 `rest.WithCustomCors` 设置复杂的跨域行为。

示例代码如下：

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
					logx.Info("请求进来了")
					httpx.OkJsonCtx(r.Context(), w, "1")
				},
			},
		},
	)

	fmt.Printf("Starting server at %s:%d...\n", c.Host, c.Port)
	server.Start()
}
```

### 自定义复杂的跨域设置示例

示例代码如下：

```go
package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"

	"github.com/zeromicro/go-zero/core/logx"
	"github.com/zeromicro/go-zero/core/conf"
	"github.com/zeromicro/go-zero/rest"
	"github.com/zeromicro/go-zero/rest/httpx"
)

var configFile = flag.String("f", "etc/core-api-dev.yaml", "the config file")

func main() {
	flag.Parse()

	var c config.Config
	conf.MustLoad(*configFile, &c)

	# 需要通过的域名，这里可以写多个域名 或者可以写 * 全部通过
	domains := []string{"*","http://127.0.0.1", "https://go-zero.dev", "http://localhost"}
	server := rest.MustNewServer(
		c.RestConf,
		rest.WithCors(domains...),
		rest.WithCustomCors(func(header http.Header) {
			# 这里写允许通过的header key 不区分大小写
			header.Add("Access-Control-Allow-Headers", "Content-Type,AccessToken,X-CSRF-Token,Authorization,Token,X-Token,X-User-Id,OS,Platform, Version")
			header.Set("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS,PATCH")
			header.Set("Access-Control-Expose-Headers", "Content-Length, Content-Type")
		}, nil, "*"),
	)

	defer server.Stop()

	ctx := svc.NewServiceContext(c)
	handler.RegisterHandlers(server, ctx)


	fmt.Printf("Starting admin_user-api server at %s:%d...\n", c.Host, c.Port)
	server.Start()
}

```
