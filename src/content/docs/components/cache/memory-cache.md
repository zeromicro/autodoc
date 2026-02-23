---
title: Memory Cache
description: In-process LRU/TTL cache for go-zero services.
sidebar:
  order: 1
---

# Memory Cache

go-zero's `collection.Cache` provides a thread-safe, size-bounded, TTL-evicting in-process cache backed by LRU eviction. It's ideal as an **L1 cache** in front of Redis for frequently-read, slow-changing data.

## Basic Usage

```go
import "github.com/zeromicro/go-zero/core/collection"

// Create a cache with 1-minute default TTL and max 10 000 entries
c := collection.NewCache(
    time.Minute,
    collection.WithLimit(10000),
)

// Set a value (uses default TTL)
c.Set("user:42", user)

// Get
val, ok := c.Get("user:42")
if ok {
    return val.(*User), nil
}
// if expired or missing, ok == false
```

## Per-Entry TTL

Override the default TTL for individual entries:

```go
// Cache a session for 30 minutes regardless of the global TTL
c.SetWithExpire("session:abc", session, 30*time.Minute)
```

## Read-Through with `Take`

`Take` is the recommended access pattern: it retrieves from cache and, on a miss, executes the provided loader exactly once — even if hundreds of goroutines call it concurrently for the same key (singleflight semantics):

```go
val, err := c.Take("user:42", func() (any, error) {
    // runs at most once per key per TTL window
    return db.QueryUserContext(ctx, 42)
})
if err != nil {
    return nil, err
}
user := val.(*User)
```

This prevents **cache stampede** — the thundering-herd problem when many goroutines try to reload the same expired key simultaneously.

## Delete

```go
c.Del("user:42")
```

## Constructor Options

| Option | Default | Description |
|--------|---------|-------------|
| `WithLimit(n)` | `nil` (unlimited) | Maximum number of items before LRU eviction kicks in |

## TTL and Eviction Behaviour

- Entries are **lazily expired**: they're removed on the next access after TTL, not by a background goroutine.
- When the item count exceeds the limit, the **least-recently-used** entry is evicted immediately.
- There is no persistence — cache is empty on process restart.

## L1 / L2 Pattern

Combine memory cache (L1) with Redis cache (L2) to slash Redis read traffic:

```go
type UserRepo struct {
    l1  *collection.Cache   // in-process, 30 s TTL
    l2  cache.Cache         // Redis-backed, 10 min TTL
    db  *model.UserModel
}

func (r *UserRepo) GetUser(ctx context.Context, id int64) (*User, error) {
    key := fmt.Sprintf("user:%d", id)

    // L1 hit?
    if v, ok := r.l1.Get(key); ok {
        return v.(*User), nil
    }

    // L2 hit? (Redis)
    var user User
    err := r.l2.TakeCtx(ctx, &user, key, func(v any) error {
        row, err := r.db.FindOne(ctx, id)
        if err != nil {
            return err
        }
        *v.(*User) = *row
        return nil
    })
    if err != nil {
        return nil, err
    }

    // Populate L1
    r.l1.Set(key, &user)
    return &user, nil
}

func (r *UserRepo) InvalidateUser(ctx context.Context, id int64) error {
    key := fmt.Sprintf("user:%d", id)
    r.l1.Del(key)          // remove from local cache
    return r.l2.Del(key)   // remove from Redis
}
```

:::caution[L1 cache is per-process]
In a multi-replica deployment, each instance has its own in-process cache. When you write or delete data, **invalidate Redis (L2) only** — L1 will re-populate on the next read or expire naturally via TTL.
:::

## Thread Safety

`collection.Cache` is safe for concurrent use from multiple goroutines. All operations use a read-write lock internally.

## When to Use

| Scenario | Recommended? |
|----------|--------------|
| Hot reference data (configs, feature flags) | ✅ Yes |
| Per-request deduplication | ✅ Yes (`Take`) |
| Large datasets (>100 MB) | ❌ No — use Redis |
| Data requiring cross-instance consistency | ⚠️ Combine with short TTL |
| Frequently-written data | ⚠️ Keep TTL short to limit staleness |
