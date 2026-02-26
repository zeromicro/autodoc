---
title: Components
description: Built-in go-zero components for resilience, caching, observability, and messaging.
sidebar:
  order: 1
---


go-zero ships a comprehensive set of production-ready components that you can drop into any service.

## Resilience

- [Circuit Breaker](./resilience/circuit-breaker/) — Stop cascading failures
- [Rate Limiter](./resilience/rate-limiter/) — Sliding-window rate limiter
- [Period Limiter](./resilience/period-limiter/) — Redis-based period rate limiter
- [Token Limiter](./resilience/token-limiter/) — Token-bucket rate limiter
- [Load Shedding](./resilience/load-shedding/) — Drop excess traffic under overload
- [Timeout](./resilience/timeout/) — Enforce per-request deadlines

## Concurrency

- [fx](./concurrency/fx/) — Functional stream processing
- [MapReduce](./concurrency/mr/) — Parallel map-reduce
- [Limit](./concurrency/limit/) — Concurrency limiting via syncx

## Caching

- [Memory Cache](./cache/memory-cache/) — In-process LRU/TTL cache
- [Redis Cache](./cache/redis-cache/) — Distributed cache with read-through

## Logging

- [logx](./log/logx/) — Core structured logger
- [logc](./log/logc/) — Context-aware logging
- [Desensitization](./log/desensitization/) — Mask sensitive log fields

## Observability

- [Metrics](./observability/metrics/) — Prometheus integration
- [Tracing](./observability/tracing/) — OpenTelemetry distributed tracing
- [Profiling](./observability/profiling/) — Runtime profiling

## Messaging

- [Kafka](./queue/kafka/) — Produce and consume Kafka messages
- [RabbitMQ](./queue/rabbitmq/) — AMQP message queue integration
