---
title: 토큰 버킷 제한기
description: go-zero에서 토큰 버킷으로 요청 속도를 제한하는 방법입니다.
sidebar:
  order: 3

---

## limit.TokenLimiter

`TokenLimiter`는 1초 안에 발생하는 이벤트 빈도를 제어하는 속도 제한기입니다. Redis에 토큰 버킷 상태를 저장하며, Redis를 사용할 수 없을 때를 대비한 대체 처리도 제공합니다.

### 새 TokenLimiter 만들기

```go
func NewTokenLimiter(rate, burst int, store *redis.Redis, key string) *TokenLimiter
```

새 `TokenLimiter` 인스턴스를 생성해 반환합니다.

- **매개변수**:
  - `rate`: 초당 허용할 이벤트 수입니다.
  - `burst`: 순간적으로 허용할 최대 이벤트 수입니다.
  - `store`: Redis 클라이언트 인스턴스입니다.
  - `key`: Redis 저장 키를 만들 때 사용하는 문자열입니다.

- **반환값**: `TokenLimiter` 인스턴스입니다.

### Allow

```go
func (lim *TokenLimiter) Allow() bool
```

단일 이벤트 발생을 허용할지 확인합니다. `AllowN(time.Now(), 1)`의 축약형입니다.

- **반환값**: 이벤트를 허용하면 `true`, 그렇지 않으면 `false`를 반환합니다.

### AllowCtx

```go
func (lim *TokenLimiter) AllowCtx(ctx context.Context) bool
```

컨텍스트 정보를 함께 사용해 단일 이벤트 발생을 허용할지 확인합니다. `AllowNCtx(ctx, time.Now(), 1)`의 축약형입니다.

- **매개변수**:
  - `ctx`: 요청의 생명 주기를 제어하는 컨텍스트 정보입니다.

- **반환값**: 이벤트를 허용하면 `true`, 그렇지 않으면 `false`를 반환합니다.

### AllowN

```go
func (lim *TokenLimiter) AllowN(now time.Time, n int) bool
```

지정한 시점에 `n`개 이벤트 발생을 허용할지 확인합니다.

- **매개변수**:
  - `now`: 현재 시간입니다.
  - `n`: 요청한 이벤트 수입니다.

- **반환값**: 이벤트를 허용하면 `true`, 그렇지 않으면 `false`를 반환합니다.

### AllowNCtx

```go
func (lim *TokenLimiter) AllowNCtx(ctx context.Context, now time.Time, n int) bool
```

컨텍스트 정보를 함께 사용해 지정한 시점에 `n`개 이벤트 발생을 허용할지 확인합니다.

- **매개변수**:
  - `ctx`: 요청의 생명 주기를 제어하는 컨텍스트 정보입니다.
  - `now`: 현재 시간입니다.
  - `n`: 요청한 이벤트 수입니다.

- **반환값**: 이벤트를 허용하면 `true`, 그렇지 않으면 `false`를 반환합니다.

## 예제

아래 예제들은 `TokenLimiter`를 사용하는 방법을 보여 줍니다.

### 간단한 예제

```go
package main

import (
	"fmt"
	"time"

	"github.com/zeromicro/go-zero/core/limit"
	"github.com/zeromicro/go-zero/core/stores/redis"
)

func main() {
	store := redis.MustNewRedis(redis.RedisConf{Host: "localhost:6379"})
	limiter := limit.NewTokenLimiter(10, 20, store, "example-key")

	if limiter.Allow() {
		fmt.Println("Request allowed")
	} else {
		fmt.Println("Request not allowed")
	}
}
```

이 예제는 초당 최대 10개 이벤트와 순간 최대 20개 이벤트를 허용하는 `TokenLimiter`를 만듭니다. 그런 다음 `Allow` 메서드로 현재 요청을 허용할지 확인합니다.

### 컨텍스트 정보를 사용하는 예제

```go
package main

import (
	"context"
	"fmt"
	"time"

	"github.com/zeromicro/go-zero/core/limit"
	"github.com/zeromicro/go-zero/core/stores/redis"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	store := redis.MustNewRedis(redis.RedisConf{Host: "localhost:6379"})
	limiter := limit.NewTokenLimiter(5, 10, store, "example-key")

	if limiter.AllowCtx(ctx) {
		fmt.Println("Request allowed with context")
	} else {
		fmt.Println("Request not allowed with context")
	}
}
```

이 예제는 컨텍스트 정보로 요청의 생명 주기를 제어합니다. 지정한 시간 안에 허용 여부를 확인하지 못하면 `AllowCtx` 메서드는 `false`를 반환합니다.

### 여러 이벤트를 한 번에 확인하는 예제

```go
package main

import (
	"fmt"
	"time"

	"github.com/zeromicro/go-zero/core/limit"
	"github.com/zeromicro/go-zero/core/stores/redis"
)

func main() {
	store := redis.MustNewRedis(redis.RedisConf{Host: "localhost:6379"})
	limiter := limit.NewTokenLimiter(10, 20, store, "example-key")

	now := time.Now()
	requests := 3
	if limiter.AllowN(now, requests) {
		fmt.Printf("%d requests allowed at %v\n", requests, now)
	} else {
		fmt.Printf("%d requests not allowed at %v\n", requests, now)
	}
}
```

이 예제는 현재 시점에 3개의 이벤트를 허용할지 확인합니다. 허용되면 해당 정보를 출력합니다.

이 예제들을 참고하면 여러 상황에서 `TokenLimiter`로 이벤트 발생 빈도를 제한하는 방법을 이해할 수 있습니다.
