---
title: 指标
description: go-zero 服务中的 Prometheus 指标采集。
sidebar:
  order: 3

---

go-zero 自动为 HTTP 和 gRPC 服务记录关键指标，并通过 Prometheus 抓取端点暴露。

## 启用

```yaml title="etc/app.yaml"
Prometheus:
  Host: 0.0.0.0
  Port: 9101
  Path: /metrics
```

## 自动指标

**HTTP 服务：**

| 指标名 | 说明 |
|--------|------|
| `http_server_requests_total` | 按路由和状态码统计的总请求数 |
| `http_server_duration_ms` | 请求耗时直方图 |
| `http_server_active_requests` | 正在处理的请求数（Gauge） |

**gRPC 服务：**

| 指标名 | 说明 |
|--------|------|
| `rpc_server_requests_total` | 按方法和状态码统计的 RPC 调用总数 |
| `rpc_server_duration_ms` | RPC 耗时直方图 |

## 自定义指标

```go
import "github.com/zeromicro/go-zero/core/metric"

// Counter
ordersTotal := metric.NewCounterVec(&metric.CounterVecOpts{
    Namespace: "order",
    Subsystem: "service",
    Name:      "created_total",
    Help:      "Total orders created",
    Labels:    []string{"status"},
})
ordersTotal.Inc("success")

// Histogram
latency := metric.NewHistogramVec(&metric.HistogramVecOpts{
    Namespace: "order",
    Name:      "payment_duration_ms",
    Help:      "Payment processing latency",
    Labels:    []string{"provider"},
    Buckets:   []float64{5, 10, 25, 50, 100, 250, 500, 1000},
})
latency.Observe(float64(elapsed.Milliseconds()), "stripe")
```

## Grafana

go-zero 在 Grafana 市场提供社区仪表盘 — 搜索 "go-zero" 即可找到。
