---
title: Redis
description: go-zero의 Redis에 대해 설명합니다.
sidebar:
  order: 2
---


## 설정

```yaml title="etc/app.yaml"
Redis:
  Host: 127.0.0.1:6379
  Pass: ""
  Type: node        # Redis, Cluster 예시입니다
```

위한 Redis Cluster:

```yaml
Redis:
  Host: redis-master:6379   # 예시입니다
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
// 설정합니다
err := rdb.Setex("session:abc123", "userId:42", 3600)

// Get
val, err := rdb.Get("session:abc123")

// 존재하지 않을 때만 설정합니다(SETNX) — 분산 중복 제거에 사용됩니다
ok, err := rdb.SetnxEx("idempotency:order:X9", "1", 86400)
if !ok {
    return nil, ErrDuplicateRequest
}

// 원자적 증가(counter)
count, err := rdb.Incr("stats:page:views")

// 지정한 값만큼 증가합니다
count, err = rdb.IncrBy("stats:total:sales", 150)
```

## Distributed Lock

```go
lock := redis.NewRedisLock(rdb, "order:process:12345")
lock.SetExpire(5)   // TTL 예시입니다

acquired, err := lock.Acquire()
if err != nil {
    return nil, err
}
if !acquired {
    return nil, ErrLockNotAcquired
}
defer lock.Release()

// 예시입니다
```

## Hash Operations

```go
// 설정합니다
err = rdb.Hset("user:42", "name", "Alice")

// Get a field
name, err := rdb.Hget("user:42", "name")

// Get all fields
fields, err := rdb.Hgetall("user:42")

// 해시 필드를 증가시킵니다(예: 사용자별 카운터)
val, err := rdb.Hincrby("user:42", "loginCount", 1)
```

## Sorted Set (Leaderboard, 속도 윈도우)

```go
// 추가합니다
err = rdb.Zadd("leaderboard", 1500, "player:alice")

// 순위를 가져옵니다(0 기반, 오름차순)
rank, err := rdb.Zrank("leaderboard", "player:alice")

// 가져옵니다
members, err := rdb.ZrevrangeWithScores("leaderboard", 0, 9)

// 슬라이딩 윈도우 속도 제한: timestamp를 score로 추가하고 오래된 항목을 제거합니다
now := time.Now().UnixMilli()
windowStart := now - int64(60*1000)   // last 60 s
_ = rdb.Zadd("rl:user:42", float64(now), fmt.Sprintf("%d", now))
_ = rdb.Zremrangebyscore("rl:user:42", "0", strconv.FormatInt(windowStart, 10))
count, _ := rdb.Zcard("rl:user:42")
if count > 100 {
    return nil, ErrRateLimited
}
```

## 파이프라인

Send multiple 명령 에서 single round-trip:

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

// 구독자(일반적으로 백그라운드 goroutine에서 실행)
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
// 확인합니다
ttl, err := rdb.Ttl("session:abc123")   // time.Duration을 반환합니다

// Refresh, TTL 예시입니다
_ = rdb.Expire("session:abc123", 3600)

// Remove, TTL 예시입니다
_ = rdb.Persist("session:abc123")
```

## 캐시-Aside 사용하여 `collection.Cache` (L1)


```go
var product Product
err = cache.TakeCtx(ctx, &product, fmt.Sprintf("product:%d", id), func(v any) error {
    *v.(*Product) = fetchFromDB(id)
    return nil
})
```

참고: [메모리 캐시](../../../components/cache/memory-cache) 위한 전체 L1/L2 pattern.

## 연결 헬스

```go
// Ping은 연결 상태를 확인합니다(헬스 체크 핸들러에서 사용)
if err := rdb.Ping(); err != nil {
    httpx.Error(w, err, http.StatusServiceUnavailable)
    return
}
```
