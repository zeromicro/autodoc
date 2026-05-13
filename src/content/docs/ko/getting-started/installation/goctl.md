---
title: goctl 설치
description: 공식 go-zero 코드 생성 도구를 설치합니다.
sidebar:
  order: 3
---


`goctl`은 go-zero의 코드 생성 CLI입니다. `.api`와 `.proto` 파일을 읽어 반복 코드를 제거한 프로덕션 준비 Go 서비스를 생성합니다.

## 설치

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
```

## 확인

```bash
goctl --version
# goctl version 1.7.3 darwin/arm64
```

`command not found`가 표시되면 `$GOBIN`이 `PATH`에 포함되지 않은 상태입니다. 다음처럼 수정하세요.

```bash
# ~/.zshrc 또는 ~/.bashrc에 추가
export GOBIN=$(go env GOPATH)/bin
export PATH=$PATH:$GOBIN
source ~/.zshrc
```

## 업그레이드

최신 버전을 받으려면 같은 설치 명령을 다시 실행합니다.

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
goctl --version
```

## goctl로 생성할 수 있는 것

| 명령 | 출력 |
|---|---|
| `goctl api new <name>` | 완전한 HTTP API 서비스 골격 |
| `goctl api go -api f.api -dir .` | 기존 `.api` 파일에서 Go 코드 생성 |
| `goctl rpc new <name>` | 완전한 gRPC 서비스 골격 |
| `goctl rpc protoc f.proto ...` | 기존 `.proto` 파일에서 Go 코드 생성 |
| `goctl model mysql ddl -src f.sql -dir .` | SQL 스키마에서 DB 모델 계층 생성 |
| `goctl docker -go main.go` | Dockerfile |
| `goctl kube deploy ...` | Kubernetes 배포 매니페스트 |

## 다음 단계

RPC 서비스: [protoc 설치 →](../protoc)

HTTP 전용 서비스: [Hello World →](../../../guides/quickstart/hello-world)
