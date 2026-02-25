---
title: 组件总览
description: 了解 go-zero 内置组件能力。
sidebar:
  order: 1
---


## 服务韧性

- [熔断器](./resilience/circuit-breaker.md) — 阻止级联故障
- [滑动窗口限流](./resilience/rate-limiter.md) — 滑动窗口限流器
- [周期限流](./resilience/period-limiter.md) — 基于 Redis 的周期限流器
- [令牌桶限流](./resilience/token-limiter.md) — 令牌桶限流器
- [负载削减](./resilience/load-shedding.md) — 过载时自动丢弃请求
- [超时](./resilience/timeout.md) — 强制请求级超时

## 并发工具

- [fx](./concurrency/fx.md) — 函数式流处理
- [MapReduce](./concurrency/mr.md) — 并行 map-reduce
- [Limit](./concurrency/limit.md) — syncx 并发限制

## 缓存

- [内存缓存](./cache/memory-cache.md) — 进程内 LRU/TTL 缓存
- [Redis 缓存](./cache/redis-cache.md) — 分布式缓存

## 日志

- [logx](./log/logx.md) — 核心结构化日志
- [logc](./log/logc.md) — 上下文感知日志
- [脱敏](./log/desensitization.md) — 屏蔽敏感字段

## 可观测性

- [指标](./observability/metrics.md) — Prometheus 集成
- [链路追踪](./observability/tracing.md) — OpenTelemetry 分布式追踪
- [性能剖析](./observability/profiling.md) — 运行时 Profiling

## 消息队列

- [Kafka](./queue/kafka.md) — Kafka 消息生产与消费
- [RabbitMQ](./queue/rabbitmq.md) — AMQP 消息队列
