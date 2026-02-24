---
title: Service Discovery
description: Register and discover services in go-zero microservices.
sidebar:
  order: 2

---

# Service Discovery

go-zero supports pluggable service discovery backends. Every RPC server registers itself automatically at startup; every RPC client watches the registry and picks healthy instances with P2C load balancing.

## etcd (Recommended for Production)

### Server Registration

Add the `Etcd` block to the RPC server config — no code changes needed:

```yaml title="etc/order-rpc.yaml"
Name: order.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts:
    - 127.0.0.1:2379
  Key: order.rpc         # discovery key — clients use this exact string
```

go-zero calls `etcd.Put(key, address)` at startup and `etcd.Delete` on graceful shutdown, with a lease so stale entries expire automatically if the process crashes.

### Client Discovery

Point the client config at the same etcd cluster and key:

```yaml title="etc/user-api.yaml"
OrderRpc:
  Etcd:
    Hosts:
      - 127.0.0.1:2379
    Key: order.rpc
  Timeout: 2000
```

```go title="internal/svc/servicecontext.go"
orderConn := zrpc.MustNewClient(c.OrderRpc)
svc.OrderRpc = order.NewOrderClient(orderConn.Conn())
```

### etcd Cluster

For high availability use three or five nodes:

```yaml
Etcd:
  Hosts:
    - etcd1.infra:2379
    - etcd2.infra:2379
    - etcd3.infra:2379
  Key: order.rpc
```

## Kubernetes DNS

When running inside Kubernetes, replace etcd with a headless Service DNS name:

```yaml
OrderRpc:
  Target: dns:///order-rpc-svc.default.svc.cluster.local:8080
```

Or use a list of pod endpoints directly (useful with StatefulSets):

```yaml
OrderRpc:
  Endpoints:
    - order-rpc-0.order-rpc-svc.default:8080
    - order-rpc-1.order-rpc-svc.default:8080
```

## Static Endpoints (Dev / CI)

For local development or integration tests, skip etcd entirely:

```yaml
OrderRpc:
  Endpoints:
    - 127.0.0.1:8080
```

## Service Key Conventions

| Convention | Example | Notes |
|---|---|---|
| `<name>.rpc` | `order.rpc` | Standard; matches the `Name` field |
| `<env>/<name>.rpc` | `prod/order.rpc` | Multi-environment shared etcd |
| `<ns>.<name>.rpc` | `payment.order.rpc` | Domain namespacing |

Use the same string in the server's `Etcd.Key` and the client's `Etcd.Key`.

## Health Checks

go-zero RPC servers implement the [gRPC health check protocol](https://github.com/grpc/grpc/blob/master/doc/health-checking.md) automatically. Kubernetes probes work out of the box:

```yaml title="k8s/order-rpc.yaml"
livenessProbe:
  exec:
    command: ["/bin/grpc_health_probe", "-addr=:8080"]
  initialDelaySeconds: 5
  periodSeconds: 10
readinessProbe:
  exec:
    command: ["/bin/grpc_health_probe", "-addr=:8080"]
  initialDelaySeconds: 3
  periodSeconds: 5
```

## Load Balancing

The client uses **P2C (pick-of-two-choices)** with EWMA latency by default. No configuration required — it selects the least-loaded among two randomly chosen instances on every call.

To verify which instance handled a request, enable debug logging or check the trace span's `peer.address` attribute.

## Graceful Scaling

When a new instance starts and registers with etcd, the client discovers it within the lease TTL (default 10 s). When an instance shuts down gracefully (`SIGTERM`), it deregisters before accepting no new connections, ensuring zero dropped requests during rolling deploys.
