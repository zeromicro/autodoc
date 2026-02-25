---
title: 文件服务器
description: 通过 go-zero HTTP 服务提供静态文件。
---


## 如何用 go-zero 服务同时提供文件服务？

可以通过 `go-zero` 的 `rest.WithFileServer(path, dir)` 来给 `restful` 服务增加文件服务能力。

示例代码如下：

```go
package main

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest"
)

func main() {
    // 在 `html` 目录下有需要对外提供的文件，比如有个文件 `index.html`，
    // 以 `/static/index.html` 这样的路径就可以访问该文件了。
	server := rest.MustNewServer(rest.RestConf{
		Host: "localhost",
		Port: 4000,
	}, rest.WithFileServer("/static", http.Dir("html")))
	defer server.Stop()

	server.AddRoute(rest.Route{
		Method:  http.MethodGet,
		Path:    "/hello",
		Handler: helloHandler,
	})

	server.Start()
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Hello, World!"))
}
```

这仅仅是个示例，一般不用做生产服务，或者当生产服务很简单的时候可以考虑使用，但不是最佳实践，一般会通过 `nginx` 或者云存储提供。

## 如何用 go-zero 服务部署 react 打包产物？

我们知道前端很多路由都是虚拟路由，并非像静态配置文件那样访问的每个路径都在文件中能一一匹配到，像 react-route
提供的路由，其实所有路由访问的页面都是基于 index.html 来渲染页面的，因此当我们部署服务后从 index
一层一层访问二级页面是没问题，但是每当直接从url地址打开二级页面或者刷新二级页面时，你会发现页面 404 了，这就需要我们在服务端做一些处理。在
not found handler 中将服务端不存在的路由转发到根路由 / 去。

部分关键目录信息树：

```bash
.
├── main.go
├── etc
├── internal
│   ├── config
│   ├── handler
│   ├── logic
│   ├── svc
│   └── types
└── public
    └── static
        ├── css
        ├── js
        └── media

13 directories

```

参考代码：

```go
const basename  = "/web" // 虚拟路由根路径

// public 为前端打包产物相对于 main 函数的路径
//go:embed public
var assets embed.FS

flag.Parse()
	var c config.Config
	conf.MustLoad(*configFile, &c)

	sub, _ := fs.Sub(assets, "public") // 读取对应目录下的内容，这里的public和上面embed目录（单目录，并非完整路径）对应
	//fs := http.Dir("public") // 如果不走 embed 形式，则用此方式 serve 前端目录，然后注释下一行代码即可。
	fs := http.FS(sub)
	fileServer := http.FileServer(fs)
	server := rest.MustNewServer(c.RestConf,
		rest.WithNotFoundHandler(&NotFoundHandler{// 自定义 NotFoundHandler，对虚拟路由做处理
			fs:         fs,
			fileServer: fileServer,
		}),
		rest.WithFileServer(basename, fs))
	defer server.Stop()

	ctx := svc.NewServiceContext(c)
	handler.RegisterHandlers(server, ctx)

	fmt.Printf("Starting server at %s:%d...\n", c.Host, c.Port)
	server.Start()
}

type NotFoundHandler struct {
	fs         http.FileSystem
	fileServer http.Handler
}

func (n NotFoundHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	filePath := strings.TrimPrefix(path.Clean(r.URL.Path), basename)
	if len(filePath) == 0 {
		filePath = basename
	}

	file, err := n.fs.Open(filePath)
	switch {
	case err == nil:
		n.fileServer.ServeHTTP(w, r)
		_ = file.Close()
		return
	case os.IsNotExist(err):
		r.URL.Path = "/" // all virtual routes in react app means visit index.html
		n.fileServer.ServeHTTP(w, r)
		return
	default:
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
}
```

> go-zero 版本：>= v1.7.0
