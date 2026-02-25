---
title: RPC Service Configuration
description: Complete reference for go-zero gRPC (zrpc) service configuration.
sidebar:
  order: 3

---


All fields for `zrpc.RpcServerConf` and `zrpc.RpcClientConf`.

## Server Config

```yaml title="etc/service.yaml"
Name: my.rpc                  # service name (required)
ListenOn: 0.0.0.0:8080       # bind address:port (required)

# ── Service Discovery ────────────────────────────────────────────────────────
Etcd:
  Hosts:
    - 127.0.0.1:2379
  Key: my.rpc                 # discovery key

# ── TLS ─────────────────────────────────────────────────────────────────────
# CertFile: /path/to/cert.pem
# KeyFile:  /path/to/key.pem

# ── Timeouts ─────────────────────────────────────────────────────────────────
Timeout: 2000                 # server-side deadline ms

# ── CPU-based Load Shedding ──────────────────────────────────────────────────
CpuThreshold: 900

# ── Prometheus ───────────────────────────────────────────────────────────────
Prometheus:
  Host: 0.0.0.0
  Port: 9102
  Path: /metrics

# ── Telemetry ────────────────────────────────────────────────────────────────
Telemetry:
  Name: my.rpc
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```

## Client Config

```yaml
MyRpc:
  # Option 1: static endpoints
  Endpoints:
    - 127.0.0.1:8080

  # Option 2: etcd discovery
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: my.rpc

  Timeout: 2000               # client-side deadline ms
  KeepaliveTime: 20000        # keepalive ping interval ms

  # TLS (mutual)
  # App:
  #   CertFile: client.pem
  #   KeyFile:  client.key
  #   CaCert:   ca.pem
```
