---
title: Token Bucket Limiter
description: Limit request rates with a token bucket in go-zero.
sidebar:
  order: 3

---


## limit.TokenLimiter

`TokenLimiter` is a rate limiter that controls the frequency of events occurring within one second. It relies on Redis to store the state of the token bucket and provides a fallback mechanism in case Redis is unavailable.

### Creating a New TokenLimiter

```go
func NewTokenLimiter(rate, burst int, store *redis.Redis, key string) *TokenLimiter
```

Creates and returns a new `TokenLimiter` instance.

- **Parameters**:
    - `rate`: The number of events allowed per second.
    - `burst`: The maximum number of burst events allowed.
    - `store`: The Redis client instance.
    - `key`: The keyword used to generate Redis storage keys.

- **Returns**: A `TokenLimiter` instance.

### Allow

```go
func (lim *TokenLimiter) Allow() bool
```

Checks if a single event is allowed to occur. This is a shorthand for `AllowN(time.Now(), 1)`.

- **Returns**: Returns `true` if the event is allowed; otherwise returns `false`.

### AllowCtx

```go
func (lim *TokenLimiter) AllowCtx(ctx context.Context) bool
```

Checks if a single event is allowed to occur with context information. This is a shorthand for `AllowNCtx(ctx, time.Now(), 1)`.

- **Parameters**:
    - `ctx`: Context information used to control the lifecycle of the request.

- **Returns**: Returns `true` if the event is allowed; otherwise returns `false`.

### AllowN

```go
func (lim *TokenLimiter) AllowN(now time.Time, n int) bool
```

Checks if `n` events are allowed to occur at the specified time.

- **Parameters**:
    - `now`: The current time.
    - `n`: The number of requested events.

- **Returns**: Returns `true` if the events are allowed; otherwise returns `false`.

### AllowNCtx

```go
func (lim *TokenLimiter) AllowNCtx(ctx context.Context, now time.Time, n int) bool
```

Checks if `n` events are allowed to occur at the specified time with context information.

- **Parameters**:
    - `ctx`: Context information used to control the lifecycle of the request.
    - `now`: The current time.
    - `n`: The number of requested events.

- **Returns**: Returns `true` if the events are allowed; otherwise returns `false`.

## Examples

Here are some examples of how to use `TokenLimiter`:

### Simple Example

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

	if limiter.Allow() {
		fmt.Println("Request allowed")
	} else {
		fmt.Println("Request not allowed")
	}
}
```

In this example, we create a `TokenLimiter` that allows up to 10 events per second and up to 20 burst events. We then use the `Allow` method to check if the current request is allowed.

### Example with Context Information

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
		fmt.Println("Request allowed with context")
	} else {
		fmt.Println("Request not allowed with context")
	}
}
```

In this example, we use context information to control the lifecycle of the request. If permission is not obtained within the specified time, the `AllowCtx` method will return `false`.

### Example Checking Multiple Events

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
		fmt.Printf("%d requests allowed at %v\n", requests, now)
	} else {
		fmt.Printf("%d requests not allowed at %v\n", requests, now)
	}
}
```

In this example, we check if 3 events are allowed to occur at the current time. If allowed, corresponding information will be printed.

These examples help you better understand how to use `TokenLimiter` for event rate limiting in different scenarios.
