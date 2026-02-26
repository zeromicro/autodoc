---
title: Database Read-Write Splitting
description: Scale database performance with master-replica routing in go-zero
sidebar:
  order: 4
---


In high-concurrency applications, the database is often the bottleneck. Read-write splitting routes write operations to a primary (master) and read operations to replicas, significantly improving throughput and resilience.

go-zero provides first-class support for read-write splitting with automatic routing, configurable load balancing, and explicit context-based overrides.

## When to Use

**Ideal scenarios:**
- High read/write ratio (e.g. e-commerce product browsing, content platforms, social feeds)
- Primary database under high write load
- Need to scale reads horizontally without sharding

**Routing rules:**
| Operation | Default routing |
|-----------|----------------|
| `INSERT`, `UPDATE`, `DELETE` | Primary (master) |
| `SELECT` (general) | Replica |
| `SELECT` (strong consistency required) | Primary, via `sqlx.WithReadPrimary` |

## Configuration

```yaml
# config.yaml
DB:
  DataSource: "user:password@tcp(master:3306)/database"
  DriverName: mysql          # optional, defaults to mysql
  Policy: "round-robin"      # load balancing: round-robin (default) or random
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

## Initializing the Connection

```go
var c Config
conf.MustLoad("config.yaml", &c)

// Create a connection that supports read-write splitting
conn := sqlx.MustNewConn(c.DB)
```

## Model Layer

```go
type UserModel struct {
    conn sqlx.SqlConn
}

// FindUser — routes to replica by default
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

// FindUserFromPrimary — force primary for strong consistency
func (m *UserModel) FindUserFromPrimary(ctx context.Context, id int64) (*User, error) {
    return m.FindUser(sqlx.WithReadPrimary(ctx), id)
}

// FindUserFromReplica — force replica
func (m *UserModel) FindUserFromReplica(ctx context.Context, id int64) (*User, error) {
    return m.FindUser(sqlx.WithReadReplica(ctx), id)
}

// CreateUser — writes always route to primary
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

// ListUsers — use replica for paginated lists (eventual consistency is fine)
func (m *UserModel) ListUsers(ctx context.Context, limit, offset int) ([]*User, error) {
    var users []*User
    err := m.conn.QueryRowsCtx(sqlx.WithReadReplica(ctx), &users,
        "SELECT * FROM users LIMIT ? OFFSET ?", limit, offset)
    return users, err
}
```

## Service Layer Patterns

### Pattern 1: Write Then Immediate Read (Strong Consistency)

After registering a user, return their full profile — must come from primary to avoid replication lag:

```go
func (s *UserService) RegisterUser(ctx context.Context, name, email string) (*User, error) {
    user := &User{Name: name, Email: email}

    if err := s.userModel.CreateUser(ctx, user); err != nil {
        return nil, err
    }

    // Force primary read — replica lag could return stale data
    return s.userModel.FindUserFromPrimary(ctx, user.ID)
}
```

### Pattern 2: List Query (Eventual Consistency OK)

```go
func (s *UserService) GetUserList(ctx context.Context, page, pageSize int) ([]*User, error) {
    offset := (page - 1) * pageSize
    return s.userModel.ListUsers(sqlx.WithReadReplica(ctx), pageSize, offset)
}
```

### Pattern 3: Transaction (All on Primary)

```go
func (s *UserService) TransferUserData(ctx context.Context, fromID, toID int64) error {
    ctx = sqlx.WithWrite(ctx) // ensure all ops in the transaction use primary

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

### Pattern 4: Replica Fallback

```go
func (m *UserModel) FindUserWithFallback(ctx context.Context, id int64) (*User, error) {
    user, err := m.FindUser(sqlx.WithReadReplica(ctx), id)
    if err == nil {
        return user, nil
    }
    // Replica failed — fall back to primary
    return m.FindUser(sqlx.WithReadPrimary(ctx), id)
}
```

## Context Reference

| Function | Effect |
|----------|--------|
| `sqlx.WithReadPrimary(ctx)` | Force read from primary (strong consistency) |
| `sqlx.WithReadReplica(ctx)` | Force read from replica |
| `sqlx.WithWrite(ctx)` | Force write routing (use inside transactions) |

## Best Practices

1. **Monitor replication lag** — ensure it is acceptable for your business. Typical lag is a few milliseconds, but can grow under heavy write load.
2. **Use `WithReadPrimary` after writes** — any read that must reflect a just-committed write should explicitly use the primary.
3. **Wrap transactions with `WithWrite`** — this ensures all reads inside a transaction use the primary.
4. **Tune replica count to your read/write ratio** — a 10:1 read/write ratio may warrant 2–3 replicas.
5. **Choose load balancing strategy** — `round-robin` (default) distributes load evenly; `random` is simpler but may be uneven for small replica counts.

## Related

- [MySQL](./mysql/)
- [MongoDB](./mongodb/)
- [Redis](./redis/)
