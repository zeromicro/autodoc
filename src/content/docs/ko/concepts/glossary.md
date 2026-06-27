---
title: 용어집
description: go-zero의 용어집에 대해 설명합니다.
sidebar:
  order: 8

---


## API DSL

HTTP 서비스를 정의하기 위한 go-zero의 도메인 특화 언어입니다. `.api` 파일은 라우트, 요청/응답 타입, 미들웨어 그룹을 설명합니다. `goctl api go`는 이를 완전한 Go 프로젝트로 컴파일합니다.

## Proto / RPC DSL

gRPC 서비스 계약을 정의하는 Protobuf `.proto` 파일입니다. `goctl rpc protoc`는 이를 gRPC 스텁과 go-zero 서버/클라이언트 스캐폴딩으로 컴파일합니다.

## goctl

go-zero의 명령줄 코드 생성 도구입니다. `.api` 또는 `.proto` 파일을 읽어 핸들러, 로직 스텁, 설정 구조체, 라우팅, Dockerfile을 포함한 실행 가능한 프로젝트 골격을 생성합니다.

## ServiceContext

go-zero 서비스의 단일 의존성 주입 컨테이너입니다. 시작 시 `internal/svc/servicecontext.go`에서 한 번 생성되며 데이터베이스 풀, Redis 클라이언트, 다운스트림 RPC 클라이언트와 기타 공유 리소스를 보관합니다. 모든 로직 메서드는 이 객체의 포인터를 받습니다.

## Logic Layer

비즈니스 계층입니다. `CreateOrderLogic`처럼 유스케이스마다 하나의 Go 파일을 둡니다. 로직 메서드는 타입이 지정된 요청 구조체를 받아 model/cache/RPC 계층을 호출하고 타입이 지정된 응답을 반환합니다. goctl이 다시 생성하지 않는 유일한 계층입니다.

## Handler

goctl이 생성하는 HTTP 어댑터 계층입니다. 핸들러는 들어온 요청을 디코딩하고 정확히 하나의 로직 메서드를 호출한 뒤 응답을 인코딩합니다. 비즈니스 로직을 포함해서는 안 됩니다.

## Middleware

HTTP 핸들러를 감싸 JWT 인증, 속도 제한, 요청 로깅, panic 복구, 추적 주입 같은 횡단 관심사를 추가하는 함수입니다. 전역으로는 `server.Use()`를 통해, 라우트 그룹별로는 `.api` 파일에서 등록합니다.

## Interceptor

HTTP 미들웨어에 해당하는 gRPC 개념입니다. Unary 인터셉터는 개별 RPC 호출을 감싸고, stream 인터셉터는 스트리밍 RPC를 감쌉니다. go-zero는 기본적으로 서킷 브레이킹, 추적, Prometheus 인터셉터를 등록합니다.

## zrpc

go-zero의 gRPC 클라이언트/서버 패키지입니다. `zrpc.Server`는 `grpc.Server`를 감싸 헬스 체크, Prometheus 메트릭, OpenTelemetry 추적을 추가합니다. `zrpc.Client`는 서비스 디스커버리, P2C 부하 분산, 서킷 브레이커를 추가합니다.

## P2C (Pick of Two Choices)

go-zero의 기본 클라이언트 측 부하 분산 알고리즘입니다. 각 요청마다 서비스 레지스트리에서 임의의 후보 두 개를 고른 뒤 가중 부하(in-flight × latency)가 더 낮은 쪽으로 전달합니다. 라운드 로빈에서 느린 노드에 트래픽이 몰리는 문제를 피할 수 있습니다.

## Circuit Breaker

슬라이딩 윈도우에서 오류 비율을 추적하는 탄력성 패턴입니다. 비율이 임계값을 넘으면 브레이커가 *열리고* 이후 요청은 다운스트림을 호출하지 않고 즉시 실패합니다(fast-fail). 쿨다운 이후에는 탐색 요청 하나를 허용하고, 성공하면 브레이커가 다시 *닫힙니다*.

## Rate Limiter

서비스가 초당 받을 수 있는 요청 수를 제어합니다. go-zero는 **토큰 버킷** 알고리즘을 사용합니다. 버스트 트래픽은 토큰을 소비하며, 버킷이 비면 요청은 `429`로 거부됩니다.

## Load Shedding

적응형 과부하 보호입니다. CPU 사용률이나 큐 깊이가 설정된 상한을 넘으면 go-zero는 나머지 요청에 대한 응답성을 유지하기 위해 우선순위가 낮은 요청을 버립니다. 고정된 초당 요청 수가 아니라 실제 시스템 부하에 반응한다는 점에서 속도 제한과 다릅니다.

## Telemetry / Observability

`Telemetry` 설정 블록은 서비스에 OpenTelemetry 추적을 연결합니다. go-zero는 모든 HTTP 핸들러와 RPC 메서드에 대해 자동으로 span을 만들고 서비스 경계를 넘어 trace context를 전파합니다.

## logx

go-zero의 구조화 로깅 패키지입니다. 레벨 기반 메서드(`Info`, `Error`, `Slow`), 제로 할당 JSON 출력, 컨텍스트 인식 필드 주입(trace ID, span ID), 고처리량 경로를 위한 로그 샘플링을 제공합니다.

## goctl Template

`~/.goctl/`에 저장되는 사용자 정의 코드 템플릿입니다. `goctl template init`을 실행해 기본 템플릿을 내보낸 뒤 수정하면 이후 모든 `goctl` 생성 코드의 스타일을 바꿀 수 있습니다.

## Etcd Key

서비스 디스커버리에 사용하는 서비스 레지스트리 식별자입니다. RPC 서버는 이 키 아래에 자신의 주소를 게시하고, RPC 클라이언트는 이를 watch하여 현재 살아 있는 인스턴스 목록을 얻습니다. 관례는 `<service-name>.rpc`입니다(예: `user.rpc`).

## Model Layer

`goctl model`이 생성하는 데이터 접근 계층입니다. 선택적으로 2단계 캐시(in-process LRU + Redis)를 포함한 CRUD 메서드를 제공합니다. 생성 코드는 `*_gen.go` 파일에 있고, 직접 작성한 쿼리는 goctl이 덮어쓰지 않는 별도 companion 파일에 둡니다.
