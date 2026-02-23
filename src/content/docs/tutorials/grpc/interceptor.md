---
title: gRPC Interceptors
description: Add server-side and client-side middleware to go-zero gRPC services.
sidebar:
  order: 3
---

# gRPC Interceptors

Interceptors are the gRPC equivalent of HTTP middleware. They run before and after each RPC call and can modify context, validate credentials, record metrics, or short-circuit requests.

## Server-Side Unary Interceptor

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

## Server-Side Streaming Interceptor

```go
func loggingStreamInterceptor(srv any, ss grpc.ServerStream,
    info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
    logx.Infof("stream started: %s", info.FullMethod)
    err := handler(srv, ss)
    if err != nil {
        logx.Errorf("stream error: %s — %v", info.FullMethod, err)
    }
    return err
}

server.AddStreamInterceptors(loggingStreamInterceptor)
```

## Client-Side Unary Interceptor

Inject tokens or propagate headers on every outgoing RPC:

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

## Client-Side Streaming Interceptor

```go
conn, _ := zrpc.NewClient(c.GreeterRpc,
    zrpc.WithStreamClientInterceptor(func(ctx context.Context, desc *grpc.StreamDesc,
        cc *grpc.ClientConn, method string, streamer grpc.Streamer,
        opts ...grpc.CallOption) (grpc.ClientStream, error) {
        ctx = metadata.AppendToOutgoingContext(ctx, "request-id", uuid.New().String())
        return streamer(ctx, desc, cc, method, opts...)
    }),
)
```

## Chaining Multiple Interceptors

Pass multiple interceptors to `AddUnaryInterceptors`; they execute in order:

```go
server.AddUnaryInterceptors(
    authInterceptor,      // 1st: reject unauthenticated requests
    rateLimitInterceptor, // 2nd: enforce per-user quota
    loggingInterceptor,   // 3rd: record method + latency
)
```

go-zero's built-in interceptors are prepended before your custom ones, so circuit breaking, Prometheus, and tracing are always innermost.

## Forwarding Metadata Between Services

Extract headers from an incoming gRPC context and attach them to a downstream call:

```go
func forwardMetadataInterceptor(ctx context.Context, req any,
    info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (any, error) {
    incomingMd, _ := metadata.FromIncomingContext(ctx)
    // forward specific headers to any RPC calls made inside handler
    outgoingCtx := metadata.NewOutgoingContext(ctx, metadata.Join(
        incomingMd,
        metadata.Pairs("x-request-id", incomingMd.Get("x-request-id")...),
    ))
    return handler(outgoingCtx, req)
}
```

## Logging Interceptor

```go
func loggingInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler) (any, error) {
    start := time.Now()
    resp, err := handler(ctx, req)
    logx.WithContext(ctx).Infow("rpc call",
        logx.Field("method", info.FullMethod),
        logx.Field("duration", time.Since(start).String()),
        logx.Field("error", err),
    )
    return resp, err
}
```

## Built-In Interceptors

go-zero registers these automatically on every `zrpc.Server` and `zrpc.Client` — no configuration needed:

| Interceptor | What it does |
|------------|-------------|
| `RecoverInterceptor` | Converts panics to gRPC `Internal` errors |
| `PrometheusInterceptor` | Records RPC duration and error-rate metrics |
| `TracingInterceptor` | Creates OpenTelemetry spans, propagates trace context |
| `BreakerInterceptor` | Opens circuit when error ratio exceeds threshold |
| `SheddingInterceptor` | Drops requests when CPU load is critical |
| `TimeoutInterceptor` | Enforces per-RPC deadline from server config |
