---
title: Middleware
description: Add request and response interceptors to go-zero HTTP services.
sidebar:
  order: 2
---

# Middleware

go-zero supports middleware at two levels: **server-wide** and **per-route** via the API spec.

## Server-Wide Middleware

```go title="main.go"
func LogMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        log.Printf("-> %s %s", r.Method, r.URL.Path)
        next(w, r)
    }
}

server := rest.MustNewServer(c.RestConf)
server.Use(LogMiddleware)
```

## Per-Route Middleware via API Spec

```text
@server (
    middleware: CheckHeader
)
service user-api {
    @handler CreateUser
    post /users (CreateUserReq) returns (CreateUserResp)
}
```

goctl generates a stub in `internal/middleware/`:

```go title="internal/middleware/checkheadermiddleware.go"
func (m *CheckHeaderMiddleware) Handle(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        if r.Header.Get("X-App-Version") == "" {
            httpx.Error(w, errors.New("missing X-App-Version header"))
            return
        }
        next(w, r)
    }
}
```

Register in `ServiceContext`:

```go
func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:      c,
        CheckHeader: middleware.NewCheckHeaderMiddleware().Handle,
    }
}
```

## Built-In Middleware

| Middleware | Purpose |
|-----------|---------|
| `RecoverHandler` | Recover from panics |
| `PrometheusHandler` | Prometheus metrics |
| `TracingHandler` | OpenTelemetry tracing |
| `MaxBytesHandler` | Limit request body size |
| `TimeoutHandler` | Per-request deadline |
