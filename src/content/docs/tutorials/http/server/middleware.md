---
title: Middleware
description: Add custom and built-in middleware to go-zero HTTP services, server-wide or per-route.
sidebar:
  order: 3

---

Middleware in go-zero intercepts requests before they reach a handler, enabling cross-cutting logic such as authentication, logging, rate limiting, and tracing.

## Custom Middleware

### Server-Wide

Use `server.Use()` to apply a middleware to every route.

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

### Per-Route via API Spec

Declare a `middleware` in your `.api` file to scope it to specific routes.

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

```go title="internal/svc/servicecontext.go"
func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:      c,
        CheckHeader: middleware.NewCheckHeaderMiddleware().Handle,
    }
}
```

## Built-In Middleware

go-zero enables a comprehensive set of middleware by default, all configurable via `MiddlewaresConf`.

| Middleware | Purpose | Default |
|---|---|---|
| `TraceHandler` | OpenTelemetry distributed tracing | `true` |
| `LogHandler` | Structured HTTP access log | `true` |
| `PrometheusHandler` | Prometheus metrics | `true` |
| `RecoverHandler` | Recover from panics | `true` |
| `BreakerHandler` | Circuit breaker | `true` |
| `SheddingHandler` | Load shedding | `true` |
| `TimeoutHandler` | Request timeout enforcement | `true` |
| `MaxConnsHandler` | Max concurrent connection limit | `true` |
| `MaxBytesHandler` | Request body size limit | `true` |
| `GunzipHandler` | Gzip decompression | `true` |
| `AuthorizeHandler` | JWT authorization (when configured) | — |

### Disabling Built-In Middleware

```yaml title="etc/config.yaml"
Name: my-api
Middlewares:
  Metrics: false
  Log: false
  Prometheus: false
```

```go
type MiddlewaresConf struct {
    Trace      bool `json:",default=true"`
    Log        bool `json:",default=true"`
    Prometheus bool `json:",default=true"`
    MaxConns   bool `json:",default=true"`
    Breaker    bool `json:",default=true"`
    Shedding   bool `json:",default=true"`
    Timeout    bool `json:",default=true"`
    Recover    bool `json:",default=true"`
    Metrics    bool `json:",default=true"`
    MaxBytes   bool `json:",default=true"`
    Gunzip     bool `json:",default=true"`
}
```

### TraceHandler

Integrates OpenTelemetry. To export traces to Jaeger:

```yaml title="etc/config.yaml"
Telemetry:
  Name: my-service
  Endpoint: http://127.0.0.1:14268/api/traces
  Batcher: jaeger
  Sampler: 1.0
```

Spans include `http.host`, `http.method`, `http.route`, and `http.status_code` by default.

### LogHandler

Every request emits a structured JSON access log:

```json
{
  "@timestamp": "2024-01-01T10:00:00.000+08:00",
  "content": "[HTTP] 200 - GET /hello - 127.0.0.1:51499",
  "duration": "1.2ms",
  "level": "info"
}
```

### PrometheusHandler

Two metrics are exported:

| Metric | Type | Labels |
|---|---|---|
| `http_server_requests_duration_ms` | Histogram (buckets: 5,10,25,50,100,250,500,1000ms) | `path` |
| `http_server_requests_code_total` | Counter | `path`, `code` |

### MaxConnsHandler

Limits concurrent HTTP connections. Returns `503 Service Unavailable` when exceeded. Default is 10,000.
