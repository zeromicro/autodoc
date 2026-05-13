---
title: 메트릭
description: go-zero의 메트릭에 대해 설명합니다.
sidebar:
  order: 3

---


## 활성화

```yaml title="etc/app.yaml"
Prometheus:
  Host: 0.0.0.0
  Port: 9101
  Path: /metrics
```

## 자동 메트릭

**HTTP 서비스:**

| Metric | 설명 |
|--------|-------------|
| `http_server_requests_total` | Total 요청 통해 라우트과 상태 |
| `http_server_duration_ms` | Request duration histogram |
| `http_server_active_requests` | In-flight 요청 gauge |

**gRPC 서비스:**

| Metric | 설명 |
|--------|-------------|
| `rpc_server_requests_total` | Total RPC calls 통해 메서드과 code |
| `rpc_server_duration_ms` | RPC duration histogram |

## Custom 메트릭

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
