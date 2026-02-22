---
title: Model Generation
description: Reference for goctl model — generate type-safe database access code.
sidebar:
  order: 4
---

# Model Generation

`goctl model` generates type-safe CRUD code for MySQL (and PostgreSQL). No ORM, no reflection — just plain Go functions backed by `sqlx`.

## From DDL File

```bash
goctl model mysql ddl \
  -src schema.sql \
  -dir ./internal/model \
  -cache          # wrap with Redis cache layer
```

## From Live Database

```bash
goctl model mysql datasource \
  -url "root:pass@tcp(127.0.0.1:3306)/mydb" \
  -table "user,order,product" \
  -dir ./internal/model \
  -cache
```

## Generated API

For a `user` table the generated interface is:

```go
type UserModel interface {
    Insert(ctx context.Context, data *User) (sql.Result, error)
    FindOne(ctx context.Context, id int64) (*User, error)
    FindOneByUsername(ctx context.Context, username string) (*User, error)
    Update(ctx context.Context, data *User) error
    Delete(ctx context.Context, id int64) error
    // Transaction support
    Trans(ctx context.Context, fn func(context.Context, sqlx.Session) error) error
}
```

## Customisation

goctl respects the `model` template directory. Override:

```bash
goctl template init --home ~/.goctl
# Edit ~/.goctl/model/insert.tpl
goctl model mysql ddl -src schema.sql -dir ./model --home ~/.goctl
```
