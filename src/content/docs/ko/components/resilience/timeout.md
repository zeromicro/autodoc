---
title: 타임아웃
description: go-zero HTTP와 gRPC 서비스에서 요청별 deadline을 강제합니다.
sidebar:
  order: 4

---


go-zero는 느린 upstream 때문에 goroutine pool이 고갈되지 않도록 여러 계층에서 요청 타임아웃을 강제합니다.

## HTTP 서비스 타임아웃

```yaml title="etc/app.yaml"
Timeout: 3000  # 밀리초 단위(기본값: 3000)
```

이 시간을 초과한 요청은 자동으로 HTTP 408 응답을 받습니다.

## gRPC 서버 타임아웃

```yaml title="etc/rpc.yaml"
Timeout: 2000  # 밀리초 단위
```

## 클라이언트 측 타임아웃

deadline이 있는 context를 전달합니다.

```go
ctx, cancel := context.WithTimeout(l.ctx, 2*time.Second)
defer cancel()

resp, err := l.svcCtx.OrderRpc.CreateOrder(ctx, req)
```

go-zero의 `TimeoutInterceptor`는 들어온 요청의 deadline을 모든 downstream RPC 호출로 자동 전파합니다.

## 라우트별 타임아웃(HTTP)

```go
server.AddRoute(rest.Route{
    Method:  http.MethodPost,
    Path:    "/slow-endpoint",
    Handler: myHandler,
}, rest.WithTimeout(10*time.Second))
```

## 타임아웃과 context cancellation 비교

| 시나리오 | 동작 |
|----------|-----------|
| 클라이언트 연결 종료 | context가 취소되고 upstream goroutine이 종료됩니다 |
| 타임아웃 초과 | 408을 반환하며, goroutine은 작업이 끝날 때까지 계속 실행됩니다 |
| 둘 다 발생 | context cancellation이 먼저 적용됩니다 |
