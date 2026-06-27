---
title: 속도 제한기
description: token bucket rate limiting으로 go-zero 서비스의 요청 처리량을 제어합니다.
sidebar:
  order: 3

---


go-zero는 Redis를 기반으로 하는 두 가지 상호 보완적인 rate limiting primitive를 제공합니다. 부드러운 처리량 제어에는 **token bucket** 제한기를 사용하고, 고정 윈도우 quota에는 **period limiter**를 사용합니다.

## Token bucket 제한기

Token bucket은 일정한 속도로 token을 다시 채우며 짧은 burst를 허용합니다. Redis를 공유 상태 저장소로 사용하므로 여러 인스턴스에 걸쳐서도 올바르게 동작합니다.

```go
import (
    "github.com/zeromicro/go-zero/core/limit"
    "github.com/zeromicro/go-zero/core/stores/redis"
)

rds := redis.MustNewRedis(redis.RedisConf{Host: "127.0.0.1:6379", Type: "node"})
// rate=100 req/s, burst=200 tokens 설정 예시입니다
limiter := limit.NewTokenLimiter(100, 200, rds, "api:orders")

if limiter.Allow() {
    // 요청을 처리합니다
} else {
    httpx.Error(w, errorx.NewCodeError(429, "too many requests"))
}
```

### context 사용

요청 취소를 존중하려면 `AllowCtx`를 사용합니다.

```go
if limiter.AllowCtx(r.Context()) {
    // 진행합니다
}
```

### 배치 소비

한 번의 호출로 N개의 token을 소비합니다. bulk 작업이나 가중치가 있는 작업에 유용합니다.

```go
n := len(req.Items)  // 항목 수만큼 차감합니다
if limiter.AllowN(time.Now(), n) {
    // 배치를 처리합니다
}
```

## 기간 제한기(고정 윈도우)

rolling time window 안에서 최대 요청 수를 강제합니다. 사용자별 quota(예: “시간당 API 호출 1000회”)에 유용합니다.

```go
// 사용자별 시간당 1000개 요청
limiter := limit.NewPeriodLimit(3600, 1000, rds, "user:rate:")

code, err := limiter.Take("user:42")
switch code {
case limit.Allowed:
    // 할당량 이하 — 정상적으로 진행합니다
case limit.HitQuota:
    // 이 윈도우에서 마지막으로 허용된 요청이므로 호출자에게 경고합니다
case limit.OverQuota:
    // 할당량 초과 — 429를 반환합니다
}
```

### context 사용

```go
code, err := limiter.TakeCtx(r.Context(), "user:42")
```

## HTTP 미들웨어

`rest.Server`가 제공하는 모든 라우트에 제한을 적용하려면 미들웨어를 등록합니다.

```go
func RateLimitMiddleware(limiter *limit.TokenLimiter) rest.Middleware {
    return func(next http.HandlerFunc) http.HandlerFunc {
        return func(w http.ResponseWriter, r *http.Request) {
            if !limiter.AllowCtx(r.Context()) {
                http.Error(w, "too many requests", http.StatusTooManyRequests)
                return
            }
            next(w, r)
        }
    }
}

// 전역으로 등록합니다
server.Use(RateLimitMiddleware(limiter))
```

또는 `.api` 파일에서 특정 라우트 그룹에만 적용할 수 있습니다.

```text
@server (
    middleware: RateLimit
)
service user-api {
    @handler CreateUser
    post /users (CreateUserReq) returns (CreateUserResp)
}
```

## 사용자별 제한

인증된 user ID와 period limiter를 결합해 사용자별 quota를 적용합니다.

```go
func (l *CreateOrderLogic) CreateOrder(req *types.CreateOrderReq) (*types.CreateOrderResp, error) {
    key := fmt.Sprintf("user:%d", req.UserId)
    code, err := l.svcCtx.RateLimiter.Take(key)
    if err != nil || code == limit.OverQuota {
        return nil, errorx.NewCodeError(429, "rate limit exceeded")
    }
    // ... 비즈니스 로직
}
```

## Redis Cluster

두 제한기 모두 `*redis.Redis` 클라이언트를 받습니다. Redis Cluster를 사용할 때는 다음과 같이 설정합니다.

```go
rds := redis.MustNewRedis(redis.RedisConf{
    Host: "127.0.0.1:7000",
    Type: "cluster",
})
```

## 설정

제한기 설정을 `etc/app.yaml`에 저장하고 `ServiceContext`에 바인딩합니다.

```yaml title="etc/app.yaml"
RateLimit:
  Rate:  100    # 초당 token 수
  Burst: 200
  Redis:
    Host: 127.0.0.1:6379
    Type: node
```

```go title="internal/svc/servicecontext.go"
svcCtx.RateLimiter = limit.NewTokenLimiter(
    c.RateLimit.Rate,
    c.RateLimit.Burst,
    redis.MustNewRedis(c.RateLimit.Redis),
    "api:global",
)
```

## 모범 사례

- **key 세분화** — 모든 요청에 단일 global key를 쓰지 말고 route별, user별 key를 사용하세요. 한 사용자가 다른 사용자의 quota를 고갈시키는 상황을 피할 수 있습니다.
- **burst 크기 조정** — 정상 트래픽의 작은 spike를 흡수할 수 있도록 `burst`를 `rate`의 약 2배로 설정하세요.
- **fallback** — Redis를 사용할 수 없으면 `TokenLimiter`가 자동으로 프로세스 내부 제한기로 fallback하므로 서비스는 계속 실행됩니다.
- **관측** — 지속적인 rate limit 압력을 감지하려면 `OverQuota` 이벤트에 대한 Prometheus counter를 증가시키세요.
