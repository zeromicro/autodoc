---
title: Redis
description: Use Redis for caching and distributed state in go-zero services.
sidebar:
  order: 2
---


go-zero wraps the Redis client with connection pooling, automatic retries, metrics, and tracing. The `core/stores/redis` package exposes a clean API covering strings, hashes, sets, sorted sets, lists, and distributed locks.

## Configuration

```yaml title="etc/app.yaml"
Redis:
  Host: 127.0.0.1:6379
  Pass: ""
  Type: node        # "node" (single) | "cluster" (Redis Cluster)
```

For Redis Cluster:

```yaml
Redis:
  Host: redis-master:6379   # any cluster node; client discovers the rest
  Type: cluster
  Pass: ""
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

## String Operations

```go
// Set with TTL (seconds)
err := rdb.Setex("session:abc123", "userId:42", 3600)

// Get
val, err := rdb.Get("session:abc123")

// Set if not exists (SETNX) — used for distributed deduplication
ok, err := rdb.SetnxEx("idempotency:order:X9", "1", 86400)
if !ok {
    return nil, ErrDuplicateRequest
}

// Atomic increment (counter)
count, err := rdb.Incr("stats:page:views")

// Increment by a specific amount
count, err = rdb.IncrBy("stats:total:sales", 150)
```

## Distributed Lock

```go
lock := redis.NewRedisLock(rdb, "order:process:12345")
lock.SetExpire(5)   // 5-second lock TTL

acquired, err := lock.Acquire()
if err != nil {
    return nil, err
}
if !acquired {
    return nil, ErrLockNotAcquired
}
defer lock.Release()

// --- critical section ---
```

## Hash Operations

```go
// Set fields on a hash
err = rdb.Hset("user:42", "name", "Alice")

// Get a field
name, err := rdb.Hget("user:42", "name")

// Get all fields
fields, err := rdb.Hgetall("user:42")

// Increment a hash field (e.g., for per-user counters)
val, err := rdb.Hincrby("user:42", "loginCount", 1)
```

## Sorted Set (Leaderboard, Rate Window)

```go
// Add / update score
err = rdb.Zadd("leaderboard", 1500, "player:alice")

// Get rank (0-based, ascending)
rank, err := rdb.Zrank("leaderboard", "player:alice")

// Get top-10 (descending)
members, err := rdb.ZrevrangeWithScores("leaderboard", 0, 9)

// Sliding-window rate limiting: add timestamp as score, trim old entries
now := time.Now().UnixMilli()
windowStart := now - int64(60*1000)   // last 60 s
_ = rdb.Zadd("rl:user:42", float64(now), fmt.Sprintf("%d", now))
_ = rdb.Zremrangebyscore("rl:user:42", "0", strconv.FormatInt(windowStart, 10))
count, _ := rdb.Zcard("rl:user:42")
if count > 100 {
    return nil, ErrRateLimited
}
```

## Pipeline

Send multiple commands in a single round-trip:

```go
_, err = rdb.Pipelined(func(pipe redis.Pipeliner) error {
    pipe.Set(ctx, "k1", "v1", time.Minute)
    pipe.Set(ctx, "k2", "v2", time.Minute)
    pipe.Incr(ctx, "counter")
    return nil
})
```

## Pub / Sub

```go
// Publisher
_ = rdb.Publish("events:order", `{"id":42,"status":"paid"}`)

// Subscriber (typically in a background goroutine)
pubsub, err := rdb.Subscribe("events:order")
if err != nil {
    log.Fatal(err)
}
defer pubsub.Close()

for msg := range pubsub.Channel() {
    fmt.Println(msg.Payload)
}
```

## TTL Management

```go
// Check remaining TTL
ttl, err := rdb.Ttl("session:abc123")   // returns time.Duration

// Refresh TTL on access
_ = rdb.Expire("session:abc123", 3600)

// Remove TTL (persist the key)
_ = rdb.Persist("session:abc123")
```

## Cache-Aside with `collection.Cache` (L1)

For hot data, combine Redis with an in-process L1 cache to avoid Redis round-trips on every request:

```go
var product Product
err = cache.TakeCtx(ctx, &product, fmt.Sprintf("product:%d", id), func(v any) error {
    *v.(*Product) = fetchFromDB(id)
    return nil
})
```

See [Memory Cache](../../components/cache/memory-cache) for the full L1/L2 pattern.

## Connection Health

```go
// Ping checks connectivity (use in health-check handlers)
if err := rdb.Ping(); err != nil {
    httpx.Error(w, err, http.StatusServiceUnavailable)
    return
}
```
