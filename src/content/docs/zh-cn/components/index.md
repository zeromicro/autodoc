---
title: 组件总览
description: 了解 go-zero 内置组件能力。
sidebar:
  order: 1
---


## 服务韧性

- [熔断器](./resilience/circuit-breaker/) — 阻止级联故障
- [滑动窗口限流](./resilience/rate-limiter/) — 滑动窗口限流器
- [周期限流](./resilience/period-limiter/) — 基于 Redis 的周期限流器
- [令牌桶限流](./resilience/token-limiter/) — 令牌桶限流器
- [负载削减](./resilience/load-shedding/) — 过载时自动丢弃请求
- [超时](./resilience/timeout/) — 强制请求级超时

## 并发工具

- [fx](./concurrency/fx/) — 函数式流处理
- [MapReduce](./concurrency/mr/) — 并行 map-reduce
- [Limit](./concurrency/limit/) — syncx 并发限制

## 缓存

- [内存缓存](./cache/memory-cache/) — 进程内 LRU/TTL 缓存
- [Redis 缓存](./cache/redis-cache/) — 分布式缓存

## 日志

- [logx](./log/logx/) — 核心结构化日志
- [logc](./log/logc/) — 上下文感知日志
- [脱敏](./log/desensitization/) — 屏蔽敏感字段

## 可观测性

- [指标](./observability/metrics/) — Prometheus 集成
- [链路追踪](./observability/tracing/) — OpenTelemetry 分布式追踪
- [性能剖析](./observability/profiling/) — 运行时 Profiling

## 消息队列

- [Kafka](./queue/kafka/) — Kafka 消息生产与消费
- [RabbitMQ](./queue/rabbitmq/) — AMQP 消息队列
