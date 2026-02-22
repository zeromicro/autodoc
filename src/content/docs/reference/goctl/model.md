---
title: Model Generation
description: Reference for goctl model — generate type-safe database access code for MySQL, PostgreSQL, and MongoDB.
sidebar:
  order: 4
---

# Model Generation

`goctl model` generates type-safe CRUD code with **no ORM, no reflection** — just plain Go functions backed by `sqlx` for relational databases and the official driver for MongoDB.

## MySQL

### From DDL File

```bash
goctl model mysql ddl [flags]
```

| Flag | Description |
|---|---|
| `-src` | Path to the `.sql` DDL file (required) |
| `-dir` | Output directory (required) |
| `-cache` | Wrap with Redis cache layer |
| `-style` | File naming style: `gozero` \| `go_zero` \| `goZero` |
| `-home` | Custom template directory |

```bash
goctl model mysql ddl \
  -src schema.sql \
  -dir ./internal/model \
  -cache
```

### From Live Database

```bash
goctl model mysql datasource [flags]
```

| Flag | Description |
|---|---|
| `-url` | MySQL DSN (required) |
| `-table` | Comma-separated table names or `"*"` for all |
| `-dir` | Output directory (required) |
| `-cache` | Wrap with Redis cache layer |
| `-style` | File naming style |

```bash
goctl model mysql datasource \
  -url "root:pass@tcp(127.0.0.1:3306)/mydb" \
  -table "user,order" \
  -dir ./internal/model \
  -cache
```

### Generated Interface (MySQL)

For a `user` table, the generated interface is:

```go
type UserModel interface {
    Insert(ctx context.Context, data *User) (sql.Result, error)
    FindOne(ctx context.Context, id int64) (*User, error)
    FindOneByUsername(ctx context.Context, username string) (*User, error)
    Update(ctx context.Context, data *User) error
    Delete(ctx context.Context, id int64) error
    Trans(ctx context.Context, fn func(context.Context, sqlx.Session) error) error
}
```

- Unique index columns (like `username` above) automatically generate a `FindOneBy<Column>` method.
- The `Trans` method wraps multiple operations in a database transaction.

---

## PostgreSQL

```bash
goctl model pg datasource [flags]
```

| Flag | Default | Description |
|---|---|---|
| `-url` | — | PostgreSQL DSN (required) |
| `-table` | — | Table name(s) |
| `-schema` | `public` | PostgreSQL schema |
| `-dir` | — | Output directory (required) |
| `-cache` | `false` | Add Redis cache layer |
| `-style` | `gozero` | File naming style |

```bash
goctl model pg datasource \
  -url "postgres://root:pass@localhost:5432/mydb?sslmode=disable" \
  -table "users,products" \
  -dir ./internal/model
```

The generated code is nearly identical to MySQL — same CRUD interface, same cache integration, different SQL placeholder syntax (`$1` vs `?`).

---

## MongoDB

```bash
goctl model mongo [flags]
```

| Flag | Default | Description |
|---|---|---|
| `-type` | — | Go type name for the document (required) |
| `-dir` | — | Output directory (required) |
| `-cache` | `false` | Add Redis cache layer |
| `-easy` | `false` | Generate a minimal no-frills interface |
| `-style` | `gozero` | File naming style |
| `-home` | `~/.goctl` | Custom template directory |

```bash
goctl model mongo -type Article -dir ./internal/model -cache
```

Generated files:

```
internal/model/
├── articlemodel.go         # interface + New() constructor
├── articlemodelgen.go      # generated CRUD implementation
└── vars.go                 # error variables
```

---

## Cache Layer

When `-cache` is passed, the generated model wraps every `FindOne` and `FindOneBy*` read in a two-level cache:

1. **Local memory cache** (LRU, 1000 entries, 60-second TTL)
2. **Redis** (configurable TTL)

Cache invalidation happens automatically on `Update` and `Delete`.

```go title="internal/svc/servicecontext.go"
import (
    "github.com/zeromicro/go-zero/core/stores/cache"
    "github.com/zeromicro/go-zero/core/stores/sqlx"
)

func NewServiceContext(c config.Config) *ServiceContext {
    sqlConn := sqlx.NewMysql(c.DataSource)
    cacheConf := cache.CacheConf{
        {Host: c.Redis.Host, Pass: c.Redis.Pass, Type: "node"},
    }
    return &ServiceContext{
        Config:    c,
        UserModel: model.NewUserModel(sqlConn, cacheConf),
    }
}
```

---

## Custom Templates

Override any generated file by editing the corresponding template:

```bash
goctl template init          # copies defaults to ~/.goctl/
ls ~/.goctl/model/           # insert.tpl, find-one.tpl, update.tpl, delete.tpl, ...

# Edit a template
vim ~/.goctl/model/insert.tpl

# Regenerate using your customised templates
goctl model mysql ddl \
  -src schema.sql \
  -dir ./internal/model \
  -home ~/.goctl
```
