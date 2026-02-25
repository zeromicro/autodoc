---
title: Redis Cache
description: Distributed read-through/write-through cache using Redis in go-zero.
sidebar:
  order: 2
---


go-zero's `cache` package wraps Redis with read-through, write-through, and cache-aside patterns, plus built-in stampede protection via singleflight. It is used internally by every `goctl`-generated model that has a cache layer.

## Configuration

```yaml title="etc/app.yaml"
Redis:
  Host: 127.0.0.1:6379
  Type: node       # "node" for single-instance, "cluster" for Redis Cluster
  Pass: ""
```

For Redis Cluster or multiple cache nodes with weighted traffic splitting:

```yaml
CacheRedis:
  - Host: redis-1:6379
    Type: node
    Weight: 50
  - Host: redis-2:6379
    Type: node
    Weight: 50
```

## Setup

```go
import (
    "github.com/zeromicro/go-zero/core/stores/cache"
    "github.com/zeromicro/go-zero/core/stores/sqlx"
)

// Single Redis node
cacheConf := cache.CacheConf{
    {RedisConf: c.Redis, Weight: 100},
}

// goctl-generated models wire this for you:
conn := sqlx.NewMysql(c.DataSource)
userModel := model.NewUserModel(conn, cacheConf)
```

## Read-Through with `Take`

`Take` is the core read-through operation. It:
1. Checks Redis for the key
2. On cache miss, runs the loader (inside a singleflight group) to prevent stampede
3. Serialises the result to JSON and stores it in Redis with a random jitter on the TTL
4. Returns the value

```go
var user model.User
err := userModel.FindOne(ctx, userId) // goctl model calls Take internally
```

For manual use outside of generated models:

```go
stats := cache.NewStat("user")         // named stat group for metrics
c := cache.New(cacheConf, nil, stats, model.ErrNotFound)

var user User
err = c.TakeCtx(ctx, &user, fmt.Sprintf("user:%d", id), func(v any) error {
    row, err := db.FindOne(ctx, id)
    if err != nil {
        return err
    }
    *v.(*User) = *row
    return nil
})
```

:::note[Negative caching]
When the loader returns `ErrNotFound` (the sentinel passed to `cache.New`), go-zero stores a placeholder in Redis for a short duration. This prevents cache penetration attacks where repeated queries for non-existent records bypass the cache and hammer the database.
:::

## Write-Through

Write the updated object to Redis immediately after the database write:

```go
// After updating the DB record:
err = c.SetWithExpire(fmt.Sprintf("user:%d", user.Id), &user, time.Hour)
```

goctl-generated `Update` methods call `DelCacheCtx` instead (cache-aside), which is simpler and avoids consistency edge cases:

```go
// goctl generated pattern — delete cache, let next read rebuild it
func (m *defaultUserModel) Update(ctx context.Context, data *User) error {
    _, err := m.ExecCtx(ctx, func(ctx context.Context, conn sqlx.SqlConn) (sql.Result, error) {
        return conn.ExecCtx(ctx, updateSql, data.Username, data.Id)
    }, m.formatPrimary(data.Id))
    return err
}
```

## Batch Invalidation

```go
// Delete multiple keys atomically
err = c.DelCtx(ctx,
    fmt.Sprintf("user:%d", id),
    fmt.Sprintf("user:name:%s", username),  // also delete secondary index key
)
```

## TTL and Jitter

go-zero adds a random jitter (±10% by default) to every cache entry's TTL to avoid **thundering herd at expiry** — the scenario where all entries for the same type expire simultaneously and cause a DB spike.

| TTL setting | Actual TTL range |
|-------------|------------------|
| 1 hour | 54 min – 66 min |
| 10 min | 9 min – 11 min |

## Stats and Metrics

The `cache.Stat` object tracks:

| Counter | Description |
|---------|-------------|
| `Total` | Total cache requests |
| `Hit` | Cache hits |
| `Miss` | Cache misses |
| `DbFails` | DB loader errors |

Expose to Prometheus:

```go
stats := cache.NewStat("user")
// metrics are exported via go-zero's built-in /metrics endpoint
// when prometheus is configured in app.yaml
```

## Best Practices

- Always **delete** the cache key after a database write rather than updating it (cache-aside). This avoids race conditions between the cache write and the DB write.
- Use **short TTL + negative caching** together to balance freshness and protection against penetration.
- Monitor the **hit rate** (`Hit / Total`). A hit rate below 90% usually indicates TTL is too short or the key space is too large.
- For write-heavy data (updated > every few seconds), consider skipping the cache entirely for that field to avoid excessive invalidation overhead.
