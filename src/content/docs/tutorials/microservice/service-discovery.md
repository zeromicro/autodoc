---
title: Service Discovery
description: Register and discover go-zero microservices using etcd or Kubernetes.
sidebar:
  order: 1
---

# Service Discovery

go-zero supports pluggable service discovery backends. etcd is the most common option.

## Register (Server Side)

```yaml title="etc/order-rpc.yaml"
Name: order.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts: [127.0.0.1:2379]
  Key: order.rpc
```

No code changes needed — go-zero registers at startup automatically.

## Discover (Client Side)

```yaml title="etc/api.yaml"
OrderRpc:
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: order.rpc
```

```go
orderClient := order.NewOrderClient(zrpc.MustNewClient(c.OrderRpc).Conn())
```

## Kubernetes DNS

```yaml
OrderRpc:
  Endpoints: [order-rpc-svc.default:8080]
```

## Direct Endpoints (Dev)

```yaml
OrderRpc:
  Endpoints: [127.0.0.1:8080]
```

## Health Checks

go-zero RPC servers implement the gRPC health check protocol automatically.

```yaml
livenessProbe:
  exec:
    command: ["/bin/grpc_health_probe", "-addr=:8080"]
  initialDelaySeconds: 5
```
