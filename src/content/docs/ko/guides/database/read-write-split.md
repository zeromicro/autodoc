---
title: 데이터베이스 Read-Write Splitting
description: go-zero의 데이터베이스 Read-Write Splitting에 대해 설명합니다.
sidebar:
  order: 4
---


## 사용 시점

**Ideal scenarios:**
- Primary 데이터베이스 under 높은 write 부하
- Need 로 scale reads horizontally 없이 sharding

**Routing rules:**
| Operation | 기본값 routing |
|-----------|----------------|
| `INSERT`, `UPDATE`, `DELETE` | Primary (master) |
| `SELECT` (general) | Replica |
| `SELECT` (strong consistency 필수) | Primary, via `sqlx.WithReadPrimary` |

## 설정

```yaml
# config.yaml
DB:
  DataSource: "user:password@tcp(master:3306)/database"
  DriverName: mysql          # 예시입니다
  Policy: "round-robin"      # 로드합니다
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

## Initializing 연결

```go
var c Config
conf.MustLoad("config.yaml", &c)

// 읽기/쓰기 분리를 지원하는 연결을 생성합니다
conn := sqlx.MustNewConn(c.DB)
```

## 모델 계층

```go
type UserModel struct {
    conn sqlx.SqlConn
}

// FindUser — 기본적으로 replica로 라우팅합니다
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

// FindUserFromPrimary — 강한 일관성을 위해 primary를 강제합니다
func (m *UserModel) FindUserFromPrimary(ctx context.Context, id int64) (*User, error) {
    return m.FindUser(sqlx.WithReadPrimary(ctx), id)
}

// FindUserFromReplica — replica를 강제합니다
func (m *UserModel) FindUserFromReplica(ctx context.Context, id int64) (*User, error) {
    return m.FindUser(sqlx.WithReadReplica(ctx), id)
}

// CreateUser — 쓰기는 항상 primary로 라우팅됩니다
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

// ListUsers — 페이지 목록에는 replica를 사용합니다(최종 일관성 허용)
func (m *UserModel) ListUsers(ctx context.Context, limit, offset int) ([]*User, error) {
    var users []*User
    err := m.conn.QueryRowsCtx(sqlx.WithReadReplica(ctx), &users,
        "SELECT * FROM users LIMIT ? OFFSET ?", limit, offset)
    return users, err
}
```

## Service 계층 Patterns

### 패턴 1: 쓰기 직후 읽기(강한 일관성)

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

```go
func (s *UserService) RegisterUser(ctx context.Context, name, email string) (*User, error) {
    user := &User{Name: name, Email: email}

    if err := s.userModel.CreateUser(ctx, user); err != nil {
        return nil, err
    }

    // primary 읽기 강제 — replica 지연으로 오래된 데이터가 반환될 수 있습니다
    return s.userModel.FindUserFromPrimary(ctx, user.ID)
}
```

### 패턴 2: 목록 조회(최종 일관성 허용)

```go
func (s *UserService) GetUserList(ctx context.Context, page, pageSize int) ([]*User, error) {
    offset := (page - 1) * pageSize
    return s.userModel.ListUsers(sqlx.WithReadReplica(ctx), pageSize, offset)
}
```

### Pattern 3: Transaction (모든 에서 Primary)

```go
func (s *UserService) TransferUserData(ctx context.Context, fromID, toID int64) error {
    ctx = sqlx.WithWrite(ctx) // 예시입니다

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
    // replica 실패 — primary로 폴백합니다
    return m.FindUser(sqlx.WithReadPrimary(ctx), id)
}
```

## 컨텍스트 참조

| 함수 | Effect |
|----------|--------|
| `sqlx.WithReadPrimary(ctx)` | Force read 에서 primary (strong consistency) |
| `sqlx.WithReadReplica(ctx)` | Force read 에서 replica |
| `sqlx.WithWrite(ctx)` | Force write routing (사용 inside transactions) |

## 모범 사례


## 관련 문서

- [MySQL](../mysql/)
- [MongoDB](../mongodb/)
- [Redis](../redis/)
