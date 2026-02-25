---
title: 内存缓存
description: 使用本地缓存降低读压力。
sidebar:
  order: 6
---


go-zero 的 `collection.Cache` 提供线程安全、大小有界、按 TTL 淘汰的进程内 LRU 缓存。适合作为 Redis 前面的 **L1 缓存**，用于读取频繁、变化缓慢的数据。

## 基本用法

```go
import "github.com/zeromicro/go-zero/core/collection"

// 创建缓存：默认 TTL 1 分钟，最多 10000 条
c := collection.NewCache(
    time.Minute,
    collection.WithLimit(10000),
)

// 写入
c.Set("user:42", user)

// 读取
val, ok := c.Get("user:42")
if ok {
    return val.(*User), nil
}
// 过期或不存在时 ok == false
```

## 单条 TTL 覆盖

```go
// 此 session 单独缓存 30 分钟，不受全局 TTL 影响
c.SetWithExpire("session:abc", session, 30*time.Minute)
```

## 旁路读取（Take）

`Take` 是推荐的访问模式：缓存命中直接返回，否则执行 loader 函数（同一 key 同时只执行一次，singleflight 语义），防止缓存击穿：

```go
val, err := c.Take("user:42", func() (any, error) {
    // 同一 key 的并发请求只执行一次
    return db.QueryUserContext(ctx, 42)
})
if err != nil {
    return nil, err
}
user := val.(*User)
```

## 删除

```go
c.Del("user:42")
```

## L1 / L2 缓存分层

本地缓存（L1）+ Redis 缓存（L2）组合，大幅减少 Redis 请求量：

```go
func (r *UserRepo) GetUser(ctx context.Context, id int64) (*User, error) {
    key := fmt.Sprintf("user:%d", id)

    // L1 命中？
    if v, ok := r.l1.Get(key); ok {
        return v.(*User), nil
    }

    // L2（Redis）命中？
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

    // 填充 L1
    r.l1.Set(key, &user)
    return &user, nil
}

func (r *UserRepo) InvalidateUser(ctx context.Context, id int64) error {
    key := fmt.Sprintf("user:%d", id)
    r.l1.Del(key)          // 清除本地缓存
    return r.l2.Del(key)   // 清除 Redis
}
```

:::caution[L1 缓存是进程级的]
多副本部署时，每个实例有独立的进程内缓存。写入或删除数据时，**只需删除 Redis（L2）**，L1 会在 TTL 到期或下次读取时自动更新。
:::

## 适用场景

| 场景 | 是否推荐 |
|------|----------|
| 热点配置、功能开关等引用数据 | ✅ 推荐 |
| 请求级并发去重 | ✅ 推荐（Take）|
| 大数据集（>100 MB）| ❌ 用 Redis |
| 需要跨实例强一致的数据 | ⚠️ 配合短 TTL 使用 |
