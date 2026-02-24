---
title: Microservice System
description: A multi-service example demonstrating service discovery, RPC calls, and observability.
sidebar:
  order: 5

---

# Microservice System

This advanced example shows how multiple go-zero services collaborate using etcd for service discovery.

## Services Overview

```text
order-api  ──→  order-rpc  ──→  MySQL
               ↓
          inventory-rpc  ──→  Redis
               ↓
          payment-rpc    ──→  MySQL
```

## Prerequisites

- etcd running on `localhost:2379`
- MySQL and Redis available

## Service Configuration

Each service registers itself with etcd:

```yaml title="etc/order-rpc.yaml"
Name: order.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts:
    - 127.0.0.1:2379
  Key: order.rpc
```

## RPC Client Configuration

```yaml title="etc/order-api.yaml"
OrderRpc:
  Etcd:
    Hosts:
      - 127.0.0.1:2379
    Key: order.rpc
```

## Observability

Enable Prometheus metrics and Jaeger tracing:

```yaml
Telemetry:
  Name: order-api
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```

## Key Concepts Demonstrated

- Service discovery via etcd
- Multi-hop RPC call chains
- Distributed tracing across services
- Rate limiting and circuit breaking in action
