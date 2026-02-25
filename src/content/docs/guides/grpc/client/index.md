---
title: gRPC Client
description: Call gRPC services from go-zero with service discovery, load balancing, circuit breaking, and timeout.
sidebar:
  order: 3

---


`zrpc.Client` is go-zero's gRPC client wrapper. It integrates **service discovery**, **P2C load balancing**, **circuit breaking**, and **OpenTelemetry tracing** automatically.

## Option A: Direct Connection (Dev / Testing)

```go title="internal/svc/servicecontext.go"
import (
    "github.com/zeromicro/go-zero/zrpc"
    "myservice/greeter"  // generated proto package
)

func NewServiceContext(c config.Config) *ServiceContext {
    conn, err := zrpc.NewClient(zrpc.RpcClientConf{
        Endpoints: []string{"localhost:8080"},
    })
    if err != nil {
        log.Fatal(err)
    }
    return &ServiceContext{
        Config:        c,
        GreeterClient: greeter.NewGreeterClient(conn.Conn()),
    }
}
```

## Option B: Service Discovery via etcd (Production)

```yaml title="etc/app.yaml"
GreeterRpc:
  Etcd:
    Hosts:
      - 127.0.0.1:2379
    Key: greeter.rpc
  Timeout: 2000       # request deadline in ms
  KeepaliveTime: 20000
```

```go title="internal/svc/servicecontext.go"
func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:        c,
        GreeterClient: greeter.NewGreeterClient(
            zrpc.MustNewClient(c.GreeterRpc).Conn(),
        ),
    }
}
```

`MustNewClient` panics on error — suitable for startup. Use `NewClient` if you want to handle the error yourself.

## Making a Call

```go title="internal/logic/hellologic.go"
func (l *HelloLogic) Hello(req *types.HelloReq) (*types.HelloResp, error) {
    resp, err := l.svcCtx.GreeterClient.SayHello(l.ctx, &greeter.SayHelloReq{
        Name: req.Name,
    })
    if err != nil {
        return nil, err
    }
    return &types.HelloResp{Message: resp.Message}, nil
}
```

The `l.ctx` carries the OpenTelemetry trace context, so the downstream RPC span is automatically linked to the parent HTTP span in Jaeger.

## Config Reference

```yaml
GreeterRpc:
  # Option 1: etcd discovery
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: greeter.rpc

  # Option 2: static
  Endpoints:
    - 127.0.0.1:8080

  Timeout: 2000           # client-side deadline (ms), 0 = no deadline
  KeepaliveTime: 20000    # gRPC keepalive ping interval (ms)

  # Mutual TLS
  # App:
  #   CertFile: client.pem
  #   KeyFile:  client.key
  #   CaCert:   ca.pem
```

## Error Handling

gRPC errors carry a status code. go-zero's circuit breaker records these:

```go
import "google.golang.org/grpc/status"

resp, err := l.svcCtx.GreeterClient.SayHello(l.ctx, req)
if err != nil {
    st, _ := status.FromError(err)
    switch st.Code() {
    case codes.NotFound:
        return nil, errorx.NewCodeError(404, "user not found")
    case codes.DeadlineExceeded:
        return nil, errorx.NewCodeError(504, "upstream timeout")
    default:
        return nil, err
    }
}
```

## Circuit Breaking

The circuit breaker is enabled by default. It opens when the error ratio over the last 10 seconds exceeds 50%, stopping requests from reaching the broken upstream:

```
Normal flow:   Request → RPC call → Response
Open breaker:  Request → 503 immediately (no RPC call made)
Half-open:     One probe request allowed through to check recovery
```

No configuration needed — it's automatic for every `zrpc.Client`.

## Adding Interceptors

Inject custom metadata (e.g. API token, user ID) into every outgoing call:

```go
conn, err := zrpc.NewClient(c.GreeterRpc,
    zrpc.WithUnaryClientInterceptor(func(
        ctx context.Context, method string,
        req, reply any, cc *grpc.ClientConn,
        invoker grpc.UnaryInvoker, opts ...grpc.CallOption,
    ) error {
        ctx = metadata.AppendToOutgoingContext(ctx,
            "x-request-id", requestIDFromCtx(ctx),
        )
        return invoker(ctx, method, req, reply, cc, opts...)
    }),
)
```

## Next Steps

- [gRPC Interceptors](../interceptor) — server-side and client-side interceptors in depth
- [Load Balancing](../../microservice/load-balancing) — how P2C routes across instances
