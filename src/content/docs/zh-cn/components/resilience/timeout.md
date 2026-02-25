---
title: 超时控制
description: 在 go-zero HTTP 和 gRPC 服务中配置请求超时。
sidebar:
  order: 4

---

go-zero 在多层执行请求超时控制，防止慢上游耗尽协程池。

## HTTP 服务超时

```yaml title="etc/app.yaml"
Timeout: 3000  # 毫秒（默认值：3000）
```

超过此时间的请求会自动收到 HTTP 408 响应。

## gRPC 服务端超时

```yaml title="etc/rpc.yaml"
Timeout: 2000  # 毫秒
```

## 客户端超时

通过带有 deadline 的 context 传递：

```go
ctx, cancel := context.WithTimeout(l.ctx, 2*time.Second)
defer cancel()

resp, err := l.svcCtx.OrderRpc.CreateOrder(ctx, req)
```

go-zero 的 `TimeoutInterceptor` 会自动将入站请求的 deadline 传播到所有下游 RPC 调用。

## 按路由超时（HTTP）

```go
server.AddRoute(rest.Route{
    Method:  http.MethodPost,
    Path:    "/slow-endpoint",
    Handler: myHandler,
}, rest.WithTimeout(10*time.Second))
```

## 超时与 Context 取消的区别

| 场景 | 行为 |
|------|------|
| 客户端断开连接 | Context 被取消，上游协程退出 |
| 超时到达 | 返回 408；协程继续运行直到完成 |
| 两者同时 | Context 先被取消 |
