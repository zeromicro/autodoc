---
title: 설계 원칙
description: go-zero의 설계 원칙에 대해 설명합니다.
sidebar:
  order: 5

---


## 설정보다 관례

goctl 스캐폴딩과 표준 폴더 구조는 팀마다 달라지는 구현 방식을 줄이고 협업 효율을 높입니다. go-zero 프로젝트를 다루는 모든 엔지니어는 동일한 구조를 보게 됩니다.

```text
internal/handler/   ← HTTP binding only
internal/logic/     ← business logic only
internal/svc/       ← shared dependencies
internal/model/     ← data access only
```

구조가 명확하게 정해져 있으면 코드 리뷰는 스타일 논쟁이 아니라 실제 구현 내용에 집중할 수 있습니다.

## 기본값으로 제공되는 안정성

탄력성 메커니즘은 선택적으로 붙이는 애드온이 아니라 프레임워크 기능으로 내장되어 있습니다. 서킷 브레이킹, 속도 제한, 부하 차단, 타임아웃 제어는 별도 설정 없이 자동으로 활성화됩니다.

```go
// 이 한 줄은 다음 기능으로 보호됩니다:
// P2C 예시입니다
// - 서킷 브레이커(Google SRE 스타일)
// RPC 예시입니다
// - Prometheus metrics
// - OpenTelemetry span
resp, err := l.svcCtx.OrderRpc.CreateOrder(l.ctx, req)
```

![탄력성 설계](../../../../assets/resilience-en.svg)

## 명확한 책임 경계

핸들러, 로직 모듈, 서비스 컨텍스트, 모델은 결합도를 낮추기 위해 의도적으로 분리되어 있습니다.

```go
// handler — 요청을 디코딩하고 logic만 호출합니다
func (h *CreateOrderHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    var req types.CreateOrderReq
    if err := httpx.Parse(r, &req); err != nil {
        httpx.ErrorCtx(r.Context(), w, err)
        return
    }
    l := logic.NewCreateOrderLogic(r.Context(), h.svcCtx)
    resp, err := l.CreateOrder(&req)
    httpx.OkJsonCtx(r.Context(), w, resp)
}

// logic — 비즈니스 규칙만 구현합니다
func (l *CreateOrderLogic) CreateOrder(req *types.CreateOrderReq) (*types.CreateOrderResp, error) {
    // 검증하고 model을 호출한 뒤 다운스트림 RPC를 호출합니다
    order, err := l.svcCtx.OrderModel.Insert(l.ctx, &model.Order{
        UserId:  req.UserId,
        Product: req.Product,
    })
    if err != nil {
        return nil, err
    }
    return &types.CreateOrderResp{OrderId: order.Id}, nil
}
```

이 경계는 코드 생성으로 강제됩니다. goctl은 비즈니스 로직을 핸들러에 넣지 않습니다.

## 관측 가능성 우선 실행

프로덕션 시스템에는 장애가 발생한 뒤가 아니라 첫날부터 로그, 메트릭, 추적이 필요합니다. go-zero는 모든 요청에 이 세 가지를 자동으로 주입합니다.

```go
// logx는 모든 로그 라인에 trace_id와 span_id를 자동으로 기록합니다
logx.Infow("order created", logx.Field("orderId", id))
// JSON 출력: {"level":"info","trace_id":"4bf92f35...","span_id":"00f067aa","orderId":"ord_123"}

// Prometheus 카운터는 요청/응답 코드별로 증가하며 별도 코드가 필요 없습니다
// POST 예시입니다
```

분산 추적은 `etc/user-api.yaml`에 네 줄을 추가해 활성화할 수 있습니다.

```yaml
Telemetry:
  Name: user-api
  Endpoint: localhost:4317
  Sampler: 1.0
```
