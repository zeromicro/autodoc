---
title: API 서비스 설정
description: go-zero의 API 서비스 설정에 대해 설명합니다.
sidebar:
  order: 3

---


모든 필드 위한 `rest.RestConf`, embedded 로서 `RestConf` 에서 your 서비스 설정 struct.

```yaml title="etc/service-api.yaml"
Name: my-api                  # 예시입니다
Host: 0.0.0.0                 # 예시입니다
Port: 8888                    # 예시입니다

# ── Limits ──────────────────────────────────────────────────────────────────
MaxConns: 10000               # 예시입니다
MaxBytes: 1048576             # 예시입니다
Timeout: 3000                 # 예시입니다
CpuThreshold: 900             # CPU 예시입니다

# ── TLS ─────────────────────────────────────────────────────────────────────
# CertFile 예시입니다
# KeyFile 예시입니다

# ── JWT ─────────────────────────────────────────────────────────────────────
Auth:
  AccessSecret: "your-secret"
  AccessExpire: 86400         # seconds

# ── Prometheus ───────────────────────────────────────────────────────────────
Prometheus:
  Host: 0.0.0.0
  Port: 9101
  Path: /metrics

# ── Logging ──────────────────────────────────────────────────────────────────
Log:
  ServiceName: my-api
  Mode: console               # 예시입니다
  Level: info                 # 예시입니다
  Encoding: json              # json | plain
  KeepDays: 7
  Compress: false

# ── Tracing ──────────────────────────────────────────────────────────────────
Telemetry:
  Name: my-api
  Endpoint: localhost:4317
  Sampler: 1.0
  Batcher: otlpgrpc
```
