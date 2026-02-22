---
title: Load Balancing
description: Distribute RPC traffic across instances in go-zero with P2C balancing.
sidebar:
  order: 2
---

# Load Balancing

go-zero uses **P2C (Power of Two Choices)** with EWMA load estimation — statistically superior to round-robin under bursty traffic.

## How It Works

1. Randomly pick **two** candidate endpoints.
2. Send the request to whichever has the **lower EWMA load**.
3. Update load estimate after the response.

## Enable (Default)

P2C is active whenever service discovery is used — no extra configuration required.

```yaml
OrderRpc:
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: order.rpc
```

## Round-Robin (Static Endpoints)

```yaml
OrderRpc:
  Endpoints:
    - 127.0.0.1:8080
    - 127.0.0.1:8081
```

## Prometheus Metrics

| Metric | Description |
|--------|-------------|
| `rpc_client_requests_total` | Total requests per target |
| `rpc_client_duration_ms` | Request latency histogram |

```yaml
Prometheus:
  Host: 0.0.0.0
  Port: 9101
  Path: /metrics
```
