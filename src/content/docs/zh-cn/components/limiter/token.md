---
title: Token Bucket Limiter
description: 使用 go-zero 令牌桶限制请求速率。
sidebar:
  order: 3

---

## limit.TokenLimiter

`TokenLimiter` 是一个基于令牌桶算法的限流器，控制每秒内事件发生的频率。它依赖 Redis 存储令牌桶状态，并在 Redis 不可用时提供降级机制。

### 创建 TokenLimiter

```go
func NewTokenLimiter(rate, burst int, store *redis.Redis, key string) *TokenLimiter
```

创建并返回一个新的 `TokenLimiter` 实例。

- **参数**：
    - `rate`：每秒允许的事件数量。
    - `burst`：允许的最大突发事件数量。
    - `store`：Redis 客户端实例。
    - `key`：用于生成 Redis 存储键的关键字。

- **返回值**：返回一个 `TokenLimiter` 实例。

### Allow

```go
func (lim *TokenLimiter) Allow() bool
```

检查是否允许发生单个事件。等价于 `AllowN(time.Now(), 1)`。

- **返回值**：若允许则返回 `true`，否则返回 `false`。

### AllowCtx

```go
func (lim *TokenLimiter) AllowCtx(ctx context.Context) bool
```

携带上下文信息检查是否允许发生单个事件，等价于 `AllowNCtx(ctx, time.Now(), 1)`。

- **参数**：
    - `ctx`：用于控制请求生命周期的上下文信息。

- **返回值**：若允许则返回 `true`，否则返回 `false`。

### AllowN

```go
func (lim *TokenLimiter) AllowN(now time.Time, n int) bool
```

检查在指定时间是否允许发生 `n` 个事件。

- **参数**：
    - `now`：当前时间。
    - `n`：请求的事件数量。

- **返回值**：若允许则返回 `true`，否则返回 `false`。

### AllowNCtx

```go
func (lim *TokenLimiter) AllowNCtx(ctx context.Context, now time.Time, n int) bool
```

携带上下文信息检查在指定时间是否允许发生 `n` 个事件。

- **参数**：
    - `ctx`：用于控制请求生命周期的上下文信息。
    - `now`：当前时间。
    - `n`：请求的事件数量。

- **返回值**：若允许则返回 `true`，否则返回 `false`。

## 示例

### 基础示例

```go
package main

import (
    "fmt"

    "github.com/zeromicro/go-zero/core/limit"
    "github.com/zeromicro/go-zero/core/stores/redis"
)

func main() {
    store := redis.NewRedis("localhost:6379", redis.NodeType)
    limiter := limit.NewTokenLimiter(10, 20, store, "example-key")

    if limiter.Allow() {
        fmt.Println("请求允许")
    } else {
        fmt.Println("请求被限流")
    }
}
```

每秒允许 10 个事件，最大突发 20 个。

### 携带上下文

```go
package main

import (
    "context"
    "fmt"
    "time"

    "github.com/zeromicro/go-zero/core/limit"
    "github.com/zeromicro/go-zero/core/stores/redis"
)

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()

    store := redis.NewRedis("localhost:6379", redis.NodeType)
    limiter := limit.NewTokenLimiter(5, 10, store, "example-key")

    if limiter.AllowCtx(ctx) {
        fmt.Println("请求允许（带上下文）")
    } else {
        fmt.Println("请求被限流（带上下文）")
    }
}
```

### 批量事件检查

```go
package main

import (
    "fmt"
    "time"

    "github.com/zeromicro/go-zero/core/limit"
    "github.com/zeromicro/go-zero/core/stores/redis"
)

func main() {
    store := redis.NewRedis("localhost:6379", redis.NodeType)
    limiter := limit.NewTokenLimiter(10, 20, store, "example-key")

    now := time.Now()
    requests := 3
    if limiter.AllowN(now, requests) {
        fmt.Printf("允许 %d 个请求（时间：%v）\n", requests, now)
    } else {
        fmt.Printf("拒绝 %d 个请求（时间：%v）\n", requests, now)
    }
}
```
