---
title: RPC 서비스 설정
description: go-zero의 RPC 서비스 설정에 대해 설명합니다.
sidebar:
  order: 4

---


모든 필드 위한 `zrpc.RpcServerConf`과 `zrpc.RpcClientConf`.

## 서버 설정

```yaml title="etc/service.yaml"
Name: my.rpc                  # 예시입니다
ListenOn: 0.0.0.0:8080       # 예시입니다

# Service, Discovery 예시입니다
Etcd:
  Hosts:
    - 127.0.0.1:2379
  Key: my.rpc                 # discovery key

# ── TLS ─────────────────────────────────────────────────────────────────────
# CertFile 예시입니다
# KeyFile 예시입니다

# ── Timeouts ─────────────────────────────────────────────────────────────────
Timeout: 2000                 # 예시입니다

# CPU, Load, Shedding 예시입니다
CpuThreshold: 900

# ── Prometheus ───────────────────────────────────────────────────────────────
Prometheus:
  Host: 0.0.0.0
  Port: 9102
  Path: /metrics

# ── Telemetry ────────────────────────────────────────────────────────────────
Telemetry:
  Name: my.rpc
  Endpoint: localhost:4317
  Sampler: 1.0
  Batcher: otlpgrpc
```

## 클라이언트 설정

```yaml
MyRpc:
  # Option 예시입니다
  Endpoints:
    - 127.0.0.1:8080

  # Option 예시입니다
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: my.rpc

  Timeout: 2000               # 예시입니다
  KeepaliveTime: 20000        # 예시입니다

  # TLS (mutual)
  # App:
  # CertFile 예시입니다
  # KeyFile 예시입니다
  #   CaCert:   ca.pem
```
