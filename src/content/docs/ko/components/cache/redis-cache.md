---
title: Redis 캐시
description: go-zero에서 Redis를 사용해 분산 read-through/write-through 캐시를 구성하는 방법입니다.
sidebar:
  order: 2
---


go-zero의 `cache` 패키지는 Redis를 감싸 read-through, write-through, cache-aside 패턴을 제공하며, singleflight를 통한 stampede 방지도 내장합니다. 캐시 계층이 있는 모든 `goctl` 생성 모델은 내부적으로 이 패키지를 사용합니다.

## 설정

```yaml title="etc/app.yaml"
Redis:
  Host: 127.0.0.1:6379
  Type: node       # 단일 인스턴스는 "node", Redis Cluster는 "cluster"를 사용합니다
  Pass: ""
```

Redis Cluster를 사용하거나 여러 캐시 노드에 가중치 기반으로 트래픽을 나누려면 다음처럼 설정합니다.

```yaml
CacheRedis:
  - Host: redis-1:6379
    Type: node
    Weight: 50
  - Host: redis-2:6379
    Type: node
    Weight: 50
```

## 초기화

```go
import (
    "github.com/zeromicro/go-zero/core/stores/cache"
    "github.com/zeromicro/go-zero/core/stores/sqlx"
)

// 단일 Redis 노드
cacheConf := cache.CacheConf{
    {RedisConf: c.Redis, Weight: 100},
}

// goctl이 생성한 모델은 이를 자동으로 연결합니다:
conn := sqlx.NewMysql(c.DataSource)
userModel := model.NewUserModel(conn, cacheConf)
```

## `Take`를 활용한 읽기 관통 방식

`Take`는 읽기 관통 방식의 핵심 연산입니다. 동작은 다음과 같습니다.

1. Redis에서 key를 조회합니다.
2. cache miss가 발생하면 loader를 실행합니다. loader는 singleflight group 안에서 실행되므로 stampede를 방지합니다.
3. 결과를 JSON으로 직렬화하고 TTL에 무작위 jitter를 더해 Redis에 저장합니다.
4. 값을 반환합니다.

```go
var user model.User
err := userModel.FindOne(ctx, userId) // goctl model은 내부적으로 Take를 호출합니다
```

생성된 모델 밖에서 직접 사용할 수도 있습니다.

```go
stats := cache.NewStat("user")         // 메트릭용 이름이 있는 stat 그룹입니다
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
loader가 `ErrNotFound`(`cache.New`에 전달한 sentinel error)를 반환하면 go-zero는 짧은 시간 동안 Redis에 placeholder를 저장합니다. 존재하지 않는 레코드에 대한 반복 조회가 캐시를 우회해 데이터베이스를 계속 두드리는 cache penetration 공격을 막기 위한 동작입니다.
:::

## 쓰기 관통 방식

데이터베이스에 쓴 직후 갱신된 객체를 Redis에 바로 기록합니다.

```go
// DB 레코드를 업데이트한 뒤:
err = c.SetWithExpire(fmt.Sprintf("user:%d", user.Id), &user, time.Hour)
```

goctl이 생성한 `Update` 메서드는 대신 `DelCacheCtx`를 호출합니다(cache-aside). 이 방식은 더 단순하고 일관성 문제가 생길 여지를 줄입니다.

```go
// goctl 생성 패턴 — 캐시를 삭제하고 다음 읽기에서 재구성하게 합니다
func (m *defaultUserModel) Update(ctx context.Context, data *User) error {
    _, err := m.ExecCtx(ctx, func(ctx context.Context, conn sqlx.SqlConn) (sql.Result, error) {
        return conn.ExecCtx(ctx, updateSql, data.Username, data.Id)
    }, m.formatPrimary(data.Id))
    return err
}
```

## 일괄 무효화

```go
// 여러 키를 원자적으로 삭제합니다
err = c.DelCtx(ctx,
    fmt.Sprintf("user:%d", id),
    fmt.Sprintf("user:name:%s", username),  // 보조 인덱스 키도 삭제합니다
)
```

## TTL과 jitter

go-zero는 모든 캐시 항목의 TTL에 기본 ±10%의 무작위 jitter를 더합니다. 같은 타입의 항목이 동시에 만료되어 데이터베이스 부하가 순간적으로 치솟는 **thundering herd at expiry** 상황을 피하기 위해서입니다.

| TTL 설정 | 실제 TTL 범위 |
|-------------|------------------|
| 1시간 | 54분 – 66분 |
| 10분 | 9분 – 11분 |

## 통계와 메트릭

`cache.Stat` 객체는 다음 값을 추적합니다.

| 카운터 | 설명 |
|---------|-------------|
| `Total` | 전체 캐시 요청 수 |
| `Hit` | 캐시 hit 수 |
| `Miss` | 캐시 miss 수 |
| `DbFails` | DB loader 오류 수 |

Prometheus로 노출하려면 다음처럼 stat을 만들면 됩니다.

```go
stats := cache.NewStat("user")
// app.yaml에 Prometheus가 설정되어 있으면
// 메트릭은 go-zero 내장 /metrics 엔드포인트로 내보냅니다
```

## 일반 Redis 명령(`Do`/`DoCtx`)(v1.10.1부터)

타입이 지정된 helper 메서드로 제공되지 않는 Redis 명령은 `Do`/`DoCtx`로 직접 보낼 수 있습니다.

```go
import "github.com/zeromicro/go-zero/core/stores/redis"

rdb := redis.MustNewRedis(redis.RedisConf{
    Host: "127.0.0.1:6379",
    Type: redis.NodeType,
})

// 임의의 Redis 명령을 실행합니다
cmd := rdb.Do(ctx, "SET", "key", "value", "EX", 3600)
if err := cmd.Err(); err != nil {
    // 오류를 처리합니다
}

// 결과를 가져옵니다
val, err := rdb.Do(ctx, "GET", "key").Text()
```

:::note
`Do`/`DoCtx`는 아직 타입이 지정된 API로 감싸지지 않은 명령을 위한 escape hatch입니다. `SetWithExpire`, `Get`처럼 타입이 지정된 메서드가 있으면 그쪽을 우선 사용하세요. 해당 메서드에는 메트릭, 추적, 일관된 오류 처리가 포함되어 있습니다.
:::

## 모범 사례

- 데이터베이스에 쓴 뒤 캐시 값을 직접 갱신하기보다 캐시 key를 **삭제**하세요(cache-aside). 캐시 쓰기와 DB 쓰기 사이의 race condition을 피할 수 있습니다.
- 신선도와 cache penetration 방어 사이의 균형을 맞추려면 **짧은 TTL + negative caching**을 함께 사용하세요.
- **hit rate**(`Hit / Total`)를 모니터링하세요. hit rate가 90%보다 낮다면 보통 TTL이 너무 짧거나 key space가 너무 큰 것입니다.
- 몇 초마다 갱신되는 write-heavy 데이터는 과도한 무효화 비용을 피하기 위해 해당 필드에 캐시를 쓰지 않는 방안도 고려하세요.
