---
title: MySQL
description: Connect to MySQL and generate type-safe models with goctl in go-zero.
sidebar:
  order: 1
---

# MySQL

go-zero uses goctl to generate type-safe, zero-reflection data access code from a DDL schema.

## Define Schema

```sql
CREATE TABLE `user` (
  `id`         bigint NOT NULL AUTO_INCREMENT,
  `username`   varchar(255) NOT NULL DEFAULT '',
  `password`   varchar(255) NOT NULL DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_username` (`username`)
) ENGINE=InnoDB;
```

## Generate Model

```bash
goctl model mysql ddl -src user.sql -dir ./internal/model
```

## Configuration

```yaml
DataSource: "root:password@tcp(127.0.0.1:3306)/dbname?parseTime=true"
```

## Usage

```go title="internal/svc/servicecontext.go"
func NewServiceContext(c config.Config) *ServiceContext {
    sqlConn := sqlx.NewMysql(c.DataSource)
    return &ServiceContext{
        Config:    c,
        UserModel: model.NewUserModel(sqlConn),
    }
}
```

```go
result, err := l.svcCtx.UserModel.Insert(l.ctx, &model.User{
    Username: req.Username,
    Password: hashPassword(req.Password),
})
```

## Transactions

```go
err = l.svcCtx.UserModel.TransactCtx(l.ctx, func(ctx context.Context, session sqlx.Session) error {
    if _, err := insertUser(ctx, session, user); err != nil {
        return err
    }
    return insertProfile(ctx, session, profile)
})
```
