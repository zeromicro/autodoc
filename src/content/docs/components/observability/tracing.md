---
title: Tracing
description: OpenTelemetry distributed tracing in go-zero services.
sidebar:
  order: 3
---

# Tracing

go-zero uses OpenTelemetry for distributed tracing. Spans are created automatically for every inbound HTTP request, outbound zrpc call, and SQL query — no instrumentation code required for the happy path.

## Configuration

```yaml title="etc/app.yaml"
Telemetry:
  Name: order-api             # service name shown in the trace UI
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0                # 1.0 = 100% sampling; use 0.1 in high-traffic production
  Batcher: jaeger             # see Backends table below
```

## What Is Traced Automatically

| Layer | Span details |
|-------|-------------|
| Inbound HTTP request | URL, method, HTTP status code |
| Outbound zrpc call | gRPC service + method name |
| SQL queries (via `sqlx`) | query string, rows affected |
| Redis commands | command name, key prefix |

## Trace Propagation

go-zero propagates trace context between services using the **W3C TraceContext** standard (`traceparent` header). When an API service calls an RPC service, the trace ID and span ID flow automatically — the entire call chain appears as a single trace in Jaeger or Zipkin.

```
Client → [order-api: span A] → [order-rpc: span B (child of A)] → DB: span C (child of B)
```

No code is needed on the RPC server side — the gRPC interceptor extracts the context from incoming metadata automatically.

## Custom Spans

Add application-level spans inside your logic:

```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/codes"
)

func (l *OrderLogic) processPayment(amount int64) error {
    tracer := otel.Tracer("order-service")
    ctx, span := tracer.Start(l.ctx, "process-payment")
    defer span.End()

    span.SetAttributes(
        attribute.Int64("amount", amount),
        attribute.String("currency", "USD"),
        attribute.String("provider", "stripe"),
    )

    if err := chargeCard(ctx, amount); err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return err
    }
    return nil
}
```

## Trace ID in Logs

When both `logx` and `Telemetry` are configured, go-zero injects the trace ID and span ID into every log line automatically:

```json
{"level":"info","trace_id":"4bf92f3577b34da6a3ce929d0e0e4736","span_id":"00f067aa0ba902b7","msg":"order created","orderId":"ord_123"}
```

This means you can jump from a Jaeger trace span straight to the logs for that specific request.

## Sampling Strategies

| Strategy | Config | When to use |
|---|---|---|
| Always sample | `Sampler: 1.0` | Development, staging |
| 10% sample | `Sampler: 0.1` | High-traffic production |
| Head-based ratio | `Sampler: 0.01` | Very high throughput (>10k req/s) |

A ratio sampler makes the decision at the trace root (the API gateway). All downstream spans in the same trace are automatically included or excluded together.

## Backends

| Backend | `Batcher` value | Endpoint format |
|---------|----------------|-----------------|
| Jaeger | `jaeger` | `http://jaeger:14268/api/traces` |
| Zipkin | `zipkin` | `http://zipkin:9411/api/v2/spans` |
| OTLP gRPC | `otlpgrpc` | `otel-collector:4317` |
| OTLP HTTP | `otlphttp` | `http://otel-collector:4318` |

### Jaeger All-in-One (Docker)

```bash
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 14268:14268 \
  jaegertracing/all-in-one:latest
# UI: http://localhost:16686
```

### OpenTelemetry Collector

For production, route traces through the OTel Collector to fan out to multiple backends:

```yaml title="etc/app.yaml"
Telemetry:
  Name: order-api
  Endpoint: otel-collector:4317
  Batcher: otlpgrpc
  Sampler: 0.1
```

## Disable Tracing

Set `Sampler: 0` or remove the `Telemetry` block entirely to disable all tracing overhead.
