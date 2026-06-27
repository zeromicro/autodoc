---
title: 기간 제한기
description: go-zero에서 일정 기간당 요청 수를 제한하는 방법입니다.
sidebar:
  order: 2

---


`limit.PeriodLimit`는 주로 특정 기간 안의 요청 수를 제한하는 데 사용합니다. Redis를 기반으로 구현되어 있으며 Lua script를 통해 rate limiting 작업을 수행합니다.

## 상수

```go
const (
    // Unknown은 초기화되지 않은 상태를 의미합니다.
    Unknown = iota
    // Allowed는 허용된 상태를 의미합니다.
    Allowed
    // HitQuota는 이 요청이 정확히 할당량에 도달했음을 의미합니다.
    HitQuota
    // OverQuota는 할당량을 초과했음을 의미합니다.
    OverQuota
)
```

## 변수

```go
var (
    // ErrUnknownCode는 알 수 없는 상태 코드를 나타내는 오류입니다.
    ErrUnknownCode = errors.New("unknown status code")
)
```

## 타입

### PeriodLimit

`PeriodLimit`는 특정 기간 동안 요청을 제한하는 데 사용합니다.

### PeriodOption

`PeriodOption`은 `PeriodLimit`을 커스터마이징하는 메서드를 정의합니다.

## 함수

### NewPeriodLimit

새 `PeriodLimit` 인스턴스를 생성합니다.

```go
func NewPeriodLimit(period, quota int, limitStore *redis.Redis, keyPrefix string, opts ...PeriodOption) *PeriodLimit
```

#### 매개변수

- `period`: rate limit을 적용할 기간입니다. 단위는 초입니다.
- `quota`: 지정한 기간 안에서 허용할 최대 요청 수입니다.
- `limitStore`: 제한 상태를 저장하는 Redis 인스턴스입니다.
- `keyPrefix`: Redis key를 구분하기 위한 prefix입니다.
- `opts`: `PeriodLimit` 인스턴스에 적용할 선택 커스터마이징 옵션입니다.

### 예제

```go
package main

import (
    "fmt"
    "github.com/zeromicro/go-zero/core/limit"
    "github.com/zeromicro/go-zero/core/stores/redis"
)

func main() {
    store := redis.MustNewRedis(redis.RedisConf{Host: "localhost:6379"})
    limiter := limit.NewPeriodLimit(60, 10, store, "exampleKey")

    result, err := limiter.Take("user1")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }

    switch result {
    case limit.Allowed:
        fmt.Println("Request allowed")
    case limit.HitQuota:
        fmt.Println("Hit the quota")
    case limit.OverQuota:
        fmt.Println("Over the quota")
    default:
        fmt.Println("Unknown status")
    }
}
```

### Take

요청 허용 여부를 확인하고 허용 상태를 반환합니다.

```go
func (h *PeriodLimit) Take(key string) (int, error)
```

#### 매개변수

- `key`: 요청자를 식별하는 key입니다. 일반적으로 요청을 보내는 client나 user의 고유 식별자를 사용합니다.

#### 반환

- 허용 상태를 나타내는 정수입니다(`Allowed`, `HitQuota`, `OverQuota`, `Unknown` 중 하나).
- 요청 처리 중 문제가 발생하면 오류를 반환합니다.

### TakeCtx

context와 함께 요청 허용 여부를 확인하고 허용 상태를 반환합니다.

```go
func (h *PeriodLimit) TakeCtx(ctx context.Context, key string) (int, error)
```

#### 매개변수

- `ctx`: 함수 실행을 제어하는 context입니다. timeout과 cancellation 처리에 유용합니다.
- `key`: 요청자를 식별하는 key입니다. 일반적으로 요청을 보내는 client나 user의 고유 식별자를 사용합니다.

#### 반환

- 허용 상태를 나타내는 정수입니다(`Allowed`, `HitQuota`, `OverQuota`, `Unknown` 중 하나).
- 요청 처리 중 문제가 발생하면 오류를 반환합니다.

### Align

시간 기간을 정렬하는 `PeriodOption`을 반환합니다.

```go
func Align() PeriodOption
```

#### 반환

- `PeriodLimit`의 시간 기간을 정렬하도록 설정하는 `PeriodOption`입니다. 예를 들어 하루의 시작 시점에 맞춰 정렬할 수 있습니다.

### 예제

```go
package main

import (
    "fmt"
    "github.com/zeromicro/go-zero/core/limit"
    "github.com/zeromicro/go-zero/core/stores/redis"
)

func main() {
    store := redis.MustNewRedis(redis.RedisConf{Host: "localhost:6379"})
    limiter := limit.NewPeriodLimit(86400, 5, store, "sms_limit", limit.Align())

    result, err := limiter.Take("user1")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }

    switch result {
    case limit.Allowed:
        fmt.Println("SMS request allowed")
    case limit.HitQuota:
        fmt.Println("Hit the daily quota")
    case limit.OverQuota:
        fmt.Println("Over the daily quota")
    default:
        fmt.Println("Unknown status")
    }
}
```
