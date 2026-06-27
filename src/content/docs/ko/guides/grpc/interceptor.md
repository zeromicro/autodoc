---
title: gRPC 인터셉터
description: go-zero의 gRPC 인터셉터에 대해 설명합니다.
sidebar:
  order: 5

---


## Server-Side Unary 인터셉터

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

## Server-Side Streaming 인터셉터

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

## Client-Side Unary 인터셉터

Inject tokens 또는 propagate 헤더 에서 모든 outgoing RPC:

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

## Client-Side Streaming 인터셉터

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

## Chaining Multiple 인터셉터

Pass multiple 인터셉터 로 `AddUnaryInterceptors`; they execute 에서 순서:

```go
server.AddUnaryInterceptors(
    authInterceptor,      // 1단계: 인증되지 않은 요청을 거부합니다
    rateLimitInterceptor, // 2단계: 사용자별 할당량을 적용합니다
    loggingInterceptor,   // 3단계: 메서드와 지연 시간을 기록합니다
)
```


## Forwarding Metadata 사이 서비스


```go
func forwardMetadataInterceptor(ctx context.Context, req any,
    info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (any, error) {
    incomingMd, _ := metadata.FromIncomingContext(ctx)
    // 핸들러 내부에서 만든 RPC 호출에 특정 헤더를 전달합니다
    outgoingCtx := metadata.NewOutgoingContext(ctx, metadata.Join(
        incomingMd,
        metadata.Pairs("x-request-id", incomingMd.Get("x-request-id")...),
    ))
    return handler(outgoingCtx, req)
}
```

## 로깅 인터셉터

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

## Built-In 인터셉터

go-zero registers these 자동으로 에서 모든 `zrpc.Server`과 `zrpc.Client` — 없음 설정 needed:

| 인터셉터 | What it does |
|------------|-------------|
| `RecoverInterceptor` | Converts panics 로 gRPC `Internal` 오류 |
| `PrometheusInterceptor` | Records RPC duration과 error-rate 메트릭 |
| `TracingInterceptor` | Creates OpenTelemetry spans, propagates 추적 컨텍스트 |
| `BreakerInterceptor` | Opens 서킷 때 오류 비율 exceeds 임계값 |
| `SheddingInterceptor` | Drops 요청 때 CPU 부하 is critical |
| `TimeoutInterceptor` | Enforces 별-RPC deadline 에서 서버 설정 |
