---
title: gRPC 客户端
description: 通过 go-zero 调用 gRPC 服务，含服务发现、负载均衡、熔断与超时。
sidebar:
  order: 3

---

# gRPC 客户端

`zrpc.Client` 是 go-zero 的 gRPC 客户端封装，自动集成**服务发现**、**P2C 负载均衡**、**熔断器**和 **OpenTelemetry 链路追踪**。

## 方案 A：直连（开发 / 测试）

```go title="internal/svc/servicecontext.go"
import (
    "github.com/zeromicro/go-zero/zrpc"
    "myservice/greeter"  // 生成的 proto 包
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

## 方案 B：通过 etcd 服务发现（生产环境）

```yaml title="etc/app.yaml"
GreeterRpc:
  Etcd:
    Hosts:
      - 127.0.0.1:2379
    Key: greeter.rpc
  Timeout: 2000       # 请求超时（毫秒）
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

`MustNewClient` 启动阶段出错时会 panic。如需自行处理错误，请使用 `NewClient`。

## 发起调用

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

`l.ctx` 携带 OpenTelemetry trace context，下游 RPC span 会自动关联到父级 HTTP span。

## 配置参考

```yaml
GreeterRpc:
  # 方案一：etcd 服务发现
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: greeter.rpc

  # 方案二：静态地址
  Endpoints:
    - 127.0.0.1:8080

  Timeout: 2000           # 客户端请求超时（毫秒），0 表示不限
  KeepaliveTime: 20000    # gRPC keepalive ping 间隔（毫秒）
```

## 错误处理

gRPC 错误携带状态码，go-zero 熔断器会统计这些状态：

```go
import "google.golang.org/grpc/status"

resp, err := l.svcCtx.GreeterClient.SayHello(l.ctx, req)
if err != nil {
    st, _ := status.FromError(err)
    switch st.Code() {
    case codes.NotFound:
        return nil, errorx.NewCodeError(404, "用户不存在")
    case codes.DeadlineExceeded:
        return nil, errorx.NewCodeError(504, "上游超时")
    default:
        return nil, err
    }
}
```

## 熔断器

熔断器默认开启。10 秒内错误率超过 50% 时自动打开：

```
正常：  请求 → RPC 调用 → 响应
断开：  请求 → 立即返回 503（不发 RPC）
半开：  允许单个探测请求通过以检查恢复情况
```

每个 `zrpc.Client` 自动生效，无需额外配置。

## 添加拦截器

向每次请求注入自定义元数据（如 API Token、用户 ID）：

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

## 延伸阅读

- [gRPC 拦截器](../interceptor) — 服务端与客户端拦截器详解
- [负载均衡](../../microservice/load-balancing) — P2C 如何在多实例间路由
