---
title: Components
description: Built-in go-zero components for resilience, caching, observability, and messaging.
sidebar:
  order: 1
---


go-zero ships a comprehensive set of production-ready components that you can drop into any service.

## Resilience

- [Circuit Breaker](./resilience/circuit-breaker.md) — Stop cascading failures
- [Rate Limiter](./resilience/rate-limiter.md) — Sliding-window rate limiter
- [Period Limiter](./resilience/period-limiter.md) — Redis-based period rate limiter
- [Token Limiter](./resilience/token-limiter.md) — Token-bucket rate limiter
- [Load Shedding](./resilience/load-shedding.md) — Drop excess traffic under overload
- [Timeout](./resilience/timeout.md) — Enforce per-request deadlines

## Concurrency

- [fx](./concurrency/fx.md) — Functional stream processing
- [MapReduce](./concurrency/mr.md) — Parallel map-reduce
- [Limit](./concurrency/limit.md) — Concurrency limiting via syncx

## Caching

- [Memory Cache](./cache/memory-cache.md) — In-process LRU/TTL cache
- [Redis Cache](./cache/redis-cache.md) — Distributed cache with read-through

## Logging

- [logx](./log/logx.md) — Core structured logger
- [logc](./log/logc.md) — Context-aware logging
- [Desensitization](./log/desensitization.md) — Mask sensitive log fields

## Observability

- [Metrics](./observability/metrics.md) — Prometheus integration
- [Tracing](./observability/tracing.md) — OpenTelemetry distributed tracing
- [Profiling](./observability/profiling.md) — Runtime profiling

## Messaging

- [Kafka](./queue/kafka.md) — Produce and consume Kafka messages
- [RabbitMQ](./queue/rabbitmq.md) — AMQP message queue integration
