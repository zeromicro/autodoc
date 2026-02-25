---
title: 限流器
description: 自适应限流器的使用与配置。
sidebar:
  order: 3

---


go-zero 提供两种基于 Redis 的限流原语：用于平滑流量的**令牌桶**限流器，以及用于固定窗口配额的**周期限流器**。

## 令牌桶限流器

令牌桶以固定速率补充，允许短时间内的突发请求。以 Redis 作为共享状态存储，在多实例场景下同样正确工作。

```go
import (
    "github.com/zeromicro/go-zero/core/limit"
    "github.com/zeromicro/go-zero/core/stores/redis"
)

rds := redis.MustNewRedis(redis.RedisConf{Host: "127.0.0.1:6379", Type: "node"})
// rate=100 req/s，burst=200 个令牌
limiter := limit.NewTokenLimiter(100, 200, rds, "api:orders")

if limiter.Allow() {
    // 处理请求
} else {
    httpx.Error(w, errorx.NewCodeError(429, "too many requests"))
}
```

### 携带上下文

使用 `AllowCtx` 可感知请求取消：

```go
if limiter.AllowCtx(r.Context()) {
    // 继续处理
}
```

### 批量消耗

一次消耗 N 个令牌，适合批处理或权重计费：

```go
n := len(req.Items)
if limiter.AllowN(time.Now(), n) {
    // 处理批量请求
}
```

## 周期限流器（固定窗口）

在固定时间窗口内限制最大请求数，适合按用户配额计费（如"每小时 1000 次 API 调用"）。

```go
// 每用户每小时限制 1000 次
limiter := limit.NewPeriodLimit(3600, 1000, rds, "user:rate:")

code, err := limiter.Take("user:42")
switch code {
case limit.Allowed:
    // 未超配额——正常处理
case limit.HitQuota:
    // 本次是窗口内最后一个允许的请求，可提前提醒调用方
case limit.OverQuota:
    // 超出配额——返回 429
}
```

### 携带上下文

```go
code, err := limiter.TakeCtx(r.Context(), "user:42")
```

## HTTP 中间件

对 `rest.Server` 下所有路由注册限流中间件：

```go
func RateLimitMiddleware(limiter *limit.TokenLimiter) rest.Middleware {
    return func(next http.HandlerFunc) http.HandlerFunc {
        return func(w http.ResponseWriter, r *http.Request) {
            if !limiter.AllowCtx(r.Context()) {
                http.Error(w, "too many requests", http.StatusTooManyRequests)
                return
            }
            next(w, r)
        }
    }
}

server.Use(RateLimitMiddleware(limiter))
```

或在 `.api` 文件中按路由组挂载：

```text
@server (
    middleware: RateLimit
)
service user-api {
    @handler CreateUser
    post /users (CreateUserReq) returns (CreateUserResp)
}
```

## 按用户限流

在 logic 中结合认证用户 ID 实现细粒度限流：

```go
func (l *CreateOrderLogic) CreateOrder(req *types.CreateOrderReq) (*types.CreateOrderResp, error) {
    key := fmt.Sprintf("user:%d", req.UserId)
    code, err := l.svcCtx.RateLimiter.Take(key)
    if err != nil || code == limit.OverQuota {
        return nil, errorx.NewCodeError(429, "触发限流")
    }
    // ... 业务逻辑
}
```

## Redis 集群

两种限流器均接受 `*redis.Redis` 客户端。使用 Redis 集群：

```go
rds := redis.MustNewRedis(redis.RedisConf{
    Host: "127.0.0.1:7000",
    Type: "cluster",
})
```

## 最佳实践

- **按接口+用户粒度设计 key**，避免单一全局 key 导致某个用户耗尽所有配额。
- **Burst 设为 rate 的 2 倍左右**，吸收正常流量毛刺，减少误拒请求。
- **Redis 不可用时自动降级**：`TokenLimiter` 会自动切换为进程内限流器，服务不会中断。
- **监控 OverQuota 事件**：通过 Prometheus 计数器告警，及时发现持续限流压力。
