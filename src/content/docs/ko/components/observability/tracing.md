---
title: 추적
description: go-zero 서비스에서 OpenTelemetry 분산 추적을 사용하는 방법입니다.
sidebar:
  order: 4

---


go-zero는 분산 추적에 OpenTelemetry를 사용합니다. 들어오는 HTTP 요청, 나가는 zrpc 호출, SQL query마다 span이 자동으로 생성되므로 일반적인 경로에서는 별도의 instrumentation 코드가 필요하지 않습니다.

:::tip
실습형 튜토리얼이 필요하다면 [분산 추적 가이드](../../guides/microservice/distributed-tracing/)에서 Jaeger 기반 단계별 안내를 확인하세요.
:::

## 설정

```yaml title="etc/app.yaml"
Telemetry:
  Name: order-api             # 추적 UI에 표시되는 서비스 이름입니다
  Endpoint: localhost:4317     # OTLP gRPC endpoint
  Sampler: 1.0                # 1.0 = 100% 샘플링입니다. 트래픽이 많은 프로덕션에서는 0.1을 사용합니다
  Batcher: otlpgrpc           # 아래 백엔드 표를 참고하세요
```

## 자동으로 추적되는 항목

| 계층 | Span 세부 정보 |
|-------|-------------|
| 들어오는 HTTP 요청 | URL, 메서드, HTTP 상태 코드 |
| 나가는 zrpc 호출 | gRPC 서비스와 메서드 이름 |
| SQL query(`sqlx` 사용) | query string, 영향받은 row 수 |
| Redis 명령 | 명령 이름, key prefix |

## 추적 전파

go-zero는 **W3C TraceContext** 표준(`traceparent` 헤더)을 사용해 서비스 간 trace context를 전파합니다. API 서비스가 RPC 서비스를 호출하면 trace ID와 span ID가 자동으로 전달되며, 전체 호출 체인이 Jaeger나 Zipkin에서 하나의 trace로 표시됩니다.

![추적 전파](../../../../../assets/trace-propagation-en.svg)

RPC 서버 쪽에는 별도 코드가 필요하지 않습니다. gRPC interceptor가 들어오는 metadata에서 context를 자동으로 추출합니다.

## 사용자 정의 span

로직 내부에 애플리케이션 수준 span을 추가할 수 있습니다.

```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/codes"
)

func (l *OrderLogic) processPayment(amount int64) error {
    tracer := otel.Tracer("order-service")
    ctx, span := tracer.Start(l.ctx, "process-payment")
    defer span.End()

    span.SetAttributes(
        attribute.Int64("amount", amount),
        attribute.String("currency", "USD"),
        attribute.String("provider", "stripe"),
    )

    if err := chargeCard(ctx, amount); err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return err
    }
    return nil
}
```

## 로그의 추적 ID

`logx`와 `Telemetry`를 함께 설정하면 go-zero가 모든 로그 라인에 trace ID와 span ID를 자동으로 주입합니다.

```json
{"level":"info","trace_id":"4bf92f3577b34da6a3ce929d0e0e4736","span_id":"00f067aa0ba902b7","msg":"order created","orderId":"ord_123"}
```

따라서 Jaeger의 특정 trace span에서 해당 요청의 로그로 바로 이동할 수 있습니다.

## 샘플링 전략

| 전략 | 설정 | 사용 시점 |
|---|---|---|
| 항상 샘플링 | `Sampler: 1.0` | 개발, staging |
| 10% 샘플링 | `Sampler: 0.1` | 트래픽이 많은 프로덕션 |
| head 기반 비율 | `Sampler: 0.01` | 처리량이 매우 높은 환경(초당 1만 요청 초과) |

비율 기반 sampler는 trace root(API gateway)에서 샘플링 여부를 결정합니다. 같은 trace의 모든 downstream span은 함께 포함되거나 함께 제외됩니다.

## 백엔드

| 백엔드 | `Batcher` 값 | endpoint 형식 |
|---------|----------------|-----------------|
| OTLP gRPC | `otlpgrpc`(기본값) | `otel-collector:4317` |
| OTLP HTTP | `otlphttp` | `http://otel-collector:4318` |
| Zipkin | `zipkin` | `http://zipkin:9411/api/v2/spans` |
| 파일 | `file` | 로컬 파일에 기록 |

:::caution
`jaeger` batcher는 OpenTelemetry Jaeger exporter가 공식적으로 deprecated되었기 때문에 **go-zero v1.10.0**에서 제거되었습니다([#5361](https://github.com/zeromicro/go-zero/pull/5361)). v1.10.0 이상에서 `Batcher: jaeger`를 사용해 업그레이드하면 서비스는 다음 오류와 함께 시작하지 못합니다.

```
value "jaeger" is not defined in options "[zipkin otlpgrpc otlphttp file]"
```

아래 [Jaeger Batcher에서 마이그레이션](#jaeger-batcher에서-마이그레이션)을 참고하세요.
:::

### OTLP를 통한 Jaeger(Docker)

Jaeger 1.35 이상은 OTLP를 기본으로 수신합니다. OTLP가 활성화된 `all-in-one` image를 사용하세요.

```bash
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
# UI: http://localhost:16686
```

```yaml title="etc/app.yaml"
Telemetry:
  Name: order-api
  Endpoint: localhost:4317
  Sampler: 1.0
  Batcher: otlpgrpc
```

### OpenTelemetry Collector

프로덕션에서는 OTel Collector를 통해 trace를 여러 백엔드로 fan-out하는 구성을 권장합니다.

```yaml title="etc/app.yaml"
Telemetry:
  Name: order-api
  Endpoint: otel-collector:4317
  Batcher: otlpgrpc
  Sampler: 0.1
```

## 추적 비활성화

모든 추적 오버헤드를 비활성화하려면 `Sampler: 0`을 설정하거나 `Telemetry` 블록을 제거합니다.

## Jaeger Batcher에서 마이그레이션

**go-zero v1.10.0**부터 `jaeger` batcher가 제거되었습니다. upstream [OpenTelemetry Jaeger exporter가 deprecated](https://opentelemetry.io/blog/2023/jaeger-exporter-collector-migration/)되었기 때문입니다. Jaeger 자체는 v1.35부터 OTLP를 native protocol로 채택했으므로, Jaeger를 계속 사용하되 exporter만 OTLP로 바꾸면 됩니다.

### 1단계: Docker Compose / Jaeger 배포 업데이트

Jaeger 인스턴스가 OTLP 포트(gRPC는 `4317`, HTTP는 `4318`)를 노출하는지 확인하세요.

```yaml title="docker-compose.yaml"
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    ports:
      - "16686:16686"   # Jaeger UI
      - "4317:4317"     # OTLP gRPC
      - "4318:4318"     # OTLP HTTP
    restart: unless-stopped
```

:::tip
호스트에서 `4317`/`4318` 포트가 다른 서비스와 충돌한다면 다른 호스트 포트(예: `34317:4317`)로 매핑하고 `Endpoint`도 그에 맞게 수정하세요.
:::

### 2단계: YAML 설정 업데이트

기존 Jaeger 전용 설정을 OTLP 설정으로 바꿉니다.

```diff
 Telemetry:
   Name: my-service
-  Endpoint: http://jaeger:14268/api/traces
-  Batcher: jaeger
+  Endpoint: jaeger:4317
+  Batcher: otlpgrpc
   Sampler: 1.0
```

또는 OTLP HTTP를 사용할 수 있습니다.

```diff
 Telemetry:
   Name: my-service
-  Endpoint: http://jaeger:14268/api/traces
-  Batcher: jaeger
+  Endpoint: http://jaeger:4318
+  Batcher: otlphttp
   Sampler: 1.0
```

### 3단계: 재시작과 확인

서비스를 재시작하고 `http://localhost:16686`에서 Jaeger UI를 엽니다. trace는 이전과 동일하게 표시되어야 하며, 달라지는 것은 전송 protocol뿐입니다.

### 빠른 참조

| 이전(< v1.10.0) | 이후(>= v1.10.0) |
|---------------------|---------------------|
| `Batcher: jaeger` | `Batcher: otlpgrpc`(권장) 또는 `otlphttp` |
| `Endpoint: http://jaeger:14268/api/traces` | `Endpoint: jaeger:4317`(gRPC) 또는 `http://jaeger:4318`(HTTP) |
| Jaeger image: 모든 버전 | Jaeger image: **1.35 이상**(native OTLP 지원) |
