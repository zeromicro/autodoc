---
title: SSE 라우트
description: go-zero의 SSE 라우트에 대해 설명합니다.
sidebar:
  order: 11

---


## 개요


## 사용법

### SSE 지원

```api
syntax = "v1"

type EventMessage {
    Type string `json:"type"`
    Data string `json:"data"`
}

@server (
    sse: true
    prefix: /api/v1
)
service EventApi {
    @handler StreamEvents
    get /events returns (EventMessage)
}
```

## 생성된 코드

때 `sse: true` is specified, goctl 생성합니다 라우트 사용하여 `rest.WithSSE()` 옵션:

```go
server.AddRoutes(
    []rest.Route{
        {
            Method:  http.MethodGet,
            Path:    "/events",
            Handler: StreamEventsHandler(serverCtx),
        },
    },
    rest.WithPrefix("/api/v1"),
    rest.WithSSE(),
)
```

## 구현 세부 사항

 `rest.WithSSE()` 옵션 자동으로:

1. Sets proper SSE 헤더 (`Content-Type: text/event-stream`, `Cache-Control: no-cache`, etc.)
2. 제거합니다 write 타임아웃 로 allow long-running 연결
3. 활성화합니다 연결 keep-alive

## Notes

- SSE 라우트 should typically 사용 `GET` 메서드
- 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.
- SSE 작동합니다 well 사용하여 JWT 인증과 미들웨어
