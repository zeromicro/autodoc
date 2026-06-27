---
title: 부하 차단
description: go-zero 서비스가 과부하 상태일 때 초과 트래픽을 자동으로 거부합니다.
sidebar:
  order: 5

---


go-zero는 CPU 사용률과 처리 중인 요청 수를 기반으로 하는 **adaptive load shedder**를 사용합니다. 시스템이 과부하 상태가 되면 새 요청을 HTTP 503 또는 gRPC `UNAVAILABLE`로 거부해 이미 처리 중인 작업을 보호합니다.

## 작동 방식

shedder는 요청을 받을지 결정할 때 두 가지 신호를 함께 사용합니다.

1. **CPU 사용률** — `/proc/stat`을 통해 250ms마다 sampling합니다. CPU가 설정한 임계값(기본 90%)을 넘으면 부하 차단이 활성화됩니다.
2. **통과율** — 최근 sliding window에서 완료된 요청 수를 전체 시도 요청 수와 비교한 rolling ratio입니다. 통과율이 계산된 하한보다 낮아지면 새 요청을 차단합니다.

이중 조건을 사용하므로 CPU가 건강한 상태에서는 요청을 차단하지 않고, CPU가 포화되면 요청량과 무관하게 차단을 수행합니다.

## HTTP 서비스

부하 차단은 모든 `rest.Server`에서 **기본으로 활성화**됩니다. YAML에서 CPU 임계값을 설정할 수 있습니다.

```yaml title="etc/app.yaml"
CpuThreshold: 900  # 90% — 단위는 millicores × 10(0-1000)입니다
```

요청이 차단되면 서버는 **HTTP 503 Service Unavailable**과 `X-Content-Type-Options: nosniff` 헤더로 응답합니다.

차단된 요청에 대한 사용자 정의 핸들러를 추가하려면 다음처럼 설정합니다.

```go
server := rest.MustNewServer(c.RestConf,
    rest.WithUnauthorizedCallback(func(w http.ResponseWriter, r *http.Request, err error) {
        // 사용자 정의 503 본문
        httpx.WriteJson(w, http.StatusServiceUnavailable, map[string]string{
            "code": "OVERLOADED",
            "msg":  "service temporarily unavailable",
        })
    }),
)
```

## gRPC 서비스

`SheddingInterceptor`는 모든 `zrpc.Server`에 **자동으로** 등록됩니다. 차단된 요청은 `codes.ResourceExhausted`(`429`)를 반환합니다.

```go
// 자동으로 등록되므로 코드 변경이 필요 없습니다.
// 차단된 요청은 다음 응답을 받습니다:
//   status.Error(codes.ResourceExhausted, "concurrent connections over threshold")
```

go-zero의 gRPC 클라이언트를 사용하는 호출자는 `zrpc.ErrResourceExhausted`를 받으며, backoff를 두고 재시도하거나 fallback을 사용할지 결정할 수 있습니다.

## 사용자 정의 shedder

HTTP가 아닌 작업, 예를 들어 message consumer를 감싸는 등 코드에서 직접 제어해야 한다면 `load.NewAdaptiveShedder`를 사용합니다.

```go
import (
    "github.com/zeromicro/go-zero/core/load"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

shedder := load.NewAdaptiveShedder(
    load.WithCpuThreshold(800),        // CPU 80%에서 활성화합니다
    load.WithWindow(5*time.Second),    // sliding window 크기
    load.WithBuckets(50),              // window bucket 수(세분성)
)

func processMessage(msg Message) error {
    promise, err := shedder.Allow()
    if err != nil {
        // 과부하 상태 — 메시지를 버리거나 큐로 되돌립니다
        metrics.Inc("messages.shed")
        return ErrOverloaded
    }

    procErr := handle(msg)

    // 중요: 항상 Pass 또는 Fail을 호출해야 합니다
    if procErr != nil {
        promise.Fail()   // 실패로 집계되어 통과율을 낮춥니다
    } else {
        promise.Pass()   // 성공으로 집계됩니다
    }
    return procErr
}
```

:::caution[항상 promise를 닫으세요]
성공한 모든 `Allow()` 호출 뒤에는 정확히 한 번의 `promise.Pass()` 또는 `promise.Fail()` 호출이 따라와야 합니다. promise가 누수되면 통과율 계산이 어긋나 부하 차단이 영구적으로 켜지거나 꺼질 수 있습니다.
:::

## 설정 참조

| 옵션 | 기본값 | 설명 |
|--------|---------|-------------|
| `WithCpuThreshold(n)` | `900` | CPU 임계값, 단위는 millicores×10(0–1000) |
| `WithWindow(d)` | `5s` | sliding window 길이 |
| `WithBuckets(n)` | `50` | window 안의 bucket 수 |

## 메트릭

Prometheus가 활성화되면 shedder는 다음 메트릭을 내보냅니다.

| 메트릭 | 타입 | 설명 |
|--------|------|-------------|
| `shedding_drops_total` | Counter | 차단된 전체 요청 수 |
| `shedding_pass_total` | Counter | 통과한 전체 요청 수 |
| `cpu_usage` | Gauge | 현재 CPU 사용률(0–1000) |

## 모범 사례

- **임계값을 서비스의 CPU 특성에 맞게 조정하세요.** Stateless 서비스는 더 높은 임계값(900–950)을 견딜 수 있지만, CPU 집약적인 서비스는 700–800을 사용하는 것이 좋습니다.
- **오류율과 함께 `shedding_drops_total`을 모니터링하세요.** drop이 급증하면 보통 트래픽 급증이나 느린 다운스트림 의존성을 의미합니다.
- **서킷 브레이커와 속도 제한기를 함께 사용하세요.** 속도 제한기는 정상 상태 부하를 제한하고, 서킷 브레이커는 비정상 의존성 호출을 막으며, 부하 차단은 프로세스 자체를 보호합니다.
- 외부 quota enforcement 계층이 없다면 프로덕션에서 부하 차단을 비활성화하지 마세요.
