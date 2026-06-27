---
title: 로그 비식별화
description: go-zero의 내장 Sensitive 인터페이스를 사용해 로그의 민감한 데이터를 보호합니다.
sidebar:
  order: 3
---


마이크로서비스 아키텍처에서 로깅은 디버깅과 모니터링에 필수입니다. 하지만 로그에는 비밀번호, 전화번호, 신분증 번호 같은 민감한 데이터가 포함될 수 있습니다. go-zero v1.9.0은 이 문제를 해결하기 위해 내장 로그 비식별화 기능을 도입했습니다.

## 문제

비식별화를 적용하지 않으면 구조화 로그가 민감한 필드를 실수로 노출할 수 있습니다.

```go
type User struct {
    Name     string `json:"name"`
    Password string `json:"password"`
    Phone    string `json:"phone"`
    Email    string `json:"email"`
}

func LoginHandler(ctx context.Context, req *LoginRequest) (*LoginResponse, error) {
    user := User{
        Name:     req.Username,
        Password: req.Password, // 평문 비밀번호입니다!
        Phone:    req.Phone,
        Email:    req.Email,
    }

    logx.Infov(ctx, user) // 로그에 비밀번호가 노출됩니다
    // ...
}
```

기존 우회 방법, 예를 들어 로깅 전에 필드를 직접 비우거나 타입별 로그 헬퍼를 만들거나 서드파티 라이브러리를 사용하는 방식은 모두 번거롭고 추가 의존성을 만들 수 있습니다.

## 해결책: `Sensitive` 인터페이스

go-zero는 가벼운 `Sensitive` 인터페이스를 제공합니다.

```go
type Sensitive interface {
    // MaskSensitive는 민감한 필드를 마스킹한 값의 복사본을 반환합니다.
    MaskSensitive() any
}
```

이 인터페이스를 구현한 타입은 `logx.Infov`, `logx.Errorv`, `logx.Debugv`, `logx.Slowv`, 그리고 `LogField` 값으로 출력될 때 자동으로 비식별화됩니다.

## 기본 사용법

```go
type User struct {
    Name     string `json:"name"`
    Password string `json:"password"`
    Phone    string `json:"phone"`
    Email    string `json:"email"`
}

// Sensitive 구현 — 값과 포인터 타입 모두에서 동작하도록 값 리시버를 사용합니다
func (u User) MaskSensitive() any {
    return User{
        Name:     u.Name,
        Password: "******",
        Phone:    maskPhone(u.Phone),
        Email:    maskEmail(u.Email),
    }
}

func maskPhone(phone string) string {
    if len(phone) < 7 {
        return phone
    }
    return phone[:3] + "****" + phone[len(phone)-3:]
}

func maskEmail(email string) string {
    parts := strings.Split(email, "@")
    if len(parts) != 2 {
        return email
    }
    username := parts[0]
    if len(username) <= 2 {
        return email
    }
    return username[:1] + "***" + username[len(username)-1:] + "@" + parts[1]
}

func LoginHandler(ctx context.Context, req *LoginRequest) (*LoginResponse, error) {
    user := User{
        Name:     req.Username,
        Password: req.Password,
        Phone:    req.Phone,
        Email:    req.Email,
    }

    // 자동으로 마스킹됩니다 — 비밀번호, 전화번호, 이메일이 보호됩니다
    logx.Infov(ctx, user)
    // 출력: {"name":"alice","password":"******","phone":"138****234","email":"a***e@example.com"}

    // LogField 값도 함께 마스킹됩니다
    logx.Infow(ctx, "user login",
        logx.LogField{Key: "user", Value: user},
        logx.LogField{Key: "ip", Value: "192.168.1.1"},
    )
}
```

## 고급 패턴

### 중첩 구조체 비식별화

```go
type Order struct {
    ID       string `json:"id"`
    UserInfo User   `json:"user_info"`
    Amount   int64  `json:"amount"`
}

func (o Order) MaskSensitive() any {
    return Order{
        ID:       o.ID,
        UserInfo: o.UserInfo.MaskSensitive().(User), // 중첩 타입에 위임합니다
        Amount:   o.Amount,
    }
}
```

### 슬라이스 비식별화

```go
type UserList []User

func (ul UserList) MaskSensitive() any {
    masked := make(UserList, len(ul))
    for i, user := range ul {
        masked[i] = user.MaskSensitive().(User)
    }
    return masked
}
```

### 역할 기반 마스킹

```go
type AdminUser struct {
    User
    IsAdmin bool `json:"is_admin"`
}

func (au AdminUser) MaskSensitive() any {
    if au.IsAdmin {
        // 관리자는 전체 전화번호를 볼 수 있습니다
        return AdminUser{
            User: User{
                Name:     au.Name,
                Password: "******",
                Phone:    au.Phone,
                Email:    maskEmail(au.Email),
            },
            IsAdmin: au.IsAdmin,
        }
    }
    return AdminUser{
        User:    au.User.MaskSensitive().(User),
        IsAdmin: au.IsAdmin,
    }
}
```

## 작동 방식

프레임워크는 로그 출력 경로에서 `Sensitive` 인터페이스 구현 여부를 확인합니다.

```go
func output(writer io.Writer, level string, val any, fields ...LogField) {
    switch v := val.(type) {
    case Sensitive:
        val = v.MaskSensitive() // 출력 전에 자동으로 마스킹합니다
    }

    entry := make(logEntry, len(fields)+3)
    for _, field := range fields {
        entry[field.Key] = maskSensitive(field.Value) // LogField 값도 마스킹합니다
    }
    // ...
}
```

**설계 특징:**
- **기존 코드 침투 없음** — 기존 로그 호출은 바꿀 필요가 없고 타입에 메서드만 추가하면 됩니다.
- **LogField까지 보호** — 메인 값뿐 아니라 모든 구조화 필드도 마스킹합니다.
- **O(1) 인터페이스 검사** — Go 타입 단언은 매우 효율적입니다.
- **명시적 적용** — `Sensitive`를 구현한 타입에만 적용됩니다.

## 모범 사례

1. **값 리시버 사용** — `func (u User) MaskSensitive()`는 값과 포인터 타입 모두에 동작합니다. 포인터 리시버는 포인터에만 동작합니다.
2. **마스킹 결과를 읽을 수 있게 유지** — `138****234`처럼 일부만 가리면 개인정보를 보호하면서도 디버깅에 도움이 됩니다.
3. **코드 리뷰에서 강제** — PII 필드가 있는 모든 구조체가 `Sensitive`를 구현하도록 요구합니다.
4. **비식별화 테스트 작성** — 민감한 필드가 로그 출력에 절대 나타나지 않는지 단위 테스트로 확인합니다.
5. **마스킹 헬퍼 표준화** — `maskPhone`, `maskEmail` 같은 헬퍼를 팀 공통 패키지에 정의합니다.

## 버전 요구 사항

로그 비식별화는 **go-zero ≥ v1.9.0**이 필요합니다.

## 관련 문서

- [로깅 개요](../logx/)
- [logx API](../logc/)
