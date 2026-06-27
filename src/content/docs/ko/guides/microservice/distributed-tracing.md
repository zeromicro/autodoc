---
title: 분산 추적
description: go-zero의 분산 추적에 대해 설명합니다.
sidebar:
  order: 4

---


:::note
:::

## 1단계: 실행 Jaeger Locally

```bash
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
```

Jaeger UI at **http://localhost:16686**.

## 2단계: 설정 Your Service

```yaml title="etc/order-api.yaml"
Name: order-api
Host: 0.0.0.0
Port: 8888

Telemetry:
  Name: order-api            # Jaeger 예시입니다
  Endpoint: localhost:4317    # OTLP gRPC
  Sampler: 1.0               # 1.0 = 100% sampling; 0.1 = 10%
  Batcher: otlpgrpc
```


## 3단계: 확인

```bash
# 시작합니다
go run order.go -f etc/order-api.yaml

# Make 예시입니다
curl http://localhost:8888/order/1

# Open, Jaeger, UI 예시입니다
```

You will see 추적 사용하여:
-  root `HTTP GET /order/1` span
- Child spans 위한 any downstream RPC calls
- Child spans 위한 SQL queries (경우 사용하여 `sqlx`)
- Child spans 위한 Redis calls

## 4단계: 추적 전반에 서비스


```yaml title="etc/user-rpc.yaml"
Name: user.rpc
ListenOn: 0.0.0.0:8081

Telemetry:
  Name: user.rpc
  Endpoint: localhost:4317
  Sampler: 1.0
  Batcher: otlpgrpc
```

 cross-service 추적 looks like:

```
order-api  [200ms] ─────────────────────────────────────────────────────────
  HTTP GET /order/1  [200ms]
    user.rpc/GetUser  [15ms]
      sqlx.FindOne  [8ms]
    order.rpc/GetOrder [40ms]
      redis.Get  [2ms]
      sqlx.FindOne  [12ms]
```

## 5단계: 추가 사용자 정의 span

위한 additional detail inside your 비즈니스 로직:

```go title="internal/logic/getorderlogic.go"
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
)

func (l *GetOrderLogic) GetOrder(req *types.GetOrderReq) (*types.GetOrderResp, error) {
    tracer := otel.Tracer("order-logic")
    ctx, span := tracer.Start(l.ctx, "validate-inventory")
    defer span.End()

    // Annotate 예시입니다
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

## 사용하여 Grafana Tempo (OTLP)

```yaml
Telemetry:
  Name: order-api
  Endpoint: http://tempo:4318   # OTLP HTTP
  Sampler: 1.0
  Batcher: otlphttp
```

또는 gRPC:

```yaml
Telemetry:
  Name: order-api
  Endpoint: tempo:4317          # OTLP gRPC (no http:// prefix)
  Sampler: 1.0
  Batcher: otlpgrpc
```

## 사용하여 OpenTelemetry Collector


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

Point your 서비스 로 Collector:

```yaml
Telemetry:
  Endpoint: http://otel-collector:4318
  Batcher: otlphttp
```

## 로그 Correlation


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


## Further 읽기

- [부하 분산](../../components/observability/tracing/#backends) — how 요청 are distributed 전반에 instances
- [아키텍처 개요](../../components/observability/tracing/#migrating-from-jaeger-batcher) — 관측 가능성 파이프라인 개요
