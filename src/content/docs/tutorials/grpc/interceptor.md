---
title: gRPC Interceptors
description: Add server-side and client-side middleware to go-zero gRPC services.
sidebar:
  order: 3
---

# gRPC Interceptors

Interceptors are the gRPC equivalent of HTTP middleware.

## Server Interceptor

```go
func authInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler) (any, error) {
    md, _ := metadata.FromIncomingContext(ctx)
    if len(md["token"]) == 0 {
        return nil, status.Error(codes.Unauthenticated, "missing token")
    }
    return handler(ctx, req)
}

server := zrpc.MustNewServer(c.RpcServerConf, func(grpcServer *grpc.Server) {
    greeter.RegisterGreeterServer(grpcServer, srv)
})
server.AddUnaryInterceptors(authInterceptor)
server.Start()
```

## Client Interceptor

```go
conn, _ := zrpc.NewClient(c.GreeterRpc,
    zrpc.WithUnaryClientInterceptor(func(ctx context.Context, method string,
        req, reply any, cc *grpc.ClientConn,
        invoker grpc.UnaryInvoker, opts ...grpc.CallOption) error {
        ctx = metadata.AppendToOutgoingContext(ctx, "token", getToken())
        return invoker(ctx, method, req, reply, cc, opts...)
    }),
)
```

## Built-In Interceptors

| Interceptor | What it does |
|------------|-------------|
| `RecoverInterceptor` | Converts panics to gRPC errors |
| `PrometheusInterceptor` | Records RPC duration metrics |
| `TracingInterceptor` | OpenTelemetry span creation |
| `BreakerInterceptor` | Circuit-breaker protection |
| `SheddingInterceptor` | Load-shedding under heavy traffic |
| `TimeoutInterceptor` | Per-RPC deadline enforcement |
