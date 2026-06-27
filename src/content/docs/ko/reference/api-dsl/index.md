---
title: API DSL 참조
description: go-zero의 API DSL 참조에 대해 설명합니다.
sidebar:
  order: 5

---


## 파일 구조

```go
syntax = "v1"         // 예시입니다

info (                 // 예시입니다
    title: "User API"
    version: "1.0"
)

import "shared.api"   // 예시입니다

type (...)             // 예시입니다

service name-api {     // 예시입니다
    @server (...)
    @handler HandlerName
    method /path (RequestType) returns (ResponseType)
}
```

## 타입 Definitions


```go
type (
    LoginReq {
        Username string `json:"username"`
        Password string `json:"password"`
    }

    LoginResp {
        Token   string `json:"token"`
        Expires int64  `json:"expires"`
    }

    // 경로 매개변수
    UserReq {
        Id int64 `path:"id"`
    }

    // 쿼리 매개변수
    SearchReq {
        Keyword string `form:"keyword"`
        Page    int    `form:"page,default=1"`
    }
)
```

### 태그 타입

| Tag | Source | 예제 |
|---|---|---|
| `json` | Request/response 본문 (POST/PUT) | `json:"username"` |
| `path` | URL 경로 매개변수 | `path:"id"` |
| `form` | URL query string (GET) | `form:"page,default=1"` |
| `header` | HTTP Request 헤더 | `header:"Authorization"` |

### 선택 필드


```go
type SearchReq {
    Keyword string `form:"keyword"`
    Page    int    `form:"page,optional"`
    Size    int    `form:"size,default=20"`
}
```

## 서비스 블록

```go
service user-api {
    @server (
        jwt:         Auth             // JWT 인증 설정
        middleware:  AccessLog,Cors   // 예시입니다
        prefix:      /v1              // URL 접두사
        timeout:     3s               // 예시입니다
    )

    @handler Login
    post /user/login (LoginReq) returns (LoginResp)

    @handler GetUser
    get /user/:id (UserReq) returns (UserResp)

    @handler DeleteUser
    delete /user/:id (UserReq)        // 예시입니다
}
```

### HTTP 메서드

`get` / `post` / `put` / `patch` / `delete` / `head`

### 여러 서비스 블록

Group 라우트 통해 인증 requirement:

```go
service user-api {
    // 공개 라우트
    @handler Login
    post /user/login (LoginReq) returns (LoginResp)
}

service user-api {
    @server (
        jwt: Auth
    )

    // JWT가 필요한 비공개 라우트
    @handler GetProfile
    get /user/profile () returns (ProfileResp)
}
```

## import

Split 큰 APIs 전반에 파일:

```go
// main.api
syntax = "v1"

import (
    "user.api"
    "order.api"
)
```


## 완전한 예제

```go
syntax = "v1"

type (
    RegisterReq {
        Username string `json:"username"`
        Password string `json:"password"`
        Email    string `json:"email"`
    }

    RegisterResp {
        Id int64 `json:"id"`
    }

    UserInfoReq {
        Id int64 `path:"id"`
    }

    UserInfoResp {
        Id       int64  `json:"id"`
        Username string `json:"username"`
    }
)

service user-api {
    @handler Register
    post /user/register (RegisterReq) returns (RegisterResp)
}

service user-api {
    @server (
        jwt:    Auth
        prefix: /api/v1
    )

    @handler GetUserInfo
    get /user/:id (UserInfoReq) returns (UserInfoResp)
}
```

생성:

```bash
goctl api go -api user.api -dir .
```

## 상세 참조

- [라우트 규칙](route-rule/) — URL 패턴, 메서드, 핸들러 정의
- [라우트 그룹](route-group/) — 공유 설정으로 라우트 구성
- [라우트 접두사](route-prefix/) — 그룹에 URL 접두사 추가
- [매개변수](parameter/) — 요청/응답 필드 타입과 태그
- [타입](type/) — 공유 요청/응답 구조체 정의
- [JWT 인증](jwt/) — JWT로 라우트 보호
- [미들웨어](middleware/) — 라우트에 전처리/후처리 적용
- [요청 서명](signature/) — HMAC 서명 검증
- [Import](import/) — import로 `.api` 파일 분리
- [SSE 라우트](route-sse/) — Server-Sent Events 엔드포인트
- [자주 묻는 질문](faq/) — 일반적인 질문과 답변
