---
title: 追踪
description: 全链路追踪请求路径与耗时。
sidebar:
  order: 4

---


go-zero 基于 OpenTelemetry 实现分布式追踪。每个 HTTP 请求、zrpc 调用和 SQL 查询都会自动创建 span——常规链路无需任何手动埋点。

## 配置

```yaml title="etc/app.yaml"
Telemetry:
  Name: order-api             # 在追踪 UI 中显示的服务名称
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0                # 1.0 = 100% 采样；高流量生产环境建议 0.1
  Batcher: jaeger             # 详见下方后端列表
```

## 自动追踪覆盖范围

| 层 | span 包含信息 |
|----|--------------|
| 入站 HTTP 请求 | URL、方法、HTTP 状态码 |
| 出站 zrpc 调用 | gRPC 服务名 + 方法名 |
| SQL 查询（sqlx） | 查询语句、影响行数 |
| Redis 命令 | 命令名称、key 前缀 |

## 跨服务追踪传播

go-zero 使用 **W3C TraceContext** 标准（`traceparent` 请求头）在服务间传播追踪上下文。API 服务调用 RPC 服务时，trace ID 和 span ID 自动流转——整条调用链在 Jaeger 或 Zipkin 中呈现为单一 trace。

```
客户端 → [order-api: span A] → [order-rpc: span B（A 的子 span）] → DB: span C（B 的子 span）
```

RPC 服务端侧无需任何代码——gRPC 拦截器自动从入站 metadata 中提取上下文。

## 自定义 Span

在业务 logic 中添加应用级 span：

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
        attribute.String("currency", "CNY"),
        attribute.String("provider", "alipay"),
    )

    if err := chargeCard(ctx, amount); err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return err
    }
    return nil
}
```

## Trace ID 注入日志

同时配置 `logx` 和 `Telemetry` 时，go-zero 自动将 trace ID 和 span ID 注入每一条日志：

```json
{"level":"info","trace_id":"4bf92f3577b34da6a3ce929d0e0e4736","span_id":"00f067aa0ba902b7","msg":"订单已创建","orderId":"ord_123"}
```

可以从 Jaeger 的某个 trace span 直接跳转到该请求对应的日志行。

## 采样策略

| 策略 | 配置 | 适用场景 |
|------|------|---------|
| 全量采样 | `Sampler: 1.0` | 开发环境、预发布环境 |
| 10% 采样 | `Sampler: 0.1` | 高流量生产环境 |
| 低频采样 | `Sampler: 0.01` | 超高吞吐（>10k req/s） |

基于比例的采样器在 trace 根节点（API 网关）做决策，同一 trace 下所有下游 span 自动跟随包含或排除。

## 后端支持

| 后端 | `Batcher` 值 | Endpoint 格式 |
|------|-------------|--------------|
| Jaeger | `jaeger` | `http://jaeger:14268/api/traces` |
| Zipkin | `zipkin` | `http://zipkin:9411/api/v2/spans` |
| OTLP gRPC | `otlpgrpc` | `otel-collector:4317` |
| OTLP HTTP | `otlphttp` | `http://otel-collector:4318` |

### Jaeger 快速启动（Docker）

```bash
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 14268:14268 \
  jaegertracing/all-in-one:latest
# UI 访问：http://localhost:16686
```

### OpenTelemetry Collector

生产环境建议通过 OTel Collector 路由追踪数据，实现多后端分发：

```yaml title="etc/app.yaml"
Telemetry:
  Name: order-api
  Endpoint: otel-collector:4317
  Batcher: otlpgrpc
  Sampler: 0.1
```

## 关闭追踪

将 `Sampler` 设为 `0` 或移除整个 `Telemetry` 块即可完全关闭追踪开销。
