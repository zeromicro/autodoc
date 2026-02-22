---
title: Rate Limiter
description: Control request throughput in go-zero services with token bucket rate limiting.
sidebar:
  order: 2
---

# Rate Limiter

go-zero provides a token-bucket rate limiter that works both in HTTP middleware and standalone.

## HTTP Service Configuration

```yaml title="etc/app.yaml"
MaxConns: 10000   # max concurrent connections
```

Add the rate-limit middleware in the API spec:

```text
@server (
    middleware: RateLimit
)
service api {
    @handler CreateOrder
    post /orders (OrderReq) returns (OrderResp)
}
```

## Standalone Rate Limiter

```go
import "github.com/zeromicro/go-zero/core/limit"

// Token bucket: 100 requests per second, burst of 200
limiter := limit.NewTokenLimiter(100, 200, store, "api:rate")

if limiter.Allow() {
    // process request
} else {
    httpx.Error(w, errorx.NewCodeError(429, "too many requests"))
}
```

## Period Limiter (Fixed Window)

```go
// 1000 requests per hour per user
limiter := limit.NewPeriodLimit(3600, 1000, store, "user:rate:")

code, err := limiter.Take("user:42")
switch code {
case limit.Allowed:
    // process
case limit.HitQuota:
    // last allowed request; warn user
case limit.OverQuota:
    // rejected
}
```
