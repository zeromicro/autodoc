---
title: 更新日志
description: go-zero 版本历史、破坏性变更与迁移说明。
sidebar:
  order: 6

---

完整的发布历史请查看 [GitHub releases 页面](https://github.com/zeromicro/go-zero/releases)。

## v1.7.x（当前版本）

- 要求 Go 1.21+
- OpenTelemetry SDK 更新至 v1.24
- `logx` 新增 `logx.WithContext`，自动关联链路追踪
- `goctl` model 现在支持 PostgreSQL `GENERATED ALWAYS AS IDENTITY`

## v1.6.x

- `zrpc` 客户端配置：`Endpoints` 列表替代已废弃的 `Target`
- Prometheus 指标重命名保持一致性：`http_server_*` 前缀
- `breaker` 包重构；新增 `NewBreaker` options 模式
- `kq`（Kafka 队列）通过 `segmentio/kafka-go` v0.4 支持 Kafka 3.x

## v1.5.x

- OpenTelemetry 替代 OpenTracing/Jaeger 客户端库
- `Telemetry` 配置块替代 `Jaeger` 块（迁移方式：重命名键名）
- `goctl` 模板引擎更新；自定义模板可能需要调整路径

## 迁移指南：v1.5 → v1.6

```yaml
# 之前（v1.5）
Jaeger:
  Endpoint: http://jaeger:14268/api/traces

# 之后（v1.6+）
Telemetry:
  Name: my-service
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```
