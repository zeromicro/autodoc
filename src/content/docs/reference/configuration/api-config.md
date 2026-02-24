---
title: API Service Configuration
description: Complete reference for go-zero HTTP (REST) service configuration.
sidebar:
  order: 2

---

# API Service Configuration

All fields for `rest.RestConf`, embedded as `RestConf` in your service config struct.

```yaml title="etc/service-api.yaml"
Name: my-api                  # service name (required)
Host: 0.0.0.0                 # bind address (default: 0.0.0.0)
Port: 8888                    # listen port (required)

# ── Limits ──────────────────────────────────────────────────────────────────
MaxConns: 10000               # max concurrent connections
MaxBytes: 1048576             # max request body bytes (default: 1MB)
Timeout: 3000                 # request timeout in ms (default: 3000)
CpuThreshold: 900             # CPU % * 10 for load shedding (default: 900 = 90%)

# ── TLS ─────────────────────────────────────────────────────────────────────
# CertFile: /path/to/cert.pem
# KeyFile:  /path/to/key.pem

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
  Mode: console               # console | file | volume
  Level: info                 # debug | info | error
  Encoding: json              # json | plain
  KeepDays: 7
  Compress: false

# ── Tracing ──────────────────────────────────────────────────────────────────
Telemetry:
  Name: my-api
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```
