---
title: Log Desensitization
description: Protect sensitive data in logs using go-zero's built-in Sensitive interface
sidebar:
  order: 3
---


In microservice architectures, logging is essential for debugging and monitoring. However, logs often contain sensitive data such as passwords, phone numbers, or ID numbers. go-zero v1.9.0 introduced a built-in log desensitization feature that elegantly solves this problem.

## The Problem

Without desensitization, structured logging can accidentally expose sensitive fields:

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
        Password: req.Password, // plaintext password!
        Phone:    req.Phone,
        Email:    req.Email,
    }

    logx.Infov(ctx, user) // exposes password in logs
    // ...
}
```

Traditional workarounds — manually nulling fields before logging, per-type log helpers, or third-party libraries — all add friction or introduce dependencies.

## The Solution: `Sensitive` Interface

go-zero provides a lightweight `Sensitive` interface:

```go
type Sensitive interface {
    // MaskSensitive returns a copy of the value with sensitive fields masked.
    MaskSensitive() any
}
```

Any type implementing this interface will be automatically desensitized by `logx.Infov`, `logx.Errorv`, `logx.Debugv`, `logx.Slowv`, and `LogField` values.

## Basic Usage

```go
type User struct {
    Name     string `json:"name"`
    Password string `json:"password"`
    Phone    string `json:"phone"`
    Email    string `json:"email"`
}

// Implement Sensitive — use value receiver so it works for both value and pointer types
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

    // Automatically masked — password, phone, and email are protected
    logx.Infov(ctx, user)
    // Output: {"name":"alice","password":"******","phone":"138****234","email":"a***e@example.com"}

    // LogField values are also masked
    logx.Infow(ctx, "user login",
        logx.LogField{Key: "user", Value: user},
        logx.LogField{Key: "ip", Value: "192.168.1.1"},
    )
}
```

## Advanced Patterns

### Nested Struct Desensitization

```go
type Order struct {
    ID       string `json:"id"`
    UserInfo User   `json:"user_info"`
    Amount   int64  `json:"amount"`
}

func (o Order) MaskSensitive() any {
    return Order{
        ID:       o.ID,
        UserInfo: o.UserInfo.MaskSensitive().(User), // delegate to nested type
        Amount:   o.Amount,
    }
}
```

### Slice Desensitization

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

### Role-Based Masking

```go
type AdminUser struct {
    User
    IsAdmin bool `json:"is_admin"`
}

func (au AdminUser) MaskSensitive() any {
    if au.IsAdmin {
        // Admins see full phone number
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

## How It Works

The framework checks for the `Sensitive` interface in the log output path:

```go
func output(writer io.Writer, level string, val any, fields ...LogField) {
    switch v := val.(type) {
    case Sensitive:
        val = v.MaskSensitive() // auto-mask before output
    }

    entry := make(logEntry, len(fields)+3)
    for _, field := range fields {
        entry[field.Key] = maskSensitive(field.Value) // mask LogField values too
    }
    // ...
}
```

**Design highlights:**
- **Zero intrusion** — existing log calls need no changes, only the type changes
- **Covers LogField** — not just the main value, but all structured fields
- **O(1) interface check** — Go type assertions are highly efficient
- **Opt-in** — only types implementing `Sensitive` are affected

## Best Practices

1. **Use value receivers** — `func (u User) MaskSensitive()` works for both value and pointer types. A pointer receiver only works for pointers.
2. **Keep masked output readable** — partial masking (e.g., `138****234`) aids debugging while protecting privacy.
3. **Enforce in code review** — require all structs with PII fields to implement `Sensitive`.
4. **Test desensitization** — write unit tests confirming that sensitive fields never appear in log output.
5. **Standardize mask helpers** — define shared `maskPhone`, `maskEmail`, etc. in a team-wide package.

## Version Requirement

Log desensitization requires **go-zero ≥ v1.9.0**.

## Related

- [Logging Overview](./logx.md)
- [logx API](./logc.md)
