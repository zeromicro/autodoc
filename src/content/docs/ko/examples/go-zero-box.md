---
title: go-zero-box 프로젝트 템플릿
description: API, 비동기 큐, 예약 작업, CLI를 통합한 go-zero 프로젝트 템플릿입니다.
sidebar:
  order: 6
---

go-zero-box는 기본 API 예제를 넘어 비즈니스 계층, 의존성 주입, 서비스 구성을 학습하기 위한 커뮤니티 프로젝트 템플릿입니다. go-zero v1.9.4를 기반으로 API, 큐 소비자, 스케줄러를 함께 실행하거나 각각 배포할 수 있습니다.

저장소：[go-zero-box](https://github.com/prf16/go-zero-box)

## 기능

| 기능 | 구현 방식 |
| --- | --- |
| API 서비스 | 모듈별 API DSL과 로그인, 회원가입, JWT 인증 예제 |
| 큐와 예약 작업 | asynq를 사용한 큐 처리와 작업 스케줄링 |
| 명령줄 도구 | Cobra를 사용한 사용자 정의 명령 등록 및 실행 |
| 의존성 관리 | Wire로 의존성 주입 코드를 생성하고 ServiceContext로 의존성을 관리 |
| 개발 도구 | 빌드, API 코드 생성, 의존성 주입 코드 생성을 위한 Makefile 대상 |

## 코드 가져오기

```bash
git clone https://github.com/prf16/go-zero-box.git
cd go-zero-box
go mod download
```

## 사전 준비

Go 1.23.5 이상, MySQL 5.7 이상, Redis.

환경에 맞게 `app/etc/app.yaml`의 `Database`, `Redis`, `Asynqx`를 수정합니다. 인증 예제를 사용하기 전에 `JwtAuth.AccessSecret`을 직접 설정합니다. 데이터베이스 스키마는 `deploy/sql/v1.sql`, 초기화 절차는 프로젝트 README를 참고하세요.

## 서비스 시작

프로젝트 루트에서 API 서비스를 실행합니다.

```bash
go run . server:api
```

기본 설정에서는 Hello 엔드포인트와 Swagger 문서에 접근할 수 있습니다.

```bash
curl http://localhost:8001/api/hello
```

[Swagger](http://localhost:8001/api/doc)

### 다른 실행 방식

| 명령 | 용도 |
| --- | --- |
| `go run . server:queue` | 큐 소비자 시작 |
| `go run . server:scheduler` | 스케줄러 시작 |
| `go run . server:all` | API, 큐 소비자, 스케줄러 함께 실행 |
| `go run . hello:world` | 예제 명령 실행 |

## RPC 확장

RPC 서비스는 별도의 [go-zero-box-rpc](https://github.com/prf16/go-zero-box-rpc) 프로젝트에서 제공합니다. 연동하려면 `UserRpc`를 설정하고 `pkg/rpc/client.go`의 클라이언트 초기화를 확인하세요. 현재 예제에서는 초기화가 비활성화되어 있으므로 RPC 엔드포인트를 호출하기 전에 연결 설정을 완료해야 합니다.

## 핵심 학습 내용

- 비즈니스 모듈별로 API 정의, handler, logic, service를 구성합니다.
- Wire와 ServiceContext로 의존성을 관리합니다.
- HTTP 요청, 큐 작업, CLI 명령에서 비즈니스 서비스를 재사용합니다.
