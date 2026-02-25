---
title: 数据库读写分离
description: 使用 go-zero 实现主从数据库读写分离，提升系统吞吐量
sidebar:
  order: 4
---


在高并发的现代应用中，数据库往往成为系统的瓶颈。读写分离作为一种有效的数据库优化策略，能够显著提升系统的性能和可用性。

go-zero 框架内置了读写分离支持，提供自动路由、可配置负载均衡和基于 context 的显式控制。

## 使用场景

**适用情况：**
- 读写比例高（如电商商品浏览、内容平台、社交媒体）
- 主库写入压力大
- 需要水平扩展读能力

**路由规则：**
| 操作 | 默认路由 |
|------|---------|
| `INSERT`、`UPDATE`、`DELETE` | 主库（Master） |
| `SELECT`（普通查询） | 从库（Replica） |
| `SELECT`（强一致性要求） | 主库，使用 `sqlx.WithReadPrimary` |

## 配置读写分离

```yaml
# config.yaml
DB:
  DataSource: "user:password@tcp(master:3306)/database"
  DriverName: mysql        # 默认值，可不写
  Policy: "round-robin"   # 负载均衡策略：round-robin 或 random，默认 round-robin
  Replicas:
    - "user:password@tcp(replica1:3306)/database"
    - "user:password@tcp(replica2:3306)/database"
    - "user:password@tcp(replica3:3306)/database"
```

```go
package config

import "github.com/zeromicro/go-zero/core/stores/sqlx"

type Config struct {
    DB sqlx.SqlConf
}
```

## 初始化数据库连接

```go
var c Config
conf.MustLoad("config.yaml", &c)

// 创建支持读写分离的数据库连接
conn := sqlx.MustNewConn(c.DB)
```

## 模型层实现

```go
type UserModel struct {
    conn sqlx.SqlConn
}

// FindUser — 默认路由到从库
func (m *UserModel) FindUser(ctx context.Context, id int64) (*User, error) {
    var user User
    err := m.conn.QueryRowCtx(ctx, &user, "SELECT * FROM users WHERE id = ?", id)
    if err != nil {
        if err == sql.ErrNoRows {
            return nil, fmt.Errorf("user not found")
        }
        return nil, err
    }
    return &user, nil
}

// FindUserFromPrimary — 强制从主库查询（强一致性）
func (m *UserModel) FindUserFromPrimary(ctx context.Context, id int64) (*User, error) {
    return m.FindUser(sqlx.WithReadPrimary(ctx), id)
}

// FindUserFromReplica — 强制从从库查询
func (m *UserModel) FindUserFromReplica(ctx context.Context, id int64) (*User, error) {
    return m.FindUser(sqlx.WithReadReplica(ctx), id)
}

// CreateUser — 写操作自动路由到主库
func (m *UserModel) CreateUser(ctx context.Context, user *User) error {
    result, err := m.conn.ExecCtx(sqlx.WithWrite(ctx),
        "INSERT INTO users (name, email, create_at, update_at) VALUES (?, ?, UNIX_TIMESTAMP(), UNIX_TIMESTAMP())",
        user.Name, user.Email)
    if err != nil {
        return err
    }
    user.ID, _ = result.LastInsertId()
    return nil
}

// ListUsers — 使用从库查询列表（可接受最终一致性）
func (m *UserModel) ListUsers(ctx context.Context, limit, offset int) ([]*User, error) {
    var users []*User
    err := m.conn.QueryRowsCtx(sqlx.WithReadReplica(ctx), &users,
        "SELECT * FROM users LIMIT ? OFFSET ?", limit, offset)
    return users, err
}
```

## 服务层最佳实践

### 场景1：写入后立即读取（强一致性）

用户注册后立即返回用户信息，必须从主库读取，避免主从延迟导致读不到刚写入的数据：

```go
func (s *UserService) RegisterUser(ctx context.Context, name, email string) (*User, error) {
    user := &User{Name: name, Email: email}

    if err := s.userModel.CreateUser(ctx, user); err != nil {
        return nil, err
    }

    // 立即读取，必须使用主库
    return s.userModel.FindUserFromPrimary(ctx, user.ID)
}
```

### 场景2：列表查询（可接受最终一致性）

```go
func (s *UserService) GetUserList(ctx context.Context, page, pageSize int) ([]*User, error) {
    offset := (page - 1) * pageSize
    return s.userModel.ListUsers(sqlx.WithReadReplica(ctx), pageSize, offset)
}
```

### 场景3：事务处理（读写操作都在主库）

```go
func (s *UserService) TransferUserData(ctx context.Context, fromID, toID int64) error {
    ctx = sqlx.WithWrite(ctx) // 事务中所有操作都使用主库

    return s.userModel.conn.TransactCtx(ctx, func(ctx context.Context, session sqlx.Session) error {
        var from, to User
        if err := session.QueryRowCtx(ctx, &from, "SELECT * FROM users WHERE id = ?", fromID); err != nil {
            return err
        }
        if err := session.QueryRowCtx(ctx, &to, "SELECT * FROM users WHERE id = ?", toID); err != nil {
            return err
        }
        _, err := session.ExecCtx(ctx,
            "UPDATE users SET update_at = UNIX_TIMESTAMP() WHERE id IN (?, ?)", fromID, toID)
        return err
    })
}
```

### 场景4：从库故障转移

```go
func (m *UserModel) FindUserWithFallback(ctx context.Context, id int64) (*User, error) {
    user, err := m.FindUser(sqlx.WithReadReplica(ctx), id)
    if err == nil {
        return user, nil
    }
    // 从库失败，回退到主库
    log.Printf("从库查询失败，回退到主库: %v", err)
    return m.FindUser(sqlx.WithReadPrimary(ctx), id)
}
```

## Context 函数参考

| 函数 | 效果 |
|------|------|
| `sqlx.WithReadPrimary(ctx)` | 强制从主库读取（强一致性） |
| `sqlx.WithReadReplica(ctx)` | 强制从从库读取 |
| `sqlx.WithWrite(ctx)` | 强制写操作路由（适合事务内使用） |

## 最佳实践建议

1. **监控主从延迟** — 确保主从延迟在业务可接受范围内（通常几毫秒，写压力大时可能增加）
2. **写入后立即读取使用主库** — 需要反映最新写入的读操作，要显式指定主库
3. **事务中使用 `WithWrite`** — 确保事务内的所有读操作都使用主库
4. **根据读写比例配置从库数量** — 10:1 的读写比例可以考虑配置 2-3 个从库
5. **选择合适的负载均衡策略** — `round-robin`（默认）均匀分配；`random` 更简单但小数量从库可能不均衡

## 相关文档

- [MySQL](./mysql.md)
- [MongoDB](./mongodb.md)
- [Redis](./redis.md)
