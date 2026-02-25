---
title: Timeout
description: Enforce per-request deadlines in go-zero HTTP and gRPC services.
sidebar:
  order: 4

---


go-zero enforces request timeouts at multiple layers to prevent slow upstreams from exhausting goroutine pools.

## HTTP Service Timeout

```yaml title="etc/app.yaml"
Timeout: 3000  # milliseconds (default: 3000)
```

Requests exceeding this duration receive HTTP 408 automatically.

## gRPC Server Timeout

```yaml title="etc/rpc.yaml"
Timeout: 2000  # milliseconds
```

## Client-Side Timeout

Pass a context with deadline:

```go
ctx, cancel := context.WithTimeout(l.ctx, 2*time.Second)
defer cancel()

resp, err := l.svcCtx.OrderRpc.CreateOrder(ctx, req)
```

go-zero's `TimeoutInterceptor` propagates the deadline from the incoming request to all downstream RPC calls automatically.

## Per-Route Timeout (HTTP)

```go
server.AddRoute(rest.Route{
    Method:  http.MethodPost,
    Path:    "/slow-endpoint",
    Handler: myHandler,
}, rest.WithTimeout(10*time.Second))
```

## Timeout vs Context Cancellation

| Scenario | Behaviour |
|----------|-----------|
| Client disconnects | Context cancelled, upstream goroutine exits |
| Timeout exceeded | 408 returned; goroutine keeps running until completion |
| Both | Context cancelled first |
