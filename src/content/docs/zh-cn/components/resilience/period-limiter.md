---
title: 周期限流器
description: 使用 go-zero 按时间段限制请求速率。
sidebar:
  order: 2

---


`limit.PeriodLimit` 主要用于在一段时间内限制请求。它基于Redis实现，通过Lua脚本进行限流操作。

## 常量

```go
const (
    // 未初始化状态。
    Unknown = iota
    // 允许状态。
    Allowed
    // 准确达到配额。
    HitQuota
    // 超过配额。
    OverQuota
)
```

## 变量

```go
var (
    // 表示未知状态码的错误。
    ErrUnknownCode = errors.New("unknown status code")
)
```

## 类型

### PeriodLimit

`PeriodLimit`用于在特定时间段内限制请求。它具有以下字段：

### PeriodOption

`PeriodOption`定义了自定义`PeriodLimit`的方法。

## 函数

### NewPeriodLimit

创建一个新的`PeriodLimit`实例。

```go
func NewPeriodLimit(period, quota int, limitStore *redis.Redis, keyPrefix string, opts ...PeriodOption) *PeriodLimit
```

#### 参数说明

- `period`: 限制应用的时间段，以秒为单位。
- `quota`: 在指定时间段内允许的最大请求数量。
- `limitStore`: 用于跟踪限制的Redis存储实例。
- `keyPrefix`: 用于区分不同限制的键前缀。
- `opts`: 自定义`PeriodLimit`实例的可选参数。

### 示例

```go
package main

import (
    "fmt"
    "limit"

    "github.com/zeromicro/go-zero/core/stores/redis"
)

func main() {
    store := redis.New("localhost:6379")
    limiter := limit.NewPeriodLimit(60, 10, store, "exampleKey")

    result, err := limiter.Take("user1")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }

    switch result {
    case limit.Allowed:
        fmt.Println("Request allowed")
    case limit.HitQuota:
        fmt.Println("Hit the quota")
    case limit.OverQuota:
        fmt.Println("Over the quota")
    default:
        fmt.Println("Unknown status")
    }
}
```

### Take

请求一个许可，返回许可状态。

```go
func (h *PeriodLimit) Take(key string) (int, error)
```

#### 参数说明

- `key`: 用于标识请求者的键。通常是客户端或用户的唯一标识符。

#### 返回值

- 一个整数表示许可状态（`Allowed`、`HitQuota`、`OverQuota` 或 `Unknown`）。
- 如果请求处理过程中出现问题，则返回错误。

### TakeCtx

带上下文地请求一个许可，返回许可状态。

```go
func (h *PeriodLimit) TakeCtx(ctx context.Context, key string) (int, error)
```

#### 参数说明

- `ctx`: 控制此函数执行的上下文，适用于超时和取消操作。
- `key`: 用于标识请求者的键。通常是客户端或用户的唯一标识符。

#### 返回值

- 一个整数表示许可状态（`Allowed`、`HitQuota`、`OverQuota` 或 `Unknown`）。
- 如果请求处理过程中出现问题，则返回错误。

### Align

返回一个用于对齐时间段的`PeriodOption`。

```go
func Align() PeriodOption
```

#### 返回值

- 一个`PeriodOption`，可用于配置`PeriodLimit`以对齐其时间段。例如，对齐到一天的开始。

### 示例

```go
package main

import (
    "fmt"
    "limit"

    "github.com/zeromicro/go-zero/core/stores/redis"
)

func main() {
    store := redis.New("localhost:6379")
    limiter := limit.NewPeriodLimit(86400, 5, store, "sms_limit", limit.Align())

    result, err := limiter.Take("user1")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }

    switch result {
    case limit.Allowed:
        fmt.Println("SMS request allowed")
    case limit.HitQuota:
        fmt.Println("Hit the daily quota")
    case limit.OverQuota:
        fmt.Println("Over the daily quota")
    default:
        fmt.Println("Unknown status")
    }
}
```