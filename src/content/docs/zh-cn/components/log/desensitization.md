---
title: 日志脱敏
description: 使用 go-zero 内置的 Sensitive 接口在日志中保护敏感数据
sidebar:
  order: 3
---


在微服务架构中，日志记录是调试和监控系统的重要手段。然而，日志中常常包含用户密码、手机号、身份证号等敏感信息，一旦泄露就可能造成严重的安全问题。如何在保证日志调试功能的同时有效保护敏感数据，成为了每个开发者都需要面对的挑战。

go-zero v1.9.0 版本新增了日志脱敏功能，为开发者提供了一个优雅且易用的敏感数据保护方案。

## 问题背景

在实际开发中，我们经常遇到以下场景：

```go
type User struct {
    Name     string `json:"name"`
    Password string `json:"password"`
    Phone    string `json:"phone"`
    Email    string `json:"email"`
}

// 用户登录逻辑
func LoginHandler(ctx context.Context, req *LoginRequest) (*LoginResponse, error) {
    user := User{
        Name:     req.Username,
        Password: req.Password,
        Phone:    req.Phone,
        Email:    req.Email,
    }

    // 记录用户信息到日志，但密码等敏感信息会被记录下来
    logx.Infov(ctx, user)

    // ... 业务逻辑
}
```

在上述代码中，`logx.Infov()` 会将整个 `user` 对象记录到日志中，包括明文密码，这显然存在安全风险。

传统的解决方案通常有以下几种：

1. **手动处理**：在记录日志前手动清空敏感字段
2. **自定义日志方法**：为每种数据类型编写专门的日志记录方法
3. **使用第三方库**：依赖外部脱敏库

这些方案都存在一定的局限性：要么增加了开发负担，要么缺乏统一性，要么引入了额外的依赖。

## go-zero 的解决方案

go-zero v1.9.0 通过引入 `Sensitive` 接口，提供了一个轻量级且优雅的日志脱敏解决方案。

### 核心设计

#### Sensitive 接口

```go
// Sensitive 是一个接口，定义了在日志中脱敏敏感信息的方法。
// 通常由包含敏感数据（如密码或个人信息）的类型实现。
// Infov、Errorv、Debugv 和 Slowv 方法会调用此方法来脱敏敏感数据。
// LogField 中的值如果实现了 Sensitive 接口，也会被脱敏处理。
type Sensitive interface {
    // MaskSensitive 对日志中的敏感信息进行脱敏。
    MaskSensitive() any
}
```

这个接口设计非常简洁，只包含一个方法 `MaskSensitive()`，返回脱敏后的数据。

## 使用示例

### 基础用法

```go
type User struct {
    Name     string `json:"name"`
    Password string `json:"password"`
    Phone    string `json:"phone"`
    Email    string `json:"email"`
}

// 实现 Sensitive 接口
// 注意：(u User) 这样的值传递对值类型的对象和指针类型的对象都有效，
// 而 (u *User) 这样的指针传递只对指针类型的对象有效，对值类型的对象不生效
func (u User) MaskSensitive() any {
    return User{
        Name:     u.Name,
        Password: "******",          // 密码脱敏
        Phone:    maskPhone(u.Phone), // 手机号脱敏
        Email:    maskEmail(u.Email), // 邮箱脱敏
    }
}

// 手机号脱敏函数
func maskPhone(phone string) string {
    if len(phone) < 7 {
        return phone
    }
    return phone[:3] + "****" + phone[len(phone)-3:]
}

// 邮箱脱敏函数
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

// 使用示例
func LoginHandler(ctx context.Context, req *LoginRequest) (*LoginResponse, error) {
    user := User{
        Name:     req.Username,
        Password: req.Password,
        Phone:    req.Phone,
        Email:    req.Email,
    }

    // 现在这里会自动脱敏
    logx.Infov(ctx, user)
    // 输出: {"name":"alice","password":"******","phone":"138****234","email":"a***e@example.com"}

    // LogField 中的敏感数据也会被脱敏
    logx.Infow(ctx, "user login",
        logx.LogField{Key: "user", Value: user},
        logx.LogField{Key: "ip", Value: "192.168.1.1"},
    )
}
```

### 高级用法

#### 嵌套结构脱敏

```go
type Order struct {
    ID       string `json:"id"`
    UserInfo User   `json:"user_info"`
    Amount   int64  `json:"amount"`
}

func (o Order) MaskSensitive() any {
    return Order{
        ID:       o.ID,
        UserInfo: o.UserInfo.MaskSensitive().(User), // 嵌套脱敏
        Amount:   o.Amount,
    }
}
```

#### 切片脱敏

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

#### 条件脱敏（基于角色）

```go
type AdminUser struct {
    User
    IsAdmin bool `json:"is_admin"`
}

func (au AdminUser) MaskSensitive() any {
    if au.IsAdmin {
        // 管理员可以看到更多信息
        return AdminUser{
            User: User{
                Name:     au.Name,
                Password: "******",
                Phone:    au.Phone, // 管理员可以看到完整手机号
                Email:    maskEmail(au.Email),
            },
            IsAdmin: au.IsAdmin,
        }
    }

    // 普通用户完全脱敏
    return AdminUser{
        User:    au.User.MaskSensitive().(User),
        IsAdmin: au.IsAdmin,
    }
}
```

## 实现原理

### 日志输出层集成

```go
func output(writer io.Writer, level string, val any, fields ...LogField) {
    switch v := val.(type) {
    case Sensitive:
        val = v.MaskSensitive() // 敏感数据自动脱敏
    }

    entry := make(logEntry, len(fields)+3)
    for _, field := range fields {
        entry[field.Key] = maskSensitive(field.Value) // LogField 中的值也会脱敏
    }
    // ...
}
```

### 设计亮点

- **透明性**：对现有代码几乎无侵入，只需给类型加上接口实现
- **全面性**：不仅主要日志内容会被脱敏，LogField 中的值也会被处理
- **高效性**：Go 的接口类型断言是高效的 O(1) 操作，按需执行
- **可选项**：只有实现了 `Sensitive` 接口的类型才会执行脱敏

## 最佳实践

1. **使用值接收者** — `func (u User) MaskSensitive()` 对值类型和指针类型的对象都生效；指针接收者只对指针有效
2. **保持可读性** — 脱敏后的数据应保持一定的可读性，便于调试（如 `138****234`）
3. **代码审查** — 确保包含 PII 字段的结构体都实现了脱敏接口
4. **编写测试** — 为脱敏功能编写专门的测试用例，确认敏感字段不会出现在日志输出中
5. **统一工具函数** — 在团队公共包中定义 `maskPhone`、`maskEmail` 等标准脱敏函数

## 版本要求

日志脱敏功能需要 **go-zero ≥ v1.9.0**。

## 相关文档

- [日志组件概述](../logx/)
- [logx API 参考](../logc/)
