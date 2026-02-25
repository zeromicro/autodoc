---
title: Architecture
description: A deep-dive into go-zero's layered architecture, request lifecycle, middleware execution, and observability pipeline — with Mermaid diagrams.
sidebar:
  order: 2

---


go-zero is a cloud-native microservices framework built around a layered design that separates concerns while keeping each layer thin and replaceable.

## 1. System Overview

```mermaid
graph TB
  subgraph Client
    B[Browser / Mobile App]
  end

  subgraph API Gateway Layer
    G[go-zero API Service<br/>REST / HTTP]
  end

  subgraph RPC Layer
    U[User RPC<br/>gRPC / zrpc]
    O[Order RPC<br/>gRPC / zrpc]
    P[Product RPC<br/>gRPC / zrpc]
  end

  subgraph Infrastructure
    D[(MySQL)]
    R[(Redis)]
    Q[Kafka / RabbitMQ]
    E[etcd<br/>Service Registry]
  end

  subgraph Observability
    L[Log Collector]
    M[Prometheus]
    T[Jaeger / Zipkin]
  end

  B --> G
  G --> U
  G --> O
  G --> P
  U --> D
  U --> R
  O --> Q
  U & O & P --> E
  G & U & O & P --> L
  G & U & O & P --> M
  G & U & O & P --> T
```

## 2. HTTP Request Lifecycle

Every incoming HTTP request flows through a fixed pipeline before reaching your business logic:

```mermaid
sequenceDiagram
  participant C as Client
  participant R as Router
  participant TH as TimeoutHandler
  participant SH as SheddingHandler
  participant RH as RateLimitHandler
  participant MW as Your Middleware
  participant H as Handler
  participant L as Logic

  C->>R: HTTP Request
  R->>TH: match route
  TH->>SH: start deadline timer
  SH->>RH: check CPU load
  RH->>MW: check token bucket
  MW->>H: custom middleware
  H->>L: parse & validate request
  L-->>H: domain result
  H-->>C: JSON response
```

**What each layer does:**

| Layer | Component | Purpose |
|---|---|---|
| Timeout | `TimeoutHandler` | Enforce per-request deadline (config: `Timeout`) |
| Load shedding | `SheddingHandler` | Reject requests when CPU > threshold |
| Rate limiting | `RateLimitHandler` | Token-bucket rate limiter per route |
| Middleware | Your code | Auth, logging, CORS, etc. |
| Handler | Generated | Unmarshal request → call Logic |
| Logic | Your code | Business rules, DB/RPC calls |

## 3. Middleware Chain Execution Order

```mermaid
flowchart LR
  subgraph "Server-Wide (rest.Use)"
    A1[RecoverHandler] --> A2[PrometheusHandler] --> A3[TracingHandler]
  end

  subgraph "Per-Route (@server middleware)"
    B1[Auth] --> B2[AccessLog] --> B3[Custom...]
  end

  subgraph "Built-In Safety"
    C1[TimeoutHandler] --> C2[SheddingHandler] --> C3[RateLimitHandler]
  end

  A3 --> B1
  B3 --> C1
  C3 --> Handler
```

Server-wide middleware is registered via `server.Use(...)` and runs for every request. Per-route middleware is declared in the `.api` file's `@server` block and generated into `ServiceContext`. Built-in safety handlers always run last before your handler code.

## 4. API Gateway → RPC Wiring

goctl generates the full wiring between the HTTP layer and RPC clients:

```mermaid
flowchart LR
  subgraph "API Service"
    R[Router] --> H[Handler]
    H --> L[Logic]
    L --> SC[ServiceContext]
  end

  subgraph "ServiceContext"
    SC --> UC[UserRpc client]
    SC --> OC[OrderRpc client]
  end

  subgraph "zrpc Client"
    UC --> LB[P2C Load Balancer]
    OC --> LB
    LB --> ED[etcd Discovery]
  end

  subgraph "RPC Services"
    ED --> US[user-rpc :8081]
    ED --> OS[order-rpc :8082]
  end
```

`ServiceContext` is the dependency injection container. It holds all RPC clients, DB connections, cache references, and config. Both handler and logic layers share it via a pointer.

## 5. Resilience: Rate Limiting & Circuit Breaking

```mermaid
flowchart TD
  Req[Incoming Request] --> RateLimiter{Token Bucket<br/>has capacity?}
  RateLimiter -- yes --> Breaker{Circuit<br/>Breaker open?}
  RateLimiter -- no --> Reject429[429 Too Many Requests]
  Breaker -- open --> Reject503[503 Service Unavailable]
  Breaker -- closed/half-open --> Backend[Call RPC / DB]
  Backend -- success --> UpdateBreaker[Close breaker, release token]
  Backend -- error / timeout --> RecordFailure[Record failure, maybe open breaker]
```

go-zero's circuit breaker uses a **sliding-window** failure counter. The breaker opens when the error ratio in the past 10 seconds exceeds the configured threshold (default: 50%). In half-open state it lets one probe request through.

**Configuration:**

```yaml
# Automatically applied to every zrpc call and every outbound HTTP call
# No explicit config needed — go-zero enables it by default
```

## 6. Observability Pipeline

go-zero instruments every layer automatically:

```mermaid
flowchart LR
  subgraph "Your Service"
    H[Handler] --> L[Logic] --> D[DB / RPC]
  end

  subgraph "Auto-instrumented"
    H -- "access log (json)" --> LOG[Log Collector<br/>ELK / Loki]
    H -- "http_request_duration_ms" --> PROM[Prometheus<br/>+ Grafana]
    H -- "span + trace ID" --> TRACE[Jaeger / Zipkin]
  end

  L -- "sql_duration_ms, rpc_duration_ms" --> PROM
  D -- "child spans" --> TRACE
```

**Enabling:**

```yaml title="etc/app.yaml"
# Structured logging (always on)
Log:
  ServiceName: order-api
  Mode: file          # console | file
  Level: info
  Encoding: json

# Metrics
Prometheus:
  Host: 0.0.0.0
  Port: 9101
  Path: /metrics

# Distributed tracing
Telemetry:
  Name: order-api
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0        # 1.0 = 100% sampling
  Batcher: jaeger
```

All logs carry a `trace_id` and `span_id` field that correlate with Jaeger traces — no manual instrumentation required.

## Next Steps

- [Design Principles](./design-principles) — how go-zero enforces these layers
- [Distributed Tracing tutorial](../guides/microservice/distributed-tracing) — hands-on Jaeger setup
- [Circuit Breaker component](../components/resilience/circuit-breaker) — configuration reference
