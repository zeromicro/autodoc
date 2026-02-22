---
title: Tracing
description: OpenTelemetry distributed tracing in go-zero services.
sidebar:
  order: 3
---

# Tracing

go-zero uses OpenTelemetry for distributed tracing, automatically creating spans for every HTTP request and gRPC call.

## Configuration

```yaml title="etc/app.yaml"
Telemetry:
  Name: order-api
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0          # 0.0–1.0; use 0.1 in production
  Batcher: jaeger        # "jaeger" | "zipkin" | "otlpgrpc" | "otlphttp"
```

## What Is Traced Automatically

- Every inbound HTTP request → span with URL, method, status code
- Every outbound zrpc call → child span with service/method
- SQL queries (via `sqlx`) → child span with query string

## Custom Spans

```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
)

func (l *OrderLogic) processPayment(amount int64) error {
    tracer := otel.Tracer("order-service")
    _, span := tracer.Start(l.ctx, "process-payment")
    defer span.End()

    span.SetAttributes(
        attribute.Int64("amount", amount),
        attribute.String("currency", "USD"),
    )

    if err := chargeCard(amount); err != nil {
        span.RecordError(err)
        return err
    }
    return nil
}
```

## Backends

| Backend | Batcher value | Notes |
|---------|--------------|-------|
| Jaeger | `jaeger` | All-in-one image available |
| Zipkin | `zipkin` | Lightweight alternative |
| OTLP gRPC | `otlpgrpc` | OpenTelemetry Collector |
| OTLP HTTP | `otlphttp` | OpenTelemetry Collector |
