---
title: Load Shedding
description: Automatically drop excess traffic when go-zero services are overloaded.
sidebar:
  order: 3
---

# Load Shedding

go-zero uses an **adaptive load shedder** based on CPU utilisation and in-flight request count. When the system is overloaded, new requests are rejected with HTTP 503 / gRPC UNAVAILABLE to protect existing in-flight work.

## How It Works

The shedder measures:
- **CPU usage** — if above threshold (default 90%), shedding activates
- **Pass rate** — the ratio of accepted to total requests in a window

Requests are shed probabilistically, allowing a controlled fraction through while the system recovers.

## HTTP Service

Load shedding is enabled by default. To configure the CPU threshold:

```yaml title="etc/app.yaml"
CpuThreshold: 900  # 90.0% — millicores * 10
```

Disable shedding (not recommended for production):

```go
server := rest.MustNewServer(c.RestConf, rest.WithNotAllowedHandler(...))
```

## gRPC Service

The `SheddingInterceptor` is registered automatically on every zrpc server.

## Custom Shedder

```go
import "github.com/zeromicro/go-zero/core/load"

shedder := load.NewAdaptiveShedder(
    load.WithCpuThreshold(800),  // 80%
)

promise, err := shedder.Allow()
if err != nil {
    // shed this request
    return nil, status.Error(codes.ResourceExhausted, "overloaded")
}
defer func() {
    if err != nil {
        promise.Fail()
    } else {
        promise.Pass()
    }
}()
```
