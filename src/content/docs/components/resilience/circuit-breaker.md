---
title: Circuit Breaker
description: Prevent cascading failures in go-zero with automatic circuit breaking.
sidebar:
  order: 2

---


go-zero integrates a Google SRE-style circuit breaker into every RPC client and HTTP service automatically — no manual wiring required.

## How It Works

The breaker tracks the ratio of errors over a sliding window. When the error rate exceeds the threshold, the circuit **opens** and subsequent requests fail immediately (fast-fail) instead of waiting for a slow upstream. After a cooldown period a probe request is allowed — if it succeeds the breaker closes again.

| State | Condition | Behaviour |
|-------|-----------|-----------|
| **Closed** | Error rate below threshold | Normal operation; errors tracked |
| **Open** | Error rate above threshold | All requests rejected instantly |
| **Half-Open** | After cooldown expires | One probe request allowed |

The algorithm is based on [Google SRE's adaptive throttling](https://sre.google/sre-book/handling-overload/): requests rejected = max(0, (requests − K × accepts) / (requests + 1)) where K defaults to 1.5.

## Automatic Mode (RPC & HTTP)

No code needed — the breaker activates automatically for all `zrpc` calls and HTTP downstream requests:

```go
// Automatically protected by circuit breaker, P2C lb, and timeout
resp, err := l.svcCtx.OrderRpc.CreateOrder(l.ctx, req)
if err != nil {
    // During open state: err == breaker.ErrServiceUnavailable
    return nil, err
}
```

## Manual Usage

Use `breaker.NewBreaker()` to protect any external call (database, HTTP API, Redis, etc.):

```go
import "github.com/zeromicro/go-zero/core/breaker"

b := breaker.NewBreaker(breaker.WithName("payment-gateway"))

// Simple: counts all non-nil errors
err := b.Do(func() error {
    return callPaymentAPI(req)
})
```

### DoWithFallback

Provide a fallback when the circuit is open — for graceful degradation:

```go
err := b.DoWithFallback(
    func() error {
        return callPaymentAPI(req)
    },
    func(err error) error {
        // use cached result, queue for retry, or return a friendly error
        return serveCachedResult(req)
    },
)
```

### DoWithAcceptable

Fine-tune which errors count as failures. Useful when `ErrNotFound` or `ErrUnauthorized` should not trip the breaker:

```go
err := b.DoWithAcceptable(
    func() error {
        return callPaymentAPI(req)
    },
    func(err error) bool {
        // return true = "this error is acceptable; don't count it against the breaker"
        return errors.Is(err, ErrNotFound) || errors.Is(err, ErrUnauthorized)
    },
)
```

### DoWithFallbackAcceptable

Combines fallback and custom error acceptance:

```go
err := b.DoWithFallbackAcceptable(fn, fallbackFn, acceptableFn)
```

## Configuration

The built-in breaker uses sensible defaults. Customise the name (used for logging and metrics labels):

```go
b := breaker.NewBreaker(breaker.WithName("stripe-api"))
```

The `zrpc` client creates one breaker per downstream service automatically, keyed by `etcd Key` or endpoint string.

## Prometheus Metrics

When Prometheus is enabled in config, the breaker exports:

| Metric | Description |
|--------|-------------|
| `breaker_total` | Total requests through the breaker |
| `breaker_pass` | Requests allowed through |
| `breaker_drop` | Requests dropped (circuit open) |

```yaml title="etc/app.yaml"
Prometheus:
  Host: 0.0.0.0
  Port: 9101
  Path: /metrics
```

## Best Practices

- **Name breakers** — give each breaker a unique name so metrics and logs distinguish between failure sources.
- **Don't suppress errors entirely** — the breaker needs accurate error feedback to calculate the error rate. Make sure `Do` callbacks return real errors, not shadowed ones.
- **Use `DoWithAcceptable` for validation errors** — 400-class errors are usually the caller's fault, not the downstream's. Excluding them gives the breaker a truer signal of downstream health.
- **Pair with timeouts** — a breaker prevents cascading failures, but you still need a deadline on each call so goroutines don't pile up behind a slow upstream.
