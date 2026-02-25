---
title: RPC 服务配置
description: go-zero gRPC（zrpc）服务的完整配置参考。
sidebar:
  order: 3

---

`zrpc.RpcServerConf` 和 `zrpc.RpcClientConf` 的所有字段。

## 服务端配置

```yaml title="etc/service.yaml"
Name: my.rpc                  # 服务名称（必填）
ListenOn: 0.0.0.0:8080       # 绑定地址:端口（必填）

# ── 服务发现 ────────────────────────────────────────────────────────
Etcd:
  Hosts:
    - 127.0.0.1:2379
  Key: my.rpc                 # 注册键名

# ── TLS ─────────────────────────────────────────────────────────────────────
# CertFile: /path/to/cert.pem
# KeyFile:  /path/to/key.pem

# ── 超时 ─────────────────────────────────────────────────────────────────
Timeout: 2000                 # 服务端 deadline，毫秒

# ── 基于 CPU 的负载卸除 ──────────────────────────────────────────────────
CpuThreshold: 900

# ── Prometheus ───────────────────────────────────────────────────────────────
Prometheus:
  Host: 0.0.0.0
  Port: 9102
  Path: /metrics

# ── 链路追踪 ────────────────────────────────────────────────────────────────
Telemetry:
  Name: my.rpc
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```

## 客户端配置

```yaml
MyRpc:
  # 方式一：静态端点
  Endpoints:
    - 127.0.0.1:8080

  # 方式二：etcd 服务发现
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: my.rpc

  Timeout: 2000               # 客户端 deadline，毫秒
  KeepaliveTime: 20000        # keepalive ping 间隔，毫秒

  # TLS（双向认证）
  # App:
  #   CertFile: client.pem
  #   KeyFile:  client.key
  #   CaCert:   ca.pem
```
