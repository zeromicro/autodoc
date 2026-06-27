---
title: 아키텍처
description: go-zero의 아키텍처에 대해 설명합니다.
sidebar:
  order: 2

---


go-zero는 각 계층을 얇고 교체 가능하게 유지하면서 관심사를 분리하도록 설계된 클라우드 네이티브 마이크로서비스 프레임워크입니다.

## 1. 시스템 개요

![go-zero 시스템 아키텍처](../../../../assets/arch-overview-en.svg)

## 2. HTTP 요청 수명 주기

들어오는 모든 HTTP 요청은 비즈니스 로직에 도달하기 전에 고정된 파이프라인을 통과합니다.

![HTTP 요청 수명 주기](../../../../assets/arch-lifecycle-en.svg)

**각 계층의 역할:**

| 계층 | 컴포넌트 | 목적 |
|---|---|---|
| Timeout | `TimeoutHandler` | 요청별 마감 시간 적용(설정: `Timeout`) |
| Load shedding | `SheddingHandler` | CPU가 임계값을 넘으면 요청 거부 |
| Rate limiting | `RateLimitHandler` | 라우트별 토큰 버킷 속도 제한 |
| Middleware | 사용자 코드 | 인증, 로깅, CORS 등 |
| Handler | 생성 코드 | 요청 언마샬링 → Logic 호출 |
| Logic | 사용자 코드 | 비즈니스 규칙, DB/RPC 호출 |

## 3. 미들웨어 체인 실행 순서

![미들웨어 체인 실행 순서](../../../../assets/arch-middleware-en.svg)

서버 전체 미들웨어는 `server.Use(...)`로 등록되며 모든 요청에 실행됩니다. 라우트별 미들웨어는 `.api` 파일의 `@server` 블록에 선언되고 `ServiceContext` 안으로 생성됩니다. 내장 안전 핸들러는 사용자 핸들러 코드 직전에 항상 마지막으로 실행됩니다.

## 4. API 게이트웨이 → RPC 연결

goctl은 HTTP 계층과 RPC 클라이언트 사이의 연결 코드를 모두 생성합니다.

![API 게이트웨이와 RPC 연결](../../../../assets/arch-gateway-rpc-en.svg)

`ServiceContext`는 의존성 주입 컨테이너입니다. 모든 RPC 클라이언트, DB 연결, 캐시 참조, 설정을 보관합니다. 핸들러 계층과 로직 계층은 포인터를 통해 같은 `ServiceContext`를 공유합니다.

## 5. 탄력성: 속도 제한과 서킷 브레이킹

![탄력성: 속도 제한과 서킷 브레이킹](../../../../assets/arch-resilience-en.svg)

go-zero의 서킷 브레이커는 **슬라이딩 윈도우** 실패 카운터를 사용합니다. 최근 10초 동안의 오류 비율이 설정된 임계값(기본값: 50%)을 넘으면 브레이커가 열립니다. 반상태에서는 하나의 탐색 요청만 통과시킵니다.

**설정:**

```yaml
# Automatically, HTTP 관련 코드
# No 예시입니다
```

## 6. 관측 가능성 파이프라인

go-zero는 모든 계층을 자동으로 계측합니다.

![관측 가능성 파이프라인](../../../../assets/arch-observability-en.svg)

**활성화:**

```yaml title="etc/app.yaml"
# Structured 예시입니다
Log:
  ServiceName: order-api
  Mode: file          # 예시입니다
  Level: info
  Encoding: json

# Metrics
Prometheus:
  Host: 0.0.0.0
  Port: 9101
  Path: /metrics

# Distributed 예시입니다
Telemetry:
  Name: order-api
  Endpoint: localhost:4317
  Sampler: 1.0        # 1.0 = 100% sampling
  Batcher: otlpgrpc
```

모든 로그에는 Jaeger 추적과 연결할 수 있는 `trace_id`, `span_id` 필드가 포함됩니다. 별도의 수동 계측은 필요하지 않습니다.

## 다음 단계

- [설계 원칙](../design-principles) — go-zero가 이러한 계층을 어떻게 강제하는지 설명합니다.
- [분산 추적 튜토리얼](../../guides/microservice/distributed-tracing) — Jaeger 설정을 직접 따라 해 봅니다.
- [서킷 브레이커 컴포넌트](../../components/resilience/circuit-breaker) — 설정 참조 문서입니다.
