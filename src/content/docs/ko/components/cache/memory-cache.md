---
title: 메모리 캐시
description: go-zero 서비스에서 사용하는 프로세스 내부 LRU/TTL 캐시입니다.
sidebar:
  order: 1
---


go-zero의 `collection.Cache`는 thread-safe하고 크기 제한이 있으며 TTL 만료와 LRU eviction을 지원하는 프로세스 내부 캐시입니다. 자주 읽히지만 자주 바뀌지 않는 데이터를 Redis 앞단의 **L1 캐시**로 둘 때 적합합니다.

## 기본 사용법

```go
import "github.com/zeromicro/go-zero/core/collection"

// 기본 TTL 1분, 최대 10,000개 항목의 캐시를 생성합니다
c := collection.NewCache(
    time.Minute,
    collection.WithLimit(10000),
)

// 값을 설정합니다(기본 TTL 사용)
c.Set("user:42", user)

// 가져오기
val, ok := c.Get("user:42")
if ok {
    return val.(*User), nil
}
// 만료되었거나 없으면 ok == false입니다
```

## 항목별 TTL

개별 항목마다 기본 TTL을 덮어쓸 수 있습니다.

```go
// 전역 TTL과 관계없이 세션을 30분 동안 캐시합니다
c.SetWithExpire("session:abc", session, 30*time.Minute)
```

## `Take`를 활용한 읽기 관통 방식

`Take`는 권장되는 접근 패턴입니다. 캐시에서 값을 가져오고, miss가 발생하면 제공한 loader를 정확히 한 번만 실행합니다. 같은 키에 대해 수백 개의 goroutine이 동시에 호출하더라도 loader는 한 번만 실행됩니다(singleflight semantics).

```go
val, err := c.Take("user:42", func() (any, error) {
    // TTL 윈도우마다 키별로 최대 한 번만 실행됩니다
    return db.QueryUserContext(ctx, 42)
})
if err != nil {
    return nil, err
}
user := val.(*User)
```

이 방식은 만료된 같은 키를 여러 goroutine이 동시에 다시 로드하려는 **cache stampede**(thundering herd) 문제를 방지합니다.

## 삭제

```go
c.Del("user:42")
```

## 생성자 옵션

| 옵션 | 기본값 | 설명 |
|--------|---------|-------------|
| `WithLimit(n)` | `nil`(제한 없음) | LRU eviction이 발생하기 전까지 보관할 수 있는 최대 항목 수 |

## TTL과 eviction 동작

- 항목은 **lazy expiration** 방식으로 만료됩니다. TTL이 지난 즉시 background goroutine이 지우는 것이 아니라, 다음 접근 시 제거됩니다.
- 항목 수가 제한을 초과하면 **least-recently-used** 항목이 즉시 제거됩니다.
- 영속성은 없습니다. 프로세스를 재시작하면 캐시는 비어 있습니다.

## L1 / L2 패턴

메모리 캐시(L1)와 Redis 캐시(L2)를 함께 사용하면 Redis 읽기 트래픽을 크게 줄일 수 있습니다.

```go
type UserRepo struct {
    l1  *collection.Cache   // 프로세스 내부 캐시, TTL 30초
    l2  cache.Cache         // Redis 기반 캐시, TTL 10분
    db  *model.UserModel
}

func (r *UserRepo) GetUser(ctx context.Context, id int64) (*User, error) {
    key := fmt.Sprintf("user:%d", id)

    // L1 적중?
    if v, ok := r.l1.Get(key); ok {
        return v.(*User), nil
    }

    // L2 적중? (Redis)
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

    // L1 채우기
    r.l1.Set(key, &user)
    return &user, nil
}

func (r *UserRepo) InvalidateUser(ctx context.Context, id int64) error {
    key := fmt.Sprintf("user:%d", id)
    r.l1.Del(key)          // 로컬 캐시에서 제거합니다
    return r.l2.Del(key)   // Redis에서 제거합니다
}
```

:::caution[L1 캐시는 프로세스별입니다]
여러 replica로 배포하면 각 인스턴스가 자기 프로세스 내부 캐시를 따로 가집니다. 데이터를 쓰거나 삭제할 때는 **Redis(L2)만 무효화**하세요. L1은 다음 읽기에서 다시 채워지거나 TTL에 따라 자연스럽게 만료됩니다.
:::

## 스레드 안전성

`collection.Cache`는 여러 goroutine에서 동시에 사용해도 안전합니다. 모든 작업은 내부적으로 read-write lock을 사용합니다.

## 사용 시점

| 시나리오 | 권장 여부 |
|----------|--------------|
| 자주 읽는 기준 데이터(설정, feature flag) | ✅ 예 |
| 요청 단위 중복 제거 | ✅ 예(`Take`) |
| 대용량 데이터셋(100MB 초과) | ❌ 아니요 — Redis를 사용하세요 |
| 인스턴스 간 일관성이 필요한 데이터 | ⚠️ 짧은 TTL과 함께 사용하세요 |
| 자주 갱신되는 데이터 | ⚠️ stale 상태를 줄이려면 TTL을 짧게 유지하세요 |
