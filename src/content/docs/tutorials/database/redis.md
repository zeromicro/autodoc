---
title: Redis
description: Use Redis for caching and distributed state in go-zero services.
sidebar:
  order: 2
---

# Redis

go-zero wraps `go-redis` with connection pooling, metrics, and tracing out of the box.

## Configuration

```yaml
Redis:
  Host: 127.0.0.1:6379
  Pass: ""
  Type: node   # or "cluster"
```

## Initialize

```go title="internal/svc/servicecontext.go"
import "github.com/zeromicro/go-zero/core/stores/redis"

func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config: c,
        Redis:  redis.MustNewRedis(c.Redis),
    }
}
```

## Common Operations

```go
// Set with expiry (seconds)
err := rdb.Setex("session:abc123", "userId:42", 3600)

// Get
val, err := rdb.Get("session:abc123")

// Atomic counter
count, err := rdb.Incr("page:views")

// Distributed lock
lock := redis.NewRedisLock(rdb, "order:lock:12345")
lock.SetExpire(5)
if acquired, _ := lock.Acquire(); acquired {
    defer lock.Release()
    // critical section
}
```

## Cache-Aside

```go
var product Product
err = cache.Take(&product, fmt.Sprintf("product:%d", id), func(v any) error {
    *v.(*Product) = fetchFromDB(id)
    return nil
})
```
