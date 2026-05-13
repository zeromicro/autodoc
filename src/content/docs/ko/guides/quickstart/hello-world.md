---
title: Hello World
description: 5분 안에 첫 go-zero API 서비스를 만들고 실행합니다.
sidebar:
  order: 8
---


이 페이지는 첫 go-zero HTTP 서비스를 처음부터 만들고, 실행하고, 테스트하는 과정을 안내합니다. 전체 과정은 약 5분이면 충분합니다.

## 사전 준비

- Go 1.21 이상 설치(`go version`)
- goctl 설치(`goctl --version`)

설치하지 않았다면 [Go 설치](../../../getting-started/installation/golang)와 [goctl 설치](../../../getting-started/installation/goctl)를 먼저 확인하세요.

## 1단계 — 프로젝트 스캐폴딩

```bash
goctl api new greet
cd greet
go mod tidy
```

이 명령은 완전한 프로젝트 구조를 생성합니다.

```
greet/
├── etc/
│   └── greet-api.yaml        # 예시입니다
├── internal/
│   ├── config/
│   │   └── config.go          # 예시입니다
│   ├── handler/
│   │   ├── greethandler.go    # HTTP 관련 코드
│   │   └── routes.go          # 예시입니다
│   ├── logic/
│   │   └── greetlogic.go      # 예시입니다
│   └── svc/
│       └── servicecontext.go  # DB 예시입니다
└── greet.go                   # 예시입니다
```

## 2단계 — 생성된 DSL 확인

`greet.api`를 엽니다.

```go
type Request {
    Name string `path:"name,options=you|me"`
}

type Response {
    Message string `json:"message"`
}

service greet-api {
    @handler Greet
    get /from/:name (Request) returns (Response)
}
```

이 하나의 파일이 단일 진실 공급원입니다. `goctl`은 여기에서 모든 Go 코드를 생성했습니다.

## 3단계 — 서비스 실행

```bash
go run greet.go
```

예상 출력:

```
Starting server at 0.0.0.0:8888...
```

## 4단계 — 테스트

새 터미널을 열고 호출합니다.

```bash
curl http://localhost:8888/from/you
```

예상 응답:

```json
{"message":"Hello you"}
```

## 5단계 — 사용자 로직 추가

`internal/logic/greetlogic.go`를 열면 다음 코드가 보입니다.

```go
func (l *GreetLogic) Greet(req *types.Request) (resp *types.Response, err error) {
    // TODO: 필요한 로직을 작성하세요
    return
}
```

다음 코드로 바꿉니다.

```go
func (l *GreetLogic) Greet(req *types.Request) (resp *types.Response, err error) {
    return &types.Response{
        Message: fmt.Sprintf("Hello %s, welcome to go-zero!", req.Name),
    }, nil
}
```

필요하다면 파일 상단에 `fmt` import를 추가합니다. 저장한 뒤 다시 실행합니다.

```bash
go run greet.go
```

```bash
curl http://localhost:8888/from/alice
# Hello 예시입니다
```

## 요청 흐름

```
curl /from/alice
  → routes.go         (route matching)
  → greethandler.go   (parse + validate request)
  → greetlogic.go     (your business logic)
  → greethandler.go   (serialize response)
  → {"message":"..."}
```

사용자는 로직만 작성합니다. go-zero가 라우팅, 파싱, 검증, 직렬화, 오류 래핑을 처리합니다.

## 다음 단계

- [사용자 정의 타입으로 완전한 API 서비스 만들기 →](../api-service)
- [RPC 서비스 만들기 →](../rpc-service)
