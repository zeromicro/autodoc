---
title: Distributed Tracing
description: Add distributed tracing to go-zero microservices.
sidebar:
  order: 4

---


go-zero integrates **OpenTelemetry** and emits spans for every HTTP request, gRPC call, SQL query, and Redis command automatically — no manual instrumentation needed for the common case.

go-zero supports several trace exporters (`otlpgrpc`, `otlphttp`, `zipkin`, `file`). See [Components > Tracing](../../components/observability/tracing/#backends) for the full backends table, sampling strategies, and migration notes.

:::note
The `jaeger` batcher was removed in go-zero v1.10.0. Use `otlpgrpc` or `otlphttp` instead — Jaeger 1.35+ natively supports OTLP. See [Migrating from Jaeger Batcher](../../components/observability/tracing/#migrating-from-jaeger-batcher).
:::

## Step 1: Run Jaeger Locally

```bash
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
```

Open the Jaeger UI at **http://localhost:16686**.

## Step 2: Configure Your Service

```yaml title="etc/order-api.yaml"
Name: order-api
Host: 0.0.0.0
Port: 8888

Telemetry:
  Name: order-api            # service name as it appears in Jaeger
  Endpoint: localhost:4317    # OTLP gRPC
  Sampler: 1.0               # 1.0 = 100% sampling; 0.1 = 10%
  Batcher: otlpgrpc
```

That's it — no code changes. go-zero reads this config and creates an OTel tracer at startup.

## Step 3: Verify

```bash
# Start your service
go run order.go -f etc/order-api.yaml

# Make a request
curl http://localhost:8888/order/1

# Open Jaeger UI, select "order-api" from the service dropdown
```

You will see a trace with:
- The root `HTTP GET /order/1` span
- Child spans for any downstream RPC calls
- Child spans for SQL queries (if using `sqlx`)
- Child spans for Redis calls

## Step 4: Trace Across Services

When your API service calls an RPC service, Jaeger shows the complete end-to-end trace automatically because go-zero propagates the `traceparent` header through every gRPC call.

```yaml title="etc/user-rpc.yaml"
Name: user.rpc
ListenOn: 0.0.0.0:8081

Telemetry:
  Name: user.rpc
  Endpoint: localhost:4317
  Sampler: 1.0
  Batcher: otlpgrpc
```

A cross-service trace looks like:

```
order-api  [200ms] ─────────────────────────────────────────────────────────
  HTTP GET /order/1  [200ms]
    user.rpc/GetUser  [15ms]
      sqlx.FindOne  [8ms]
    order.rpc/GetOrder [40ms]
      redis.Get  [2ms]
      sqlx.FindOne  [12ms]
```

## Step 5: Add Custom Spans

For additional detail inside your business logic:

```go title="internal/logic/getorderlogic.go"
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
)

func (l *GetOrderLogic) GetOrder(req *types.GetOrderReq) (*types.GetOrderResp, error) {
    tracer := otel.Tracer("order-logic")
    ctx, span := tracer.Start(l.ctx, "validate-inventory")
    defer span.End()

    // Annotate with business context
    span.SetAttributes(
        attribute.Int64("order.id", req.Id),
        attribute.String("order.region", req.Region),
    )

    if err := l.checkInventory(ctx, req.Id); err != nil {
        span.RecordError(err)
        return nil, err
    }

    return &types.GetOrderResp{ /* ... */ }, nil
}
```

## Using Grafana Tempo (OTLP)

```yaml
Telemetry:
  Name: order-api
  Endpoint: http://tempo:4318   # OTLP HTTP
  Sampler: 1.0
  Batcher: otlphttp
```

Or gRPC:

```yaml
Telemetry:
  Name: order-api
  Endpoint: tempo:4317          # OTLP gRPC (no http:// prefix)
  Sampler: 1.0
  Batcher: otlpgrpc
```

## Using OpenTelemetry Collector

The Collector lets you fan out traces to multiple backends:

```yaml title="otel-collector-config.yaml"
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318
      grpc:
        endpoint: 0.0.0.0:4317

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true
  prometheusremotewrite:
    endpoint: http://prometheus:9090/api/v1/write

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [jaeger]
```

Point your services to the Collector:

```yaml
Telemetry:
  Endpoint: http://otel-collector:4318
  Batcher: otlphttp
```

## Log Correlation

go-zero's structured JSON logger automatically injects `trace_id` and `span_id` into every log entry, enabling log–trace correlation in tools like Grafana / Loki:

```json
{
  "level": "info",
  "ts": "2026-02-22T10:01:05Z",
  "caller": "logic/getorderlogic.go:42",
  "msg": "order fetched",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7"
}
```

In Grafana you can jump from a trace span to the matching log entry using the `trace_id` field.

## Further Reading

- [Tracing Component Reference](../../components/observability/tracing/) — sampling strategies, backend comparison, Jaeger migration, custom spans API
- [Load Balancing](./load-balancing) — how requests are distributed across instances
- [Architecture Overview](../../concepts/architecture) — observability pipeline overview
