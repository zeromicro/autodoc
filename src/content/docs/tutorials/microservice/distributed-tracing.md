---
title: Distributed Tracing
description: Trace requests across go-zero microservices with OpenTelemetry.
sidebar:
  order: 3
---

# Distributed Tracing

go-zero integrates OpenTelemetry and exports traces to Jaeger, Zipkin, or any OTLP endpoint.

## Configuration

```yaml title="etc/app.yaml"
Telemetry:
  Name: order-api
  Endpoint: http://jaeger-collector:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger   # or "zipkin", "otlpgrpc", "otlphttp"
```

No code changes needed — go-zero creates spans for every HTTP and gRPC request.

## Run Jaeger Locally

```bash
docker run -d --name jaeger \
  -p 16686:16686 -p 14268:14268 \
  jaegertracing/all-in-one:latest
```

Open `http://localhost:16686` to view traces.

## Custom Spans

```go
tracer := otel.Tracer("order-service")
ctx, span := tracer.Start(l.ctx, "validate-inventory")
defer span.End()

_, err := l.svcCtx.InventoryRpc.CheckStock(ctx, req)
```

## Propagation

go-zero propagates the W3C `traceparent` header across HTTP and gRPC boundaries automatically.
