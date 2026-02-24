---
title: Metrics
description: Prometheus metrics collection in go-zero services.
sidebar:
  order: 3

---

# Metrics

go-zero automatically records key metrics for HTTP and gRPC services and exposes them via a Prometheus scrape endpoint.

## Enable

```yaml title="etc/app.yaml"
Prometheus:
  Host: 0.0.0.0
  Port: 9101
  Path: /metrics
```

## Automatic Metrics

**HTTP service:**

| Metric | Description |
|--------|-------------|
| `http_server_requests_total` | Total requests by route and status |
| `http_server_duration_ms` | Request duration histogram |
| `http_server_active_requests` | In-flight requests gauge |

**gRPC service:**

| Metric | Description |
|--------|-------------|
| `rpc_server_requests_total` | Total RPC calls by method and code |
| `rpc_server_duration_ms` | RPC duration histogram |

## Custom Metrics

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

go-zero provides community dashboards on Grafana's marketplace — search for "go-zero".
