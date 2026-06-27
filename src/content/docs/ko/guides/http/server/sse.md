---
title: Server-Sent Events
description: go-zero에서 SSE로 client에 데이터를 stream하는 방법입니다.
sidebar:
  order: 8

---


웹 개발에서는 실시간 업데이트가 자주 필요합니다. 실시간 주식 시세, 채팅 알림, 서버 모니터링 대시보드가 대표적인 예입니다. 실시간 통신에서는 WebSocket이 자주 언급되지만, Server-Sent Events(SSE)는 서버에서 client로 데이터를 stream할 때 더 단순한 HTTP 기반 대안이 될 수 있습니다. 이 문서에서는 고성능 Go 프레임워크인 **go-zero**로 SSE를 구현하는 방법을 실행 가능한 예제와 함께 설명합니다.

## SSE를 사용하는 이유

SSE는 HTML5에 내장된 가벼운 protocol입니다. 하나의 오래 유지되는 HTTP 연결을 통해 서버가 client로 업데이트를 push해야 하는 경우에 적합합니다. WebSocket은 양방향 통신을 제공하지만 복잡도가 더 높습니다. SSE는 단방향이며 표준 HTTP를 사용하므로 설정과 디버깅이 쉽습니다.

주요 장점은 다음과 같습니다.

- **단순함**: HTTP 위에서 `text/event-stream`을 사용합니다.
- **내장 재연결**: 연결이 끊기면 브라우저가 자동으로 재시도합니다.
- **가벼움**: 알림이나 live feed처럼 한 방향 데이터 흐름에 적합합니다.

아래에서는 go-zero를 사용해 연결된 client에 서버 시간을 1초마다 stream하는 SSE 서비스를 만들어 보겠습니다.

## 프로젝트 준비

먼저 Go가 설치되어 있는지 확인하세요(Go 1.16 이상 권장). 그런 다음 go-zero 프레임워크를 가져옵니다.

```bash
go get -u github.com/zeromicro/go-zero
```

다음 구조로 프로젝트 디렉터리를 만듭니다.

```text
sse-demo/
├── main.go          # 서버 코드
└── static/
    └── index.html   # client HTML
```

## 서버 코드

다음은 SSE 서비스를 구동하는 전체 Go 코드입니다.

```go
package main

import (
	"fmt"
	"net/http"
	"time"

	"github.com/zeromicro/go-zero/core/logx"
	"github.com/zeromicro/go-zero/rest"
)

type SseHandler struct {
	clients map[chan string]struct{}
}

func NewSseHandler() *SseHandler {
	return &SseHandler{
		clients: make(map[chan string]struct{}),
	}
}

// Serve는 SSE 연결을 처리합니다
func (h *SseHandler) Serve(w http.ResponseWriter, r *http.Request) {
	// go-zero v1.8.1 이하에서는 SSE header를 직접 설정합니다
	// v1.8.1 초과 버전에서는 아래 세 줄을 추가할 필요가 없습니다
	w.Header().Add("Content-Type", "text/event-stream")
	w.Header().Add("Cache-Control", "no-cache")
	w.Header().Add("Connection", "keep-alive")

	// 새 client를 등록합니다
	clientChan := make(chan string)
	h.clients[clientChan] = struct{}{}

	// 연결이 끊기면 정리합니다
	defer func() {
		delete(h.clients, clientChan)
		close(clientChan)
	}()

	// event를 stream합니다
	for {
		select {
		case msg := <-clientChan:
			fmt.Fprintf(w, "data: %s\n\n", msg)
			w.(http.Flusher).Flush()
		case <-r.Context().Done():
			return // client 연결이 끊겼습니다
		}
	}
}

// SimulateEvents는 주기적으로 업데이트를 push합니다
func (h *SseHandler) SimulateEvents() {
	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()

	for range ticker.C {
		message := fmt.Sprintf("Server time: %s", time.Now().Format(time.RFC3339))
		for clientChan := range h.clients {
			select {
			case clientChan <- message:
			default: // 막힌 channel은 건너뜁니다
			}
		}
	}
}

func main() {
	server := rest.MustNewServer(rest.RestConf{
		Host: "0.0.0.0",
		Port: 8080,
	}, rest.WithFileServer("/static", http.Dir("static")))
	defer server.Stop()

	sseHandler := NewSseHandler()

	// go-zero v1.8.1 이하에서는 timeout 없이 SSE endpoint를 등록합니다
	server.AddRoute(rest.Route{
		Method:  http.MethodGet,
		Path:    "/sse",
		Handler: sseHandler.Serve,
	}, rest.WithTimeout(0)) // 오래 유지되는 연결에 중요합니다

	// go-zero v1.8.1 초과 버전에서는 WithSSE를 사용합니다
	server.AddRoute(rest.Route{
		Method:  http.MethodGet,
		Path:    "/sse",
		Handler: sseHandler.Serve,
	}, rest.WithSSE())

	go sseHandler.SimulateEvents()

	logx.Info("Server starting on :8080")
	server.Start()
}
```

### 동작 방식

1. **SseHandler**
   - `map[chan string]struct{}`로 연결된 client를 추적합니다. 빈 구조체(`struct{}`)는 0 byte 타입이므로 단순 존재 여부를 기록할 때 `bool`보다 메모리 효율적입니다.
   - 각 client는 메시지를 받을 전용 channel을 가집니다.

2. **Serve 메서드**
   - `Content-Type: text/event-stream`, `Cache-Control: no-cache`, `Connection: keep-alive` 같은 SSE 전용 header를 설정합니다.
   - client channel에서 메시지를 받아 계속 전송하거나, client가 연결을 끊으면 `r.Context().Done()`을 통해 종료합니다.
   - `Flush()`를 사용해 연결 위로 데이터를 즉시 push합니다.

3. **SimulateEvents**
   - ticker를 실행해 1초마다 timestamp를 생성합니다.
   - 모든 client에 메시지를 broadcast하며, 막힌 channel은 non-blocking `select`로 건너뜁니다.

4. **main 함수**
   - 8080 포트에서 go-zero REST 서버를 설정합니다.
   - `rest.WithFileServer`로 `static` 폴더의 정적 파일(HTML client)을 제공합니다.
   - `/sse` endpoint를 `rest.WithTimeout(0)`으로 등록합니다. 이 부분은 아래에서 설명하는 중요한 세부 사항입니다.

### timeout 주의 사항

SSE는 지속 연결에 의존하지만, go-zero의 기본 요청 timeout(일반적으로 10초)이 적용되면 연결이 너무 일찍 끊어질 수 있습니다. `AddRoute`에 `rest.WithTimeout(0)`을 전달하면 timeout을 비활성화해 필요한 만큼 연결을 유지할 수 있습니다. 이 설정이 없으면 client가 예기치 않게 연결 해제되어 원하는 실시간 경험을 제공할 수 없습니다.

## client 코드

다음 내용을 `static/index.html`로 저장합니다.

```html
<!DOCTYPE html>
<html>
<head>
    <title>SSE Demo</title>
</head>
<body>
    <h1>Server-Sent Events Demo</h1>
    <div id="events"></div>

    <script>
        const eventList = document.getElementById('events');
        const source = new EventSource('/sse');

        source.onmessage = function(event) {
            const p = document.createElement('p');
            p.textContent = event.data;
            eventList.appendChild(p);
        };

        source.onerror = function() {
            console.log('Connection error');
        };
    </script>
</body>
</html>
```

이 간단한 페이지는 다음을 수행합니다.

- `EventSource`로 `/sse`에 연결합니다.
- 수신한 각 메시지를 paragraph로 추가합니다.
- 연결 오류가 발생하면 로그를 남깁니다.

HTML이 같은 서버(`/static`)에서 제공되므로 CORS 문제를 피할 수 있습니다. `Access-Control-Allow-Origin` 같은 추가 header가 필요하지 않습니다.

## 데모 실행

1. Go 코드를 `main.go`로, HTML을 `static/index.html`로 저장합니다.
2. 서버를 실행합니다.

   ```bash
   go run main.go
   ```

3. 브라우저에서 `http://localhost:8080/static/index.html`을 엽니다.
4. 1초마다 timestamp가 추가되는 것을 확인합니다.

## 팁과 요령

- **확장성**: client 수가 많다면 buffered channel이나 Redis 같은 pub/sub 시스템을 사용하세요.
- **보안**: 공개 서비스라면 `Serve`에서 header를 확인하는 방식 등으로 인증을 추가하세요.
- **사용자 정의 event**: 더 풍부한 업데이트가 필요하면 `event: type\ndata: value\n\n` 형식으로 SSE format을 확장할 수 있습니다.

## SSE 코드 생성

### 예제

goctl 1.9.0-alpha부터 SSE 샘플 코드 생성 기능이 내장되어 있습니다. SSE 코드를 생성하는 절차는 다음과 같습니다.

1. API 파일에 interface를 선언합니다. 해당 interface에는 반드시 response body가 있어야 합니다. 없으면 다음과 같은 코드 생성 오류가 발생합니다.

```plaintext
syntax error: sse-demo.api 20:7 missing response type
```

2. `@server` annotation에 `sse: true`를 선언합니다. 다음은 `sse-demo.api` 예제입니다.

```go
syntax = "v1"

type (
	SseReq {
		Body string `json:"body"`
	}
	SseResp {
		Msg string `json:"msg"`
	}
)

@server (
	sse: true
)
service sse {
	@handler sse
	post /sse/with/req (SseReq) returns (SseResp)

	@handler sseresp
	post /sse/without/resp returns (*SseResp)
}
```

3. API Go 코드를 생성하면 SSE를 지원하는 HTTP 서비스를 얻을 수 있습니다.

```bash
goctl api go --api sse-demo.api --dir .
```

### 템플릿 설명

SSE의 handler와 logic 템플릿은 일반 HTTP interface service의 handler 템플릿과 다릅니다. SSE handler 템플릿은 response body를 직접 반환하지 않고 event를 전달하는 channel(`chan`)을 사용합니다.

아래는 유사한 라우트에서 SSE 사용 여부에 따른 handler와 logic 차이를 보여 줍니다.

**handler diff**

![goctl handler diff](/resource/tutorials/http/sse_http_handler_diff.png)

**logic diff**

![goctl logic diff](/resource/tutorials/http/sse_http_logic_diff.png)

## 왜 go-zero인가요?

go-zero는 간결한 routing, 내장 정적 파일 제공, 성능 최적화 덕분에 이 예제에 잘 맞습니다. boilerplate는 줄이면서도 HTTP 계층을 직접 제어할 수 있으므로 긴 연결이 필요한 SSE 특성을 다루기에 적합합니다.

## 결론

몇십 줄의 코드만으로 go-zero 기반 실시간 SSE 서비스를 만들었습니다. 로그, 업데이트, 메트릭을 stream하든 이 접근 방식은 가볍고 안정적인 출발점이 됩니다. live CPU monitor나 chat feed처럼 여러분의 데이터로 확장해 보세요.
