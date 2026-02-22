---
title: gRPC Client
description: Call gRPC services from go-zero with load balancing and circuit breaking.
sidebar:
  order: 2
---

# gRPC Client

go-zero's `zrpc.Client` integrates service discovery, load balancing, and circuit breaking automatically.

## Direct Connection

```go
conn, err := zrpc.NewClient(zrpc.RpcClientConf{
    Endpoints: []string{"localhost:8080"},
})
client := greeter.NewGreeterClient(conn.Conn())
```

## Via Service Discovery (etcd)

```yaml title="etc/app.yaml"
GreeterRpc:
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: greeter.rpc
```

```go title="internal/svc/servicecontext.go"
func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:     c,
        GreeterRpc: greeter.NewGreeterClient(
            zrpc.MustNewClient(c.GreeterRpc).Conn(),
        ),
    }
}
```

## Make a Call

```go
resp, err := l.svcCtx.GreeterRpc.SayHello(l.ctx, &greeter.SayHelloReq{Name: "world"})
```

## Timeout & Retry

```yaml
GreeterRpc:
  Timeout: 2000        # ms
  KeepaliveTime: 20000
```
