---
title: Proto DSL 참조
description: go-zero의 Proto DSL 참조에 대해 설명합니다.
sidebar:
  order: 6

---


## 최소 예제

```proto
syntax = "proto3";

package user;
option go_package = "./user";

service User {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}

message GetUserRequest {
    int64 id = 1;
}

message GetUserResponse {
    int64  id   = 1;
    string name = 2;
}

message CreateUserRequest {
    string name  = 1;
    string email = 2;
}

message CreateUserResponse {
    int64 id = 1;
}
```

## go_package Convention


```proto
option go_package = "./user";   // 예시입니다
```

## 스칼라 타입

| Proto 타입 | Go 타입 |
|---|---|
| `string` | `string` |
| `int32` | `int32` |
| `int64` | `int64` |
| `bool` | `bool` |
| `float` | `float32` |
| `double` | `float64` |
| `bytes` | `[]byte` |

## 반복 필드(slice)

```proto
message ListUsersResponse {
    repeated UserInfo users = 1;
    int64 total = 2;
}

message UserInfo {
    int64  id   = 1;
    string name = 2;
}
```

## 중첩 메시지

```proto
message CreateOrderRequest {
    int64   user_id = 1;
    Address address = 2;
}

message Address {
    string street = 1;
    string city   = 2;
    string zip    = 3;
}
```

## 열거형

```proto
enum UserStatus {
    ACTIVE   = 0;
    INACTIVE = 1;
    BANNED   = 2;
}

message UserInfo {
    int64      id     = 1;
    string     name   = 2;
    UserStatus status = 3;
}
```

## 여러 서비스

goctl 생성합니다 separate zRPC 서비스 위한 각 `service` block. Keep one 서비스 별 `.proto` 파일.

## Go 코드 생성

```bash
# 사용 예시
goctl rpc protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user \
    --zrpc_out=.

# 또는 다음 방법 사용
protoc user.proto \
    --go_out=./user \
    --go-grpc_out=./user
```

## 명명 규칙

| What | Convention | 예제 |
|---|---|---|
| Service name | PascalCase | `UserService` |
| RPC 메서드 | PascalCase | `GetUserById` |
| 메시지 name | PascalCase | `GetUserRequest` |
| 필드 name | snake_case | `user_id` |
| 패키지 name | lowercase | `package user` |


## 상세 참조

- [Proto 사양](spec/) — go-zero proto 관례
- [서비스 그룹화](services-group/) — proto 파일에서 서비스 구성
- [자주 묻는 질문](faq/) — 일반적인 질문
