---
title: 서킷 브레이커
description: go-zero의 자동 서킷 브레이킹으로 연쇄 장애를 방지합니다.
sidebar:
  order: 2

---


go-zero는 Google SRE 스타일 서킷 브레이커를 모든 RPC 클라이언트와 HTTP 서비스에 자동으로 통합합니다. 수동 연결은 필요 없습니다.

## 작동 방식

브레이커는 sliding window 안에서 오류 비율을 추적합니다. 오류율이 임계값을 넘으면 서킷이 **열리고**, 이후 요청은 느린 upstream을 기다리지 않고 즉시 실패합니다(fast-fail). cooldown 시간이 지난 뒤에는 probe 요청 하나가 허용되며, 그 요청이 성공하면 브레이커가 다시 닫힙니다.

| 상태 | 조건 | 동작 |
|-------|-----------|-----------|
| **닫힘** | 오류율이 임계값보다 낮음 | 정상 동작하며 오류를 추적 |
| **열림** | 오류율이 임계값보다 높음 | 모든 요청을 즉시 거부 |
| **반열림** | cooldown 만료 후 | probe 요청 하나를 허용 |

이 알고리즘은 [Google SRE의 adaptive throttling](https://sre.google/sre-book/handling-overload/)을 기반으로 합니다. 거부되는 요청 수는 `max(0, (requests − K × accepts) / (requests + 1))`로 계산하며, K의 기본값은 1.5입니다.

## 자동 모드(RPC & HTTP)

코드가 필요하지 않습니다. 브레이커는 모든 `zrpc` 호출과 다운스트림 HTTP 요청에 자동으로 적용됩니다.

```go
// 서킷 브레이커, P2C 부하 분산, 타임아웃으로 자동 보호됩니다
resp, err := l.svcCtx.OrderRpc.CreateOrder(l.ctx, req)
if err != nil {
    // 열림 상태에서는 err == breaker.ErrServiceUnavailable입니다
    return nil, err
}
```

## 수동 사용

`breaker.NewBreaker()`로 데이터베이스, HTTP API, Redis 같은 외부 호출을 보호할 수 있습니다.

```go
import "github.com/zeromicro/go-zero/core/breaker"

b := breaker.NewBreaker(breaker.WithName("payment-gateway"))

// 단순 모드: nil이 아닌 모든 오류를 집계합니다
err := b.Do(func() error {
    return callPaymentAPI(req)
})
```

### DoWithFallback

서킷이 열렸을 때 graceful degradation을 위해 fallback을 제공합니다.

```go
err := b.DoWithFallback(
    func() error {
        return callPaymentAPI(req)
    },
    func(err error) error {
        // 캐시된 결과를 사용하거나 재시도 큐에 넣거나 사용자 친화적인 오류를 반환합니다
        return serveCachedResult(req)
    },
)
```

### DoWithAcceptable

어떤 오류를 실패로 집계할지 세밀하게 조정합니다. `ErrNotFound`나 `ErrUnauthorized`처럼 브레이커를 열 필요가 없는 오류를 제외할 때 유용합니다.

```go
err := b.DoWithAcceptable(
    func() error {
        return callPaymentAPI(req)
    },
    func(err error) bool {
        // true 반환 = "허용 가능한 오류이므로 브레이커 실패로 집계하지 않음"
        return errors.Is(err, ErrNotFound) || errors.Is(err, ErrUnauthorized)
    },
)
```

### DoWithFallbackAcceptable

fallback과 사용자 정의 오류 허용 규칙을 함께 사용합니다.

```go
err := b.DoWithFallbackAcceptable(fn, fallbackFn, acceptableFn)
```

## 설정

내장 브레이커는 합리적인 기본값을 사용합니다. 로그와 메트릭 label에 사용할 이름을 커스터마이징할 수 있습니다.

```go
b := breaker.NewBreaker(breaker.WithName("stripe-api"))
```

`zrpc` 클라이언트는 `etcd Key` 또는 엔드포인트 문자열을 기준으로 다운스트림 서비스마다 하나의 브레이커를 자동 생성합니다.

## Prometheus 메트릭

설정에서 Prometheus를 활성화하면 브레이커는 다음 메트릭을 내보냅니다.

| 메트릭 | 설명 |
|--------|-------------|
| `breaker_total` | 브레이커를 거친 전체 요청 수 |
| `breaker_pass` | 통과한 요청 수 |
| `breaker_drop` | 거부된 요청 수(서킷 열림) |

```yaml title="etc/app.yaml"
Prometheus:
  Host: 0.0.0.0
  Port: 9101
  Path: /metrics
```

## 모범 사례

- **브레이커에 이름을 붙이세요** — 각 브레이커에 고유한 이름을 주면 메트릭과 로그에서 장애 원인을 구분하기 쉽습니다.
- **오류를 완전히 숨기지 마세요** — 브레이커는 정확한 오류 피드백을 받아야 오류율을 계산할 수 있습니다. `Do` callback이 shadowed error가 아니라 실제 오류를 반환하는지 확인하세요.
- **검증 오류에는 `DoWithAcceptable`을 사용하세요** — 400번대 오류는 보통 다운스트림이 아니라 호출자 문제입니다. 이를 제외하면 브레이커가 다운스트림 상태를 더 정확하게 판단합니다.
- **타임아웃과 함께 사용하세요** — 브레이커는 연쇄 장애를 막지만, 느린 upstream 뒤에 goroutine이 쌓이지 않도록 각 호출에는 deadline이 필요합니다.
