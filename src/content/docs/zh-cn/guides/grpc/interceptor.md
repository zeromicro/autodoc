---
title: gRPC 拦截器
description: 为 gRPC 服务添加服务端和客户端拦截器。
sidebar:
  order: 5

---


拦截器是 gRPC 中实现跨请求逻辑的关键机制，等价于 HTTP 中间件。每次 RPC 调用前后都会执行拦截器，可用于鉴权、记录指标或修改请求上下文。

## 服务端一元拦截器

```go
func authInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler) (any, error) {
    md, _ := metadata.FromIncomingContext(ctx)
    if len(md["token"]) == 0 {
        return nil, status.Error(codes.Unauthenticated, "缺少 token")
    }
    return handler(ctx, req)
}

server := zrpc.MustNewServer(c.RpcServerConf, func(grpcServer *grpc.Server) {
    greeter.RegisterGreeterServer(grpcServer, srv)
})
server.AddUnaryInterceptors(authInterceptor)
server.Start()
```

## 服务端流式拦截器

```go
func loggingStreamInterceptor(srv any, ss grpc.ServerStream,
    info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
    logx.Infof("流式调用开始: %s", info.FullMethod)
    err := handler(srv, ss)
    if err != nil {
        logx.Errorf("流式调用错误: %s — %v", info.FullMethod, err)
    }
    return err
}

server.AddStreamInterceptors(loggingStreamInterceptor)
```

## 客户端一元拦截器

在每次对外 RPC 请求中注入 Token 或传递请求头：

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

## 客户端流式拦截器

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

## 链式注册多个拦截器

向 `AddUnaryInterceptors` 传入多个拦截器，按顺序依次执行：

```go
server.AddUnaryInterceptors(
    authInterceptor,      // 第 1 步：拒绝未认证请求
    rateLimitInterceptor, // 第 2 步：执行用户级限流
    loggingInterceptor,   // 第 3 步：记录方法名与耗时
)
```

go-zero 内置拦截器会在自定义拦截器之前注入，确保熔断、Prometheus 和追踪始终在最内层执行。

## 跨服务透传元数据

将上游 gRPC 请求的 metadata 提取后，附加到对下游的调用：

```go
func forwardMetadataInterceptor(ctx context.Context, req any,
    info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (any, error) {
    incomingMd, _ := metadata.FromIncomingContext(ctx)
    outgoingCtx := metadata.NewOutgoingContext(ctx, metadata.Join(
        incomingMd,
        metadata.Pairs("x-request-id", incomingMd.Get("x-request-id")...),
    ))
    return handler(outgoingCtx, req)
}
```

## 日志拦截器

```go
func loggingInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler) (any, error) {
    start := time.Now()
    resp, err := handler(ctx, req)
    logx.WithContext(ctx).Infow("rpc 调用",
        logx.Field("method", info.FullMethod),
        logx.Field("duration", time.Since(start).String()),
        logx.Field("error", err),
    )
    return resp, err
}
```

## 内置拦截器

go-zero 在每个 `zrpc.Server` 和 `zrpc.Client` 上自动注册以下拦截器，无需额外配置：

| 拦截器 | 功能 |
|--------|------|
| `RecoverInterceptor` | 将 panic 转换为 gRPC `Internal` 错误 |
| `PrometheusInterceptor` | 记录 RPC 耗时与错误率指标 |
| `TracingInterceptor` | 创建 OpenTelemetry span，传播 trace context |
| `BreakerInterceptor` | 错误率超阈值时打开熔断器 |
| `SheddingInterceptor` | CPU 负载过高时主动降载 |
| `TimeoutInterceptor` | 根据服务端配置执行每次 RPC 的超时限制 |
