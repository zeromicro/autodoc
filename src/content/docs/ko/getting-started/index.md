---
title: 시작하기
description: 환경을 준비하고 5분 안에 첫 go-zero 서비스를 실행합니다.
sidebar:
  order: 1

---


이 섹션은 빈 개발 환경에서 실행 중인 go-zero 서비스까지 안내합니다. 끝까지 진행하면 Go, goctl, 선택적으로 protoc을 설치하고 첫 HTTP API와 RPC 서비스를 실행하게 됩니다.

**예상 시간:** 전체 과정은 약 15분, Hello World만 실행하면 약 5분입니다.

## 사전 준비

| 요구 사항 | 최소 버전 | 참고 |
|---|---|---|
| Go | 1.21 | [다운로드](https://go.dev/dl/) |
| goctl | latest | go-zero 코드 생성 CLI |
| protoc | 3.x | RPC 서비스에서만 필요 |

## 권장 학습 순서

처음이라면 다음 순서대로 진행하세요.

```
1. Go 설치             →  installation/golang
2. goctl 설치          →  installation/goctl
3. protoc 설치         →  installation/protoc     (RPC 전용)
4. IDE 설정            →  installation/ide-plugins
5. API DSL 이해        →  ../reference/api-dsl
6. Hello World         →  ../guides/quickstart/hello-world   ← 바로 실행해 보고 싶다면 여기부터 시작
7. 전체 API 서비스     →  ../guides/quickstart/api-service
8. 전체 RPC 서비스     →  ../guides/quickstart/rpc-service
```

## 60초 빠른 시작

이미 Go 1.21 이상이 설치되어 있다면 다음 명령을 실행하세요.

```bash
# goctl 설치
go install github.com/zeromicro/go-zero/tools/goctl@latest

# Hello World API 골격을 만들고 실행
goctl api new greet
cd greet
go mod tidy
go run greet.go
```

다른 터미널에서 호출합니다.

```bash
curl http://localhost:8888/from/you
# {"message":"Hello you"}
```

이제 실행 중인 API 서비스가 준비되었습니다. 핸들러, 미들웨어, 데이터베이스 접근을 추가하는 방법은 [전체 API 빠른 시작](../guides/quickstart/api-service)을 이어서 확인하세요.

## goctl이 생성하는 것

`goctl api new greet`를 실행하면 프로덕션에 사용할 수 있는 완전한 구조가 만들어집니다.

```
greet/
├── etc/
│   └── greet-api.yaml      # 설정 파일
├── internal/
│   ├── config/             # 설정 구조체
│   ├── handler/            # HTTP 핸들러(자동 등록)
│   ├── logic/              # 비즈니스 로직(여기를 수정)
│   ├── middleware/         # 사용자 정의 미들웨어 훅
│   ├── svc/                # 서비스 컨텍스트(공유 의존성)
│   └── types/              # 요청/응답 타입
├── greet.go                # 진입점
└── greet.api               # DSL 원본
```

일반적으로 `internal/logic/` 아래의 파일만 수정합니다. 나머지는 `.api` 파일을 기준으로 `goctl api go`를 실행할 때마다 다시 생성됩니다.

## 다음 단계

- [Go 설치 →](./installation/golang)
- [goctl 설치 →](./installation/goctl)
- [Hello World →](../guides/quickstart/hello-world)
