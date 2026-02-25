---
title: Redis
description: 缓存与分布式协作场景中的 Redis 使用。
sidebar:
  order: 11
---

# Redis

go-zero 对 Redis 客户端进行封装，内置连接池、自动重试、指标统计和链路追踪。

## 配置

```yaml title="etc/app.yaml"
Redis:
  Host: 127.0.0.1:6379
  Pass: ""
  Type: node        # node=单机 | cluster=集群
```

## 初始化

```go title="internal/svc/servicecontext.go"
import "github.com/zeromicro/go-zero/core/stores/redis"

func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config: c,
        Redis:  redis.MustNewRedis(c.Redis),
    }
}
```

## 字符串操作

```go
// 带过期时间设置（秒）
err := rdb.Setex("session:abc123", "userId:42", 3600)

// 读取
val, err := rdb.Get("session:abc123")

// 不存在则设置（SETNX）—接口幂等等场景
ok, err := rdb.SetnxEx("idempotency:order:X9", "1", 86400)
if !ok {
    return nil, ErrDuplicateRequest
}

// 原子自增
count, err := rdb.Incr("stats:page:views")
```

## 分布式锁

```go
lock := redis.NewRedisLock(rdb, "order:process:12345")
lock.SetExpire(5)   // 锁超时 5 秒

acquired, err := lock.Acquire()
if !acquired {
    return nil, ErrLockNotAcquired
}
defer lock.Release()
// 临界区
```

## Hash 操作

```go
// 设置字段
err = rdb.Hset("user:42", "name", "Alice")

// 读取字段
name, err := rdb.Hget("user:42", "name")

// 获取所有字段
fields, err := rdb.Hgetall("user:42")
```

## 有序集合（排行榜、滑动窗口限流）

```go
// 添加分数
err = rdb.Zadd("leaderboard", 1500, "player:alice")

// 获取前 10（降序）
members, err := rdb.ZrevrangeWithScores("leaderboard", 0, 9)

// 滑动窗口限流：用时间戳为 score，删除过期当口
now := time.Now().UnixMilli()
_ = rdb.Zadd("rl:user:42", float64(now), fmt.Sprintf("%d", now))
_ = rdb.Zremrangebyscore("rl:user:42", "0",
    strconv.FormatInt(now-60000, 10))
count, _ := rdb.Zcard("rl:user:42")
if count > 100 {
    return nil, ErrRateLimited
}
```

## Pipeline 批量命令

```go
_, err = rdb.Pipelined(func(pipe redis.Pipeliner) error {
    pipe.Set(ctx, "k1", "v1", time.Minute)
    pipe.Set(ctx, "k2", "v2", time.Minute)
    pipe.Incr(ctx, "counter")
    return nil
})
```

## 发布 / 订阅

```go
// 发布
_ = rdb.Publish("events:order", `{"id":42,"status":"paid"}`)

// 订阅（通常在后台 goroutine 中运行）
pubsub, _ := rdb.Subscribe("events:order")
for msg := range pubsub.Channel() {
    fmt.Println(msg.Payload)
}
```

## TTL 管理

```go
// 查询剩余 TTL
ttl, err := rdb.Ttl("session:abc123")

// 刷新 TTL
_ = rdb.Expire("session:abc123", 3600)

// 移除 TTL（持久化 key）
_ = rdb.Persist("session:abc123")
```

## 健康检查

```go
if err := rdb.Ping(); err != nil {
    httpx.Error(w, err, http.StatusServiceUnavailable)
    return
}
```
