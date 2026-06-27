---
title: Hello World
description: 가장 작은 go-zero API 서비스를 만들고 실행하는 예제입니다.
sidebar:
  order: 2

---


이 예제는 `goctl api new`로 생성한 기본 HTTP 서비스를 실행하고 호출하는 최소 흐름을 보여 줍니다.

## 사전 준비

- Go 1.21 이상
- goctl 설치 완료

## 생성

```bash
goctl api new greet
cd greet
go mod tidy
```

## 프로젝트 구조

```text
greet/
├── etc/
│   └── greet-api.yaml
├── internal/
│   ├── config/
│   ├── handler/
│   ├── logic/
│   ├── svc/
│   └── types/
└── greet.go
```

## 실행

```bash
go run greet.go
```

## 테스트

```bash
curl http://localhost:8888/from/you
# {"message":"Hello you"}
```

## 다음 단계

- 로깅을 위해 [미들웨어](../../guides/http/server/middleware/) 추가
- [데이터베이스](../../guides/database/mysql/) 연결
