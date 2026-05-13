---
title: 파일 서버
description: go-zero REST 서비스에서 정적 파일을 제공하는 방법입니다.
sidebar:
  order: 3
---


## go-zero로 파일 서비스를 제공하려면?

`rest.WithFileServer(path, dir)` 옵션을 사용하면 `rest` 서비스에서 정적 파일을 제공할 수 있습니다.

예제 코드:

```go
package main

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest"
)

func main() {
    // 외부에 제공해야 하는 파일이 `html` 디렉터리에 있습니다.
    // 예를 들어 `index.html` 파일은 `/static/index.html` 경로로 접근할 수 있습니다.
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


지원 버전: go-zero >= v1.7.0
