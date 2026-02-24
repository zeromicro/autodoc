---
title: Load Shedding
description: Automatically drop excess traffic when go-zero services are overloaded.
sidebar:
  order: 5

---

# Load Shedding

go-zero uses an **adaptive load shedder** based on CPU utilisation and in-flight request count. When the system is overloaded, new requests are rejected with HTTP 503 / gRPC UNAVAILABLE to protect existing in-flight work.

## How It Works

The shedder combines two signals to decide whether to accept a request:

1. **CPU usage** — sampled every 250 ms via `/proc/stat`. Shedding activates once CPU exceeds the configured threshold (default 90%).
2. **Pass rate** — the rolling ratio of completed requests to total attempted requests in the last sliding window. If the pass rate drops below a calculated floor, new arrivals are shed.

This double-gate ensures you never shed when the CPU is healthy, and always shed when it is saturated, regardless of the request volume.

## HTTP Service

Load shedding is **enabled by default** for every `rest.Server`. Configure the CPU threshold in your YAML:

```yaml title="etc/app.yaml"
CpuThreshold: 900  # 90% — unit is millicores × 10 (0-1000)
```

When a request is shed, the server responds with **HTTP 503 Service Unavailable** and a `X-Content-Type-Options: nosniff` header.

To add a custom handler for shed requests:

```go
server := rest.MustNewServer(c.RestConf,
    rest.WithUnauthorizedCallback(func(w http.ResponseWriter, r *http.Request, err error) {
        // custom 503 body
        httpx.WriteJson(w, http.StatusServiceUnavailable, map[string]string{
            "code": "OVERLOADED",
            "msg":  "service temporarily unavailable",
        })
    }),
)
```

## gRPC Service

The `SheddingInterceptor` is registered **automatically** on every `zrpc.Server`. Shed requests return `codes.ResourceExhausted` (`429`):

```go
// Automatically registered — no code changes needed.
// Shed requests get:
//   status.Error(codes.ResourceExhausted, "concurrent connections over threshold")
```

Callers using go-zero's gRPC client see `zrpc.ErrResourceExhausted` and can decide to retry with backoff or fallback.

## Custom Shedder

Use `load.NewAdaptiveShedder` when you need programmatic control — for example, to wrap a non-HTTP workload like a message consumer:

```go
import (
    "github.com/zeromicro/go-zero/core/load"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

shedder := load.NewAdaptiveShedder(
    load.WithCpuThreshold(800),        // activate at 80% CPU
    load.WithWindow(5*time.Second),    // sliding window size
    load.WithBuckets(50),              // window buckets (granularity)
)

func processMessage(msg Message) error {
    promise, err := shedder.Allow()
    if err != nil {
        // overloaded — drop the message or push back to queue
        metrics.Inc("messages.shed")
        return ErrOverloaded
    }

    procErr := handle(msg)

    // IMPORTANT: always call Pass or Fail
    if procErr != nil {
        promise.Fail()   // counts as failed — lowers pass rate
    } else {
        promise.Pass()   // counts as success
    }
    return procErr
}
```

:::caution[Always close the promise]
Every successful `Allow()` call **must** be followed by exactly one `promise.Pass()` or `promise.Fail()`. Leaking promises causes the pass rate to drift and may permanently activate or deactivate shedding.
:::

## Configuration Reference

| Option | Default | Description |
|--------|---------|-------------|
| `WithCpuThreshold(n)` | `900` | CPU threshold in millicores×10 (0–1000) |
| `WithWindow(d)` | `5s` | Sliding window duration |
| `WithBuckets(n)` | `50` | Number of buckets in window |

## Metrics

When Prometheus is enabled, the shedder exports:

| Metric | Type | Description |
|--------|------|-------------|
| `shedding_drops_total` | Counter | Total requests shed |
| `shedding_pass_total` | Counter | Total requests passed |
| `cpu_usage` | Gauge | Current CPU usage (0–1000) |

## Best Practices

- **Tune the threshold** based on your service's CPU profile. Stateless services can tolerate higher thresholds (900–950); CPU-intensive services should use 700–800.
- **Monitor `shedding_drops_total`** alongside error rate. A spike in drops usually indicates a traffic surge or a slow downstream dependency.
- **Combine with circuit breaker and rate limiter** for defence in depth: rate limiter caps steady-state load, circuit breaker stops calls to unhealthy dependencies, load shedder protects the process itself.
- Do **not** disable shedding in production unless you have an external quota enforcement layer.
