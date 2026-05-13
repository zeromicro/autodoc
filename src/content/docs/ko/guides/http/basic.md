---
title: 기본 HTTP 서비스
description: go-zero로 REST API 서비스를 만들고 실행하는 방법입니다.
sidebar:
  order: 2

---

이 가이드는 go-zero의 API framework를 사용해 최소 HTTP 서비스를 만드는 과정을 단계별로 설명합니다.

## API 정의

`hello.api` 파일을 만듭니다.

```text
syntax = "v1"

type HelloReq {
    Name string `path:"name,options=you|me"`
}

type HelloReply {
    Message string `json:"message"`
}

service hello-api {
    @handler HelloHandler
    get /hello/:name (HelloReq) returns (HelloReply)
}
```

## 코드 생성

```bash
goctl api go -api hello.api -dir ./hello
```

생성된 구조는 다음과 같습니다.

```text
hello/
├── etc/hello-api.yaml
├── internal/
│   ├── config/config.go
│   ├── handler/hellohandler.go
│   ├── logic/hellologic.go
│   ├── svc/servicecontext.go
│   └── types/types.go
└── hello.go
```

## 로직 구현

```go title="internal/logic/hellologic.go"
func (l *HelloLogic) Hello(req *types.HelloReq) (resp *types.HelloReply, err error) {
    return &types.HelloReply{
        Message: "Hello " + req.Name,
    }, nil
}
```

## 설정

```yaml title="etc/hello-api.yaml"
Name: hello-api
Host: 0.0.0.0
Port: 8888
```

## 서버 시작

```bash
cd hello && go mod tidy && go run hello.go
```

## 테스트

```bash
curl http://localhost:8888/hello/world
# {"message":"Hello world"}
```

## 오류 처리

```go
import "github.com/zeromicro/go-zero/rest/httpx"

httpx.Error(w, errorx.NewCodeError(400, "invalid name"))
```
