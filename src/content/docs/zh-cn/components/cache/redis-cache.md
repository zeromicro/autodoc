---
title: Redis 缓存
description: 使用 Redis 构建分布式缓存能力。
sidebar:
  order: 7
---


go-zero 的 `cache` 包对 Redis 进行了封装，支持旁路读取、写穿、缓存失效等模式，并通过 singleflight 内置防击穿保护。goctl 生成的所有带缓存的 model 均基于此包。

## 配置

```yaml title="etc/app.yaml"
Redis:
  Host: 127.0.0.1:6379
  Type: node       # node=单机，cluster=集群
  Pass: ""
```

多节点（权重分片）：

```yaml
CacheRedis:
  - Host: redis-1:6379
    Type: node
    Weight: 50
  - Host: redis-2:6379
    Type: node
    Weight: 50
```

## 初始化

```go
cacheConf := cache.CacheConf{
    {RedisConf: c.Redis, Weight: 100},
}
// goctl 生成的 model 会自动接入，无需手动初始化
conn := sqlx.NewMysql(c.DataSource)
userModel := model.NewUserModel(conn, cacheConf)
```

## 旁路读取（Take）

`Take` 是核心访问模式。cache miss 时由 singleflight 保证 loader 只执行一次，并将结果序列化为 JSON 存入 Redis：

```go
var user model.User
err := userModel.FindOne(ctx, userId) // goctl model 内部调用 Take
```

手动使用：

```go
stats := cache.NewStat("user")
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

:::note[空值缓存]
当 loader 返回 `ErrNotFound` 时，go-zero 会在 Redis 中存储占位符，防止缓存穿透攻击（对不存在记录的大量查询穿透缓存直达数据库）。
:::

## 写后删除（Cache-Aside）

goctl 生成的 `Update` / `Delete` 方法采用**删除缓存**而非更新缓存的模式，避免并发写入时的一致性问题：

```go
// goctl 生成模式：更新 DB 后删除缓存，下次读取时重建
func (m *defaultUserModel) Update(ctx context.Context, data *User) error {
    _, err := m.ExecCtx(ctx, func(ctx context.Context, conn sqlx.SqlConn) (sql.Result, error) {
        return conn.ExecCtx(ctx, updateSql, data.Username, data.Id)
    }, m.formatPrimary(data.Id))
    return err
}
```

## 批量失效

```go
// 同时删除主键缓存和唯一索引缓存
err = c.DelCtx(ctx,
    fmt.Sprintf("user:%d", id),
    fmt.Sprintf("user:name:%s", username),
)
```

## TTL 抖动

go-zero 对每个缓存条目的 TTL 增加 ±10% 的随机抖动，防止大量同类型缓存在同一时刻集中过期导致数据库流量突增。

## 最佳实践

- 写入后**删除缓存**而不是更新缓存，避免并发竞态。
- 短 TTL + 空值缓存结合，兼顾数据新鲜度与缓存穿透防护。
- 监控命中率，低于 90% 时通常意味着 TTL 过短或 key 空间过大。
- 高频写入（每秒多次更新）的字段不适合缓存，频繁失效的开销会超过收益。
