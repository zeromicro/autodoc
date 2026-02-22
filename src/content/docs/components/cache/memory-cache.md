---
title: Memory Cache
description: In-process LRU/TTL cache for go-zero services.
sidebar:
  order: 1
---

# Memory Cache

go-zero's `collection.Cache` provides a thread-safe, size-bounded, TTL-evicting in-process cache backed by LRU eviction.

## Basic Usage

```go
import "github.com/zeromicro/go-zero/core/collection"

c := collection.NewCache(time.Minute)   // default TTL = 1 minute

// Set
c.Set("user:42", user)

// Get
val, ok := c.Get("user:42")
if ok {
    return val.(*User), nil
}
```

## With Custom TTL per Entry

```go
c.SetWithExpire("session:abc", session, 30*time.Minute)
```

## Take (Read-Through)

```go
val, err := c.Take("user:42", func() (any, error) {
    return db.QueryUser(42)
})
```

`Take` is safe for concurrent callers — only one goroutine executes the loader function for the same key (singleflight semantics).

## Configuration

```go
c := collection.NewCache(
    time.Minute,
    collection.WithLimit(10000),   // max 10 000 items
)
```

## When to Use

- Hot data that fits in memory and changes infrequently
- Local deduplication of identical concurrent reads
- Complement to Redis cache for L1/L2 layering
