---
title: 미들웨어
description: go-zero HTTP 서비스에 사용자 정의 및 내장 미들웨어를 서버 전체 또는 라우트별로 추가하는 방법입니다.
sidebar:
  order: 3

---


미들웨어는 handler에 도달하기 전에 요청을 가로채 인증, 로깅, 속도 제한, 추적 같은 cross-cutting logic을 실행할 수 있게 합니다.

## 사용자 정의 미들웨어

### 서버 전체 적용

`server.Use()`를 사용하면 모든 라우트에 미들웨어를 적용할 수 있습니다.

```go title="main.go"
func LogMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        log.Printf("-> %s %s", r.Method, r.URL.Path)
        next(w, r)
    }
}

server := rest.MustNewServer(c.RestConf)
server.Use(LogMiddleware)
```

### API spec을 통한 라우트별 적용

특정 라우트에만 적용하려면 `.api` 파일에서 `middleware`를 선언합니다.

```text
@server (
    middleware: CheckHeader
)
service user-api {
    @handler CreateUser
    post /users (CreateUserReq) returns (CreateUserResp)
}
```

goctl은 `internal/middleware/` 아래에 stub을 생성합니다.

```go title="internal/middleware/checkheadermiddleware.go"
func (m *CheckHeaderMiddleware) Handle(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        if r.Header.Get("X-App-Version") == "" {
            httpx.Error(w, errors.New("missing X-App-Version header"))
            return
        }
        next(w, r)
    }
}
```

`ServiceContext`에 등록합니다.

```go title="internal/svc/servicecontext.go"
func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:      c,
        CheckHeader: middleware.NewCheckHeaderMiddleware().Handle,
    }
}
```

## 내장 미들웨어

go-zero는 기본적으로 포괄적인 미들웨어 세트를 활성화하며, 모두 `MiddlewaresConf`로 설정할 수 있습니다.

| 미들웨어 | 목적 | 기본값 |
|---|---|---|
| `TraceHandler` | OpenTelemetry 분산 추적 | `true` |
| `LogHandler` | 구조화된 HTTP access log | `true` |
| `PrometheusHandler` | Prometheus 메트릭 | `true` |
| `RecoverHandler` | panic 복구 | `true` |
| `BreakerHandler` | 서킷 브레이커 | `true` |
| `SheddingHandler` | 부하 차단 | `true` |
| `TimeoutHandler` | 요청 timeout 강제 | `true` |
| `MaxConnsHandler` | 최대 동시 연결 수 제한 | `true` |
| `MaxBytesHandler` | 요청 본문 크기 제한 | `true` |
| `GunzipHandler` | Gzip 압축 해제 | `true` |
| `AuthorizeHandler` | JWT 인가(설정된 경우) | — |

### 내장 미들웨어 비활성화

```yaml title="etc/config.yaml"
Name: my-api
Middlewares:
  Metrics: false
  Log: false
  Prometheus: false
```

```go
type MiddlewaresConf struct {
    Trace      bool `json:",default=true"`
    Log        bool `json:",default=true"`
    Prometheus bool `json:",default=true"`
    MaxConns   bool `json:",default=true"`
    Breaker    bool `json:",default=true"`
    Shedding   bool `json:",default=true"`
    Timeout    bool `json:",default=true"`
    Recover    bool `json:",default=true"`
    Metrics    bool `json:",default=true"`
    MaxBytes   bool `json:",default=true"`
    Gunzip     bool `json:",default=true"`
}
```

### TraceHandler

OpenTelemetry와 통합합니다. Jaeger로 trace를 내보내려면 다음처럼 설정합니다.

```yaml title="etc/config.yaml"
Telemetry:
  Name: my-service
  Endpoint: localhost:4317
  Batcher: otlpgrpc
  Sampler: 1.0
```

기본 span에는 `http.host`, `http.method`, `http.route`, `http.status_code`가 포함됩니다.

### LogHandler

모든 요청은 구조화된 JSON access log를 남깁니다.

```json
{
  "@timestamp": "2024-01-01T10:00:00.000+08:00",
  "content": "[HTTP] 200 - GET /hello - 127.0.0.1:51499",
  "duration": "1.2ms",
  "level": "info"
}
```

### PrometheusHandler

두 가지 메트릭을 내보냅니다.

| 메트릭 | 타입 | label |
|---|---|---|
| `http_server_requests_duration_ms` | Histogram(bucket: 5,10,25,50,100,250,500,1000ms) | `path` |
| `http_server_requests_code_total` | Counter | `path`, `code` |

### MaxConnsHandler

동시 HTTP 연결 수를 제한합니다. 제한을 초과하면 `503 Service Unavailable`을 반환합니다. 기본값은 10,000입니다.
