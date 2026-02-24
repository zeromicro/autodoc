---
title: syncx Limit
description: Concurrency limiting with a borrow/return semaphore from go-zero syncx.
sidebar:
  order: 10

---

## syncx.Limit

The `syncx` package provides a concurrency-limiting primitive via the `Limit` type. It uses a buffered channel as a semaphore to cap the number of simultaneous in-flight requests.

## Variables

### ErrLimitReturn

```go
var ErrLimitReturn = errors.New("discarding limited token, resource pool is full, someone returned multiple times")
```

Returned when a caller tries to return more tokens than were borrowed — i.e., the resource pool is already full.

## Types

### Limit

```go
type Limit struct {
    pool chan lang.PlaceholderType
}
```

`Limit` wraps a buffered channel `pool` that controls the number of concurrent requests.

## Functions

### NewLimit

```go
func NewLimit(n int) Limit
```

Creates a `Limit` that allows at most `n` concurrent borrows.

**Parameters**

- `n` (`int`): Maximum number of simultaneous borrows allowed.

**Returns**

- `Limit`: A new `Limit` instance.

### Borrow

```go
func (l Limit) Borrow()
```

Blocks until a token is available, then acquires it.

### Return

```go
func (l Limit) Return() error
```

Returns a previously borrowed token. Returns `ErrLimitReturn` if the pool is already full (i.e., a token was returned more times than it was borrowed).

**Returns**

- `error`: `nil` on success, `ErrLimitReturn` on over-return.

### TryBorrow

```go
func (l Limit) TryBorrow() bool
```

Attempts to acquire a token without blocking.

**Returns**

- `bool`: `true` if a token was acquired, `false` if none are available.

## Example

```go
package main

import (
    "fmt"

    "github.com/zeromicro/go-zero/core/syncx"
)

func main() {
    limit := syncx.NewLimit(3) // allow at most 3 concurrent operations

    // Non-blocking try
    if limit.TryBorrow() {
        fmt.Println("acquired token")
        if err := limit.Return(); err != nil {
            fmt.Println("return error:", err)
        }
    }

    // Blocking borrow
    limit.Borrow()
    defer limit.Return()
    fmt.Println("doing work under limit")
}
```
