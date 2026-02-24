---
title: 链路追踪
description: 为 go-zero 微服务添加分布式链路追踪。
sidebar:
  order: 4

---

# 分布式链路追踪

go-zero 内置 OpenTelemetry SDK，开箱即支持分布式链路追踪、跨服务 span 传播和 Prometheus 指标采集——无需手动埋点。

## 第一步：启动 Jaeger

```bash
docker run -d --name jaeger \
  -p 5775:5775/udp -p 6831:6831/udp -p 6832:6832/udp \
  -p 5778:5778 -p 16686:16686 -p 14268:14268 \
  jaegertracing/all-in-one:latest
```

Jaeger UI：http://localhost:16686

## 第二步：配置服务

```yaml title="etc/user-api.yaml"
Telemetry:
  Name: user-api
  Endpoint: http://localhost:14268/api/traces
  Sampler: 1.0      # 1.0 = 全量采样
  Batcher: jaeger   # 协议：jaeger | otlp
```

```yaml title="etc/user-rpc.yaml"
Telemetry:
  Name: user-rpc
  Endpoint: http://localhost:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```

go-zero 在首次请求时自动注册追踪器，无需任何代码改动。

## 第三步：验证链路

发起 HTTP 请求后，打开 Jaeger UI 并查看 `user-api` 服务。一条完整的跨服务链路应如下所示：

```
user-api: POST /api/user/login  [12 ms]
  └─ user-rpc: UserService/Login  [8 ms]
       └─ MySQL: SELECT users  [3 ms]
```

## 第四步：添加自定义 Span

在 go-zero 服务中可以添加任意自定义 span：

```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
)

func (l *LoginLogic) Login(req *types.LoginReq) (*types.LoginResp, error) {
    // 开始自定义 span
    tracer := otel.Tracer("user-api")
    ctx, span := tracer.Start(l.ctx, "validate-credentials")
    defer span.End()

    // 为 span 添加属性
    span.SetAttributes(
        attribute.String("user.email", req.Email),
        attribute.String("auth.method", "password"),
    )

    // 执行业务逻辑
    if err := l.validatePassword(ctx, req); err != nil {
        span.RecordError(err)
        return nil, err
    }
    // ...
}
```

## 第五步：使用 OTLP 导出至 Grafana Tempo

```yaml title="etc/app.yaml"
Telemetry:
  Name: user-api
  Endpoint: http://tempo:4318/v1/traces
  Sampler: 1.0
  Batcher: otlp    # OTLP HTTP 协议
```

使用 OpenTelemetry Collector 代理时，可同时输出到多个后端：

```yaml title="otel-collector.yaml"
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true
  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [jaeger, otlp/tempo]
```

## 第六步：日志关联 Trace ID

go-zero 自动将 `trace_id` 和 `span_id` 注入结构化日志输出：

```json
{
  "level": "info",
  "ts": "2024-01-15T10:30:45Z",
  "msg": "user login",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "user_id": 12345
}
```

在 Grafana 中可使用 trace_id 在 Tempo 与 Loki 日志之间一键跳转。

## 延伸阅读

- [负载均衡](./load-balancing) — 了解请求如何在多实例间分发
- [架构概览](../../concepts/architecture) — Observability 流水线全貌
