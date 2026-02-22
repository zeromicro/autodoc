---
title: 中间件
description: 在 go-zero 中编写和挂载中间件。
sidebar:
  order: 3
---

# 中间件

中间件用于封装横切逻辑，如日志、鉴权、限流。

```go
func AuthMiddleware(next http.HandlerFunc) http.HandlerFunc {
  return func(w http.ResponseWriter, r *http.Request) {
    next(w, r)
  }
}
```
