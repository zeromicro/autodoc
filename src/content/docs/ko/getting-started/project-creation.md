---
title: 프로젝트 생성 방법
description: goctl로 go-zero 프로젝트를 부트스트랩하고 스캐폴딩하는 모든 방법입니다.
sidebar:
  order: 4

---


goctl은 시작 지점에 따라 프로젝트를 만드는 여러 방법을 제공합니다.

## 처음부터 만들기(대화형 스캐폴드)

새 서비스를 가장 빠르게 시작하는 방법입니다.

```bash
# HTTP API 서비스
goctl api new myservice
cd myservice && go mod tidy

# gRPC 서비스
goctl rpc new myservice
cd myservice && go mod tidy
```

goctl은 예제 `.api` / `.proto` 파일, 엔트리포인트, 설정, 스텁 로직 계층을 포함한 실행 가능한 프로젝트를 생성합니다.

## 기존 DSL 파일에서 생성하기

이미 `.api` 또는 `.proto` 파일이 있는 경우(예: 팀 간 공유 DSL) 다음처럼 생성합니다.

```bash
# .api 파일에서 생성
mkdir myservice && cd myservice
go mod init myservice
goctl api go -api myservice.api -dir .
go mod tidy

# .proto 파일에서 생성
mkdir myservice && cd myservice
go mod init myservice
goctl rpc protoc myservice.proto \
    --go_out=./pb \
    --go-grpc_out=./pb \
    --zrpc_out=.
go mod tidy
```

DSL이 별도 저장소에서 관리되는 단일 진실 공급원(source of truth)일 때 이 방식을 사용합니다.

## 기존 프로젝트 다시 생성하기

`.api` 또는 `.proto` 파일을 수정한 뒤 로직을 덮어쓰지 않고 생성 코드를 갱신할 수 있습니다.

```bash
# API 코드 다시 생성, internal/logic/ 보존
goctl api go -api myservice.api -dir .

# RPC 코드 다시 생성, internal/logic/ 보존
goctl rpc protoc myservice.proto \
    --go_out=./pb \
    --go-grpc_out=./pb \
    --zrpc_out=.
```

goctl은 `internal/logic/`에 절대 쓰지 않습니다. 그 외 핸들러, 라우트, 타입, 설정 구조체는 다시 생성됩니다.

## 사용자 정의 템플릿에서 생성하기

로깅 설정, 오류 코드, CI 설정처럼 팀 규칙을 강제하고 싶은 경우 goctl의 사용자 정의 템플릿을 사용할 수 있습니다.

```bash
# 기본 템플릿 디렉터리 초기화
goctl template init
# 템플릿 저장 위치: ~/.goctl/

# 예: logic 파일 템플릿 수정
vim ~/.goctl/api/logic.tpl

# 다음 코드 생성부터 사용자 템플릿 적용
goctl api go -api myservice.api -dir .
```

템플릿 디렉터리는 생성 결과 구조를 그대로 반영합니다. 일반적인 커스터마이징은 다음과 같습니다.

- 표준 오류 코드 import 추가
- 팀별 로깅 호출 주입
- OpenTelemetry span 생성 추가

## 보조 파일 생성하기

goctl은 Go 코드가 아닌 산출물도 생성할 수 있습니다.

```bash
# Dockerfile
goctl docker -go main.go

# Kubernetes 배포과 서비스 매니페스트
goctl kube deploy \
    -name myservice \
    -namespace prod \
    -image myregistry/myservice:v1.0.0 \
    -o deployment.yaml

# SQL DDL에서 DB 모델 계층 생성
goctl model mysql ddl \
    -src schema.sql \
    -dir internal/model

# 클라이언트 SDK
goctl api ts -api myservice.api -dir ./sdk/ts
goctl api dart -api myservice.api -dir ./sdk/dart
```

## 요약

| 방법 | 사용 시점 |
|---|---|
| `goctl api new` / `rpc new` | 새 서비스를 처음부터 시작할 때 |
| `goctl api go` / `rpc protoc` | DSL 파일이 이미 있을 때 |
| 다시 생성 | `.api` 또는 `.proto` 수정 후 |
| 사용자 정의 템플릿 | 팀 수준 관례를 강제할 때 |
| `goctl docker` / `kube` | 배포 산출물을 생성할 때 |
