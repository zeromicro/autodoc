---
title: Rate Limiter
description: Control request throughput in go-zero services with token bucket rate limiting.
sidebar:
  order: 2
---

# Rate Limiter

go-zero provides two complementary rate limiting primitives backed by Redis: a **token-bucket** limiter for smooth throughput control, and a **period limiter** for fixed-window quotas.

## Token Bucket Limiter

The token bucket refills at a constant rate and allows short bursts. It uses Redis as a shared state store, so it works correctly across multiple instances.

```go
import (
    "github.com/zeromicro/go-zero/core/limit"
    "github.com/zeromicro/go-zero/core/stores/redis"
)

rds := redis.MustNewRedis(redis.RedisConf{Host: "127.0.0.1:6379", Type: "node"})
// rate=100 req/s, burst=200 tokens
limiter := limit.NewTokenLimiter(100, 200, rds, "api:orders")

if limiter.Allow() {
    // process request
} else {
    httpx.Error(w, errorx.NewCodeError(429, "too many requests"))
}
```

### With Context

Use `AllowCtx` to honour request cancellations:

```go
if limiter.AllowCtx(r.Context()) {
    // proceed
}
```

### Batch Consumption

Consume N tokens in one call — useful for bulk or weighted operations:

```go
n := len(req.Items)  // charge by item count
if limiter.AllowN(time.Now(), n) {
    // process batch
}
```

## Period Limiter (Fixed Window)

Enforces a maximum number of requests inside a rolling time window. Useful for per-user quotas (e.g. "1000 API calls per hour").

```go
// 1000 requests per hour per user
limiter := limit.NewPeriodLimit(3600, 1000, rds, "user:rate:")

code, err := limiter.Take("user:42")
switch code {
case limit.Allowed:
    // under quota — proceed normally
case limit.HitQuota:
    // this is the last allowed request in the window; warn the caller
case limit.OverQuota:
    // quota exceeded — return 429
}
```

### With Context

```go
code, err := limiter.TakeCtx(r.Context(), "user:42")
```

## HTTP Middleware

To limit all routes served by a `rest.Server`, register a middleware:

```go
func RateLimitMiddleware(limiter *limit.TokenLimiter) rest.Middleware {
    return func(next http.HandlerFunc) http.HandlerFunc {
        return func(w http.ResponseWriter, r *http.Request) {
            if !limiter.AllowCtx(r.Context()) {
                http.Error(w, "too many requests", http.StatusTooManyRequests)
                return
            }
            next(w, r)
        }
    }
}

// Register globally
server.Use(RateLimitMiddleware(limiter))
```

Or scope it to specific route groups in the `.api` file:

```text
@server (
    middleware: RateLimit
)
service user-api {
    @handler CreateUser
    post /users (CreateUserReq) returns (CreateUserResp)
}
```

## Per-User Limiting

Combine the period limiter with the authenticated user ID for per-user quotas:

```go
func (l *CreateOrderLogic) CreateOrder(req *types.CreateOrderReq) (*types.CreateOrderResp, error) {
    key := fmt.Sprintf("user:%d", req.UserId)
    code, err := l.svcCtx.RateLimiter.Take(key)
    if err != nil || code == limit.OverQuota {
        return nil, errorx.NewCodeError(429, "rate limit exceeded")
    }
    // ... business logic
}
```

## Redis Cluster

Both limiters accept a `*redis.Redis` client. For Redis Cluster:

```go
rds := redis.MustNewRedis(redis.RedisConf{
    Host: "127.0.0.1:7000",
    Type: "cluster",
})
```

## Configuration

Store the limiter config in `etc/app.yaml` and bind it to `ServiceContext`:

```yaml title="etc/app.yaml"
RateLimit:
  Rate:  100    # tokens per second
  Burst: 200
  Redis:
    Host: 127.0.0.1:6379
    Type: node
```

```go title="internal/svc/servicecontext.go"
svcCtx.RateLimiter = limit.NewTokenLimiter(
    c.RateLimit.Rate,
    c.RateLimit.Burst,
    redis.MustNewRedis(c.RateLimit.Redis),
    "api:global",
)
```

## Best Practices

- **Key granularity** — use per-route and per-user keys, not a single global key, to avoid one user starving others.
- **Burst sizing** — set `burst` to ~2× `rate` to absorb small spikes without rejecting legitimate traffic.
- **Fallback** — when Redis is unavailable, `TokenLimiter` falls back to an in-process limiter automatically so the service keeps running.
- **Observe** — increment a Prometheus counter for `OverQuota` events to alert on sustained rate-limit pressure.
