---
title: Logging
description: Structured, level-based logging in go-zero with logx.
sidebar:
  order: 1
---

# Logging

go-zero's `logx` package provides structured, level-based, zero-allocation JSON logging with automatic trace correlation.

## Basic Usage

```go
import "github.com/zeromicro/go-zero/core/logx"

logx.Info("server started")
logx.Infof("listening on port %d", port)
logx.Infow("order created",
    logx.Field("orderId", id),
    logx.Field("userId", userId),
    logx.Field("amount", amount),
)
logx.Errorw("database error", logx.Field("err", err), logx.Field("query", sql))
```

## Log Levels

```go
logx.Debug("verbose debug info")    // hidden unless Level is "debug"
logx.Info("normal operation")
logx.Slow("query took 200ms")       // logged at "slow" level; use for threshold warnings
logx.Error("something failed")
logx.Severe("critical condition")   // also writes to stderr
```

Level hierarchy (low → high): `debug < info < slow < error < severe`

## Configuration

```yaml title="etc/app.yaml"
Log:
  ServiceName: order-api
  Mode: file              # "console" | "file" | "volume"
  Path: /var/log/order-api
  Level: info             # "debug" | "info" | "error"
  Encoding: json          # "json" | "plain"
  Compress: true          # gzip rotated files
  KeepDays: 7             # delete logs older than N days
  StackCooldownMillis: 100
```

### Mode Reference

| Mode | Behaviour |
|------|-----------|
| `console` | Write to stdout — good for containers / local dev |
| `file` | Write to `<Path>/<ServiceName>.log` with daily rotation |
| `volume` | Write to mounted volume (same as `file` behaviour) |

## Context Logging

Use `logx.WithContext` to attach the current trace ID and span ID automatically:

```go
func (l *OrderLogic) CreateOrder(req *types.OrderReq) (*types.OrderResp, error) {
    // l.Logger is a logx.Logger pre-bound to l.ctx
    l.Logger.Infow("creating order",
        logx.Field("userId", req.UserId),
        logx.Field("amount", req.Amount),
    )
    // Output: {"level":"info","trace_id":"4bf92...","span_id":"00f06...","userId":42,"amount":100}
    return nil, nil
}
```

Outside a logic struct:

```go
logger := logx.WithContext(ctx)
logger.Infow("event", logx.Field("key", value))
```

## Log Sampling

High-throughput services can produce millions of log lines per second. Use sampling to keep a representative fraction without disk pressure:

```go
// Log at most 100 "cache miss" events per second
logx.WithContext(ctx).WithDuration(time.Since(start)).
    Sloww("slow query", logx.Field("sql", query))
```

Configure global sampling in code before server start:

```go
logx.SetLevel(logx.InfoLevel)
logx.DisableStat()      // disable periodic stat logging (CPU/memory)
```

## Custom Writer

Route logs to any `io.Writer` — useful for sending to Sentry, Loki, or a log aggregator:

```go
logx.SetWriter(logx.NewWriter(myWriter))
```

Combine with the default writer to fan out:

```go
type teeWriter struct {
    a, b io.Writer
}
func (t *teeWriter) Write(p []byte) (int, error) {
    t.a.Write(p)
    return t.b.Write(p)
}
logx.SetWriter(logx.NewWriter(&teeWriter{os.Stdout, sentryWriter}))
```

## Disable in Tests

Suppress all log output in unit tests:

```go
func TestMain(m *testing.M) {
    logx.Disable()
    os.Exit(m.Run())
}
```

## Structured Field Patterns

| Pattern | Code |
|---------|------|
| Error with stack | `logx.Field("err", err)` |
| Duration | `logx.Field("latency", time.Since(start))` |
| Slice | `logx.Field("ids", ids)` |
| Nested struct | `logx.Field("req", req)` (marshalled to JSON) |

## Slow Log Threshold

go-zero automatically logs requests that exceed the slow log threshold:

```yaml
Log:
  Level: info
# Requests exceeding Timeout are logged as "slow" automatically
Timeout: 3000
```
