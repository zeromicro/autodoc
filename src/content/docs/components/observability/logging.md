---
title: Logging
description: Structured, level-based logging in go-zero with logx.
sidebar:
  order: 1
---

# Logging

go-zero's `logx` package provides structured, level-based, high-performance logging with zero allocations on the hot path.

## Basic Usage

```go
import "github.com/zeromicro/go-zero/core/logx"

logx.Info("server started")
logx.Infof("listening on port %d", port)
logx.Errorw("database error", logx.Field("err", err), logx.Field("query", sql))
```

## Log Levels

```go
logx.Debug("verbose debug info")   // hidden by default
logx.Info("normal operation")
logx.Slow("query took 200ms")      // slow threshold logging
logx.Error("something failed")
logx.Severe("critical condition")  // also writes to stderr
```

## Configuration

```yaml title="etc/app.yaml"
Log:
  ServiceName: order-api
  Mode: file          # "console" | "file" | "volume"
  Path: /var/log/order-api
  Level: info         # "debug" | "info" | "error"
  Compress: false
  KeepDays: 7
  Encoding: json      # "json" | "plain"
```

## Context Logging

Attach request-scoped fields automatically:

```go
func (l *OrderLogic) CreateOrder(req *types.OrderReq) (*types.OrderResp, error) {
    l.Logger.Infow("creating order",
        logx.Field("userId", req.UserId),
        logx.Field("amount", req.Amount),
    )
    ...
}
```

## Disable in Tests

```go
func TestMain(m *testing.M) {
    logx.Disable()
    os.Exit(m.Run())
}
```
