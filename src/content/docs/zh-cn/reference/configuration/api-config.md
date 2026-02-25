---
title: API 服务配置
description: go-zero HTTP（REST）服务的完整配置参考。
sidebar:
  order: 2

---

`rest.RestConf` 的所有字段，嵌入到你的服务配置结构体中作为 `RestConf`。

```yaml title="etc/service-api.yaml"
Name: my-api                  # 服务名称（必填）
Host: 0.0.0.0                 # 绑定地址（默认：0.0.0.0）
Port: 8888                    # 监听端口（必填）

# ── 限制 ──────────────────────────────────────────────────────────────────
MaxConns: 10000               # 最大并发连接数
MaxBytes: 1048576             # 最大请求体字节数（默认：1MB）
Timeout: 3000                 # 请求超时，毫秒（默认：3000）
CpuThreshold: 900             # CPU % * 10，用于负载卸除（默认：900 = 90%）

# ── TLS ─────────────────────────────────────────────────────────────────────
# CertFile: /path/to/cert.pem
# KeyFile:  /path/to/key.pem

# ── JWT ─────────────────────────────────────────────────────────────────────
Auth:
  AccessSecret: "your-secret"
  AccessExpire: 86400         # 秒

# ── Prometheus ───────────────────────────────────────────────────────────────
Prometheus:
  Host: 0.0.0.0
  Port: 9101
  Path: /metrics

# ── 日志 ──────────────────────────────────────────────────────────────────
Log:
  ServiceName: my-api
  Mode: console               # console | file | volume
  Level: info                 # debug | info | error
  Encoding: json              # json | plain
  KeepDays: 7
  Compress: false

# ── 链路追踪 ──────────────────────────────────────────────────────────────────
Telemetry:
  Name: my-api
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```
