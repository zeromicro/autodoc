---
title: Redis Cache
description: Distributed read-through/write-through cache using Redis in go-zero.
sidebar:
  order: 2
---

# Redis Cache

go-zero's `cache` package wraps Redis with read-through, write-through, and cache-aside patterns, plus built-in stampede protection via singleflight.

## Setup

```go
import (
    "github.com/zeromicro/go-zero/core/stores/cache"
    "github.com/zeromicro/go-zero/core/stores/redis"
)

rds := redis.MustNewRedis(c.Redis)
cacheConf := cache.CacheConf{
    {RedisConf: c.Redis, Weight: 100},
}
stats := cache.NewStat("user")
c := cache.New(cacheConf, nil, stats, model.ErrNotFound)
```

## Read-Through

```go
var user User
err = c.Take(&user, fmt.Sprintf("user:%d", id), func(v any) error {
    row, err := db.QueryUser(l.ctx, id)
    if err != nil {
        return err
    }
    *v.(*User) = *row
    return nil
})
```

If the key is missing, the loader runs, stores the result in Redis, and returns it. Concurrent callers for the same key share a single loader execution (singleflight).

## Write-Through

```go
err = c.SetWithExpire(fmt.Sprintf("user:%d", user.Id), user, time.Hour)
```

## Invalidation

```go
err = c.Del(fmt.Sprintf("user:%d", id))
```

## Stats

```go
// stats.IncrTotal() / stats.IncrHit() called internally
// Export to Prometheus via go-zero metrics integration
```
