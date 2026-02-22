---
title: Circuit Breaker
description: Prevent cascading failures in go-zero with automatic circuit breaking.
sidebar:
  order: 1
---

# Circuit Breaker

go-zero integrates a Google SRE-style circuit breaker into every RPC client and HTTP service automatically — no manual wiring required.

## How It Works

The breaker tracks the ratio of errors over a sliding window. When the error rate exceeds a threshold, the circuit **opens** and requests fail immediately (fast-fail) instead of waiting for a slow upstream.

| State | Behaviour |
|-------|-----------|
| **Closed** | Normal operation, errors tracked |
| **Open** | Requests rejected immediately |
| **Half-Open** | Probe requests allowed; recovers or re-opens |

## Automatic Mode (RPC Clients)

The circuit breaker activates automatically for all zrpc calls — nothing to configure.

```go
// This call is automatically protected
resp, err := l.svcCtx.OrderRpc.CreateOrder(l.ctx, req)
if err != nil {
    // err may be breaker.ErrServiceUnavailable during open state
    return nil, err
}
```

## Manual Usage

```go
import "github.com/zeromicro/go-zero/core/breaker"

b := breaker.NewBreaker()

err := b.Do(func() error {
    return callExternalAPI()
})
// or with custom accept/reject functions:
err = b.DoWithAcceptable(func() error {
    return callExternalAPI()
}, func(err error) bool {
    // return true to not count this error against the breaker
    return errors.Is(err, ErrNotFound)
})
```

## Configuration

The built-in breaker uses sensible defaults. To tune:

```go
b := breaker.NewBreaker(breaker.WithName("payment-service"))
```

Metrics are exported to Prometheus automatically when Prometheus is enabled in config.
