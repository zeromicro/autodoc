---
title: Period Limiter
description: Limit request rates per period with go-zero.
sidebar:
  order: 2

---


The `limit.PeriodLimit` is mainly used to limit requests within a period. It is implemented based on Redis and performs rate limiting operations through Lua scripts.

## Constants

```go
const (
    // Unknown means not initialized state.
    Unknown = iota
    // Allowed means allowed state.
    Allowed
    // HitQuota means this request exactly hit the quota.
    HitQuota
    // OverQuota means passed the quota.
    OverQuota
)
```

## Variables

```go
var (
    // ErrUnknownCode is an error that represents unknown status code.
    ErrUnknownCode = errors.New("unknown status code")
)
```

## Types

### PeriodLimit

`PeriodLimit` is used to limit requests during a specific period. It has the following fields:

### PeriodOption

`PeriodOption` defines the method to customize a `PeriodLimit`.

## Functions

### NewPeriodLimit

Creates a new `PeriodLimit` instance.

```go
func NewPeriodLimit(period, quota int, limitStore *redis.Redis, keyPrefix string, opts ...PeriodOption) *PeriodLimit
```

#### Parameters

- `period`: The time period in seconds for which the rate limit applies.
- `quota`: The maximum number of allowed requests within the specified period.
- `limitStore`: The Redis store instance used for keeping track of the limits.
- `keyPrefix`: A prefix for the keys used in Redis to distinguish different limits.
- `opts`: Optional customization options for the `PeriodLimit` instance.

### Example

```go
package main

import (
    "fmt"
    "github.com/zeromicro/go-zero/core/stores/redis"
    "limit"
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

Requests a permit, returns the permit state.

```go
func (h *PeriodLimit) Take(key string) (int, error)
```

#### Parameters

- `key`: The key to identify the requester. This is usually a unique identifier for the client or user making the request.

#### Returns

- An integer representing the permit state (`Allowed`, `HitQuota`, `OverQuota`, or `Unknown`).
- An error if something goes wrong during the request processing.

### TakeCtx

Requests a permit with context, returns the permit state.

```go
func (h *PeriodLimit) TakeCtx(ctx context.Context, key string) (int, error)
```

#### Parameters

- `ctx`: The context to control the execution of this function, useful for timeouts and cancellations.
- `key`: The key to identify the requester. This is usually a unique identifier for the client or user making the request.

#### Returns

- An integer representing the permit state (`Allowed`, `HitQuota`, `OverQuota`, or `Unknown`).
- An error if something goes wrong during the request processing.

### Align

Returns a `PeriodOption` to align the time period.

```go
func Align() PeriodOption
```

#### Returns

- A `PeriodOption` that can be used to configure a `PeriodLimit` to align its time periods. For example, aligning to the start of a day.

### Example

```go
package main

import (
    "fmt"
    "github.com/zeromicro/go-zero/core/stores/redis"
    "limit"
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
