---
title: Deployment FAQ
description: Common deployment questions for go-zero services.
sidebar:
  order: 4
---

# Deployment FAQ

## Service fails to start: `etcd connection refused`

Check that etcd is running and reachable from the service container:

```bash
# Test connectivity
nc -zv etcd-host 2379

# Check etcd health
etcdctl --endpoints=http://etcd-host:2379 endpoint health
```

In Kubernetes, use the etcd service DNS name, not `localhost`.

## `bind: address already in use`

Another process is listening on the same port. Find and stop it:

```bash
lsof -i :8888
kill -9 <PID>
```

In Kubernetes, ensure no two pods use the same `hostPort`.

## High memory usage after load spike

Check for goroutine leaks:

```bash
curl http://localhost:6060/debug/pprof/goroutine?debug=1
```

Enable pprof in your config:

```yaml
Log:
  Mode: console
# Add pprof route in main.go:
```

```go
import _ "net/http/pprof"
go http.ListenAndServe(":6060", nil)
```

## Requests time out under load

1. Check `MaxConns` — increase if connection pool is exhausted.
2. Check `Timeout` — too low for your workload.
3. Check downstream RPC timeouts.
4. Check CPU-based load shedding threshold (`CpuThreshold`).

```yaml
MaxConns: 50000
Timeout: 5000
CpuThreshold: 950
```

## How to do zero-downtime deployments?

Use Kubernetes rolling deployments with proper readiness probes:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
readinessProbe:
  httpGet: {path: /healthz, port: 8888}
  initialDelaySeconds: 5
  periodSeconds: 5
```
