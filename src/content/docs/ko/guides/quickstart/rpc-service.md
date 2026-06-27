---
title: RPC 서비스 만들기
description: go-zero로 gRPC 서비스를 만들고 API 게이트웨이에 연결합니다.
sidebar:
  order: 10
---


이 가이드는 API 게이트웨이가 gRPC로 호출할 수 있는 **user RPC service**를 만듭니다.

## 사전 준비

- `protoc` 설치
- `protoc-gen-go`, `protoc-gen-go-grpc` 설치

설치하지 않았다면 [protoc 설치](../../../getting-started/installation/protoc)를 확인하세요.

## 1단계 — 서비스 스캐폴딩

```bash
goctl rpc new user
cd user
go mod tidy
```

Goctl은 `.proto` 파일과 전체 서비스 골격을 생성합니다.

```
user/
├── etc/
│   └── user.yaml
├── internal/
│   ├── config/config.go
│   ├── logic/
│   │   └── getuserlogic.go      # 예시입니다
│   ├── server/userserver.go   # 예시입니다
│   └── svc/servicecontext.go
├── user/
│   └── user.pb.go             # 예시입니다
│   └── user_grpc.pb.go        # 예시입니다
├── user.go                  # entrypoint
└── user.proto               # 예시입니다
```

## 2단계 — 생성된 Proto 확인

`user.proto`를 엽니다.

```proto
syntax = "proto3";

package user;
option go_package = "./user";

service User {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
}

message GetUserRequest {
    int64 id = 1;
}

message GetUserResponse {
    int64 id = 1;
    string name = 2;
}
```

## 3단계 — 비즈니스 로직 구현

`internal/logic/getuserlogic.go`를 수정합니다.

```go
func (l *GetUserLogic) GetUser(in *user.GetUserRequest) (*user.GetUserResponse, error) {
    // In, DB 예시입니다
    return &user.GetUserResponse{
        Id:   in.Id,
        Name: "alice",
    }, nil
}
```

## 4단계 — 설정과 실행

`etc/user.yaml`을 엽니다. 기본 포트는 `8080`입니다.

```yaml
Name: user.rpc
ListenOn: 0.0.0.0:8080
```

RPC 서버를 실행합니다.

```bash
go run user.go
# 시작합니다
```

## 5단계 — API 서비스에서 호출하기

API 게이트웨이가 사용할 RPC 클라이언트 스텁을 생성합니다.

```bash
goctl rpc protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user \
    --zrpc_out=./client
```

API 서비스의 `servicecontext.go`에 다음 클라이언트를 주입합니다.

```go
UserRpc userclient.User  // 예시입니다
```

그다음 로직 파일에서 호출합니다.

```go
resp, err := l.svcCtx.UserRpc.GetUser(l.ctx, &user.GetUserRequest{Id: 1})
```

go-zero는 연결 풀링, 부하 분산, 서킷 브레이킹을 자동으로 처리합니다.

## Proto 변경 후 다시 생성하기

```bash
goctl rpc protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user \
    --zrpc_out=.
```

## 다음 단계

- [etcd를 사용하여 서비스 디스커버리](../../microservice/service-discovery)
- [서킷 브레이커 설정](../../../components/resilience/circuit-breaker)
- [프로젝트 생성 패턴](../../../getting-started/project-creation)
