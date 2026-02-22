---
title: Components
description: Built-in go-zero components for resilience, caching, observability, and messaging.
sidebar:
  order: 1
---

# Components

go-zero ships a comprehensive set of production-ready components that you can drop into any service.

## Resilience

- [Circuit Breaker](./resilience/circuit-breaker.md) — Stop cascading failures
- [Rate Limiter](./resilience/rate-limiter.md) — Control request throughput
- [Load Shedding](./resilience/load-shedding.md) — Drop excess traffic under overload
- [Timeout](./resilience/timeout.md) — Enforce per-request deadlines

## Caching

- [Memory Cache](./cache/memory-cache.md) — In-process LRU/TTL cache
- [Redis Cache](./cache/redis-cache.md) — Distributed cache with read-through

## Observability

- [Logging](./observability/logging.md) — Structured, level-based logging
- [Metrics](./observability/metrics.md) — Prometheus integration
- [Tracing](./observability/tracing.md) — OpenTelemetry distributed tracing

## Messaging

- [Kafka](./queue/kafka.md) — Produce and consume Kafka messages
- [RabbitMQ](./queue/rabbitmq.md) — AMQP message queue integration
