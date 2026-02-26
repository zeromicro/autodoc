---
title: File Server
description: Serve static files from a go-zero HTTP service.
sidebar:
  order: 3
---


## How to provide file services using go-zero?

You can add file service capabilities to a `restful` service through `go-zero` using `rest.WithFileServer(path, dir)`.

Here is an example code:

```go
package main

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest"
)

func main() {
    // There are files in the `html` directory that need to be provided externally,
    // for example, a file named `index.html`, which can be accessed via the path `/static/index.html`.
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

This is just an example and generally should not be used for production services. It may be considered when the production service is very simple, but it is not best practice. Typically, file serving would be handled by `nginx` or cloud storage.

go-zero version: >= v1.7.0