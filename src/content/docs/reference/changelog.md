---
title: Changelog
description: go-zero version history, breaking changes, and migration notes.
sidebar:
  order: 10
---

# Changelog

For the full release history see the [GitHub releases page](https://github.com/zeromicro/go-zero/releases).

## v1.7.x (current)

- Go 1.21+ required
- OpenTelemetry SDK updated to v1.24
- `logx` gains `logx.WithContext` for automatic trace correlation
- `goctl` model now supports PostgreSQL `GENERATED ALWAYS AS IDENTITY`

## v1.6.x

- `zrpc` client config: `Endpoints` list replaces deprecated `Target`
- Prometheus metrics renamed for consistency: `http_server_*` prefix
- `breaker` package refactored; `NewBreaker` options pattern added
- `kq` (Kafka queue) now supports Kafka 3.x via `segmentio/kafka-go` v0.4

## v1.5.x

- OpenTelemetry replaces OpenTracing/Jaeger client library
- `Telemetry` config block replaces `Jaeger` block (migration: rename keys)
- `goctl` template engine updated; custom templates may need path adjustments

## Migration: v1.5 → v1.6

```yaml
# Before (v1.5)
Jaeger:
  Endpoint: http://jaeger:14268/api/traces

# After (v1.6+)
Telemetry:
  Name: my-service
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```
