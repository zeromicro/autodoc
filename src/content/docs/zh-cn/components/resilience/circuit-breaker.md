---
title: 熔断器
description: 通过熔断保护下游服务。
sidebar:
  order: 2

---


go-zero 在每个 RPC 客户端和 HTTP 服务中内置了 Google SRE 风格的熔断器——无需手动配置即可自动生效。

## 工作原理

熔断器在滑动窗口内统计错误率。当错误率超过阈值时，熔断器**打开**，后续请求立即失败（快速失败），不再等待慢速下游。冷却期结束后，允许一个探测请求通过——若成功则重新关闭熔断器。

| 状态 | 条件 | 行为 |
|------|------|------|
| **关闭（Closed）** | 错误率低于阈值 | 正常处理，持续统计错误 |
| **打开（Open）** | 错误率超过阈值 | 所有请求立即被拒绝 |
| **半开（Half-Open）** | 冷却期到达 | 放行一个探测请求 |

算法基于 [Google SRE 自适应限流](https://sre.google/sre-book/handling-overload/)：被拒绝请求数 = max(0, (请求数 − K × 成功数) / (请求数 + 1))，K 默认为 1.5。

## 自动模式（RPC 与 HTTP）

无需任何代码——所有 `zrpc` 调用和 HTTP 下游请求自动受到保护：

```go
// 自动受到熔断器、P2C 负载均衡和超时保护
resp, err := l.svcCtx.OrderRpc.CreateOrder(l.ctx, req)
if err != nil {
    // 熔断器打开时：err == breaker.ErrServiceUnavailable
    return nil, err
}
```

## 手动使用

使用 `breaker.NewBreaker()` 保护任意外部调用（数据库、HTTP API、Redis 等）：

```go
import "github.com/zeromicro/go-zero/core/breaker"

b := breaker.NewBreaker(breaker.WithName("payment-gateway"))

// 简单模式：统计所有非 nil 错误
err := b.Do(func() error {
    return callPaymentAPI(req)
})
```

### DoWithFallback

熔断器打开时提供降级逻辑：

```go
err := b.DoWithFallback(
    func() error {
        return callPaymentAPI(req)
    },
    func(err error) error {
        // 返回缓存结果、加入重试队列，或返回友好错误
        return serveCachedResult(req)
    },
)
```

### DoWithAcceptable

精确控制哪些错误计入失败计数——避免 `ErrNotFound` 等业务错误触发熔断：

```go
err := b.DoWithAcceptable(
    func() error {
        return callPaymentAPI(req)
    },
    func(err error) bool {
        // 返回 true = "此错误可接受，不计入熔断计数"
        return errors.Is(err, ErrNotFound) || errors.Is(err, ErrUnauthorized)
    },
)
```

### DoWithFallbackAcceptable

同时使用降级逻辑和自定义错误接受策略：

```go
err := b.DoWithFallbackAcceptable(fn, fallbackFn, acceptableFn)
```

## 配置

内置熔断器使用合理的默认参数。可自定义名称（用于日志和指标标签）：

```go
b := breaker.NewBreaker(breaker.WithName("stripe-api"))
```

`zrpc` 客户端自动为每个下游服务创建独立熔断器，以 `etcd Key` 或 endpoint 字符串为键。

## Prometheus 指标

开启 Prometheus 后，熔断器自动上报以下指标：

| 指标 | 含义 |
|------|------|
| `breaker_total` | 通过熔断器的总请求数 |
| `breaker_pass` | 允许通过的请求数 |
| `breaker_drop` | 被拒绝的请求数（熔断器打开状态） |

## 最佳实践

- **为熔断器命名**：唯一名称使日志和指标能区分不同的故障来源。
- **不要吞掉错误**：熔断器依赖准确的错误反馈计算错误率，不要在回调函数中吞掉真实错误。
- **使用 `DoWithAcceptable` 排除业务错误**：4xx 类错误通常是调用方的问题，非下游故障，排除后可让熔断器更准确地感知下游健康状态。
- **配合超时使用**：熔断器防止级联失败，但仍需为每次调用设置超时，避免 goroutine 堆积。
