---
title: MySQL
description: go-zero의 MySQL에 대해 설명합니다.
sidebar:
  order: 1
---


## 1. Define 스키마

```sql title="user.sql"
CREATE TABLE `user` (
  `id`         bigint NOT NULL AUTO_INCREMENT,
  `username`   varchar(255) NOT NULL DEFAULT '',
  `password`   varchar(255) NOT NULL DEFAULT '',
  `mobile`     varchar(20)  NOT NULL DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_username` (`username`),
  UNIQUE KEY `idx_mobile`   (`mobile`)
) ENGINE=InnoDB;
```

## 2. 생성 모델

```bash
# Without 예시입니다
goctl model mysql ddl -src user.sql -dir ./internal/model

# With, Redis 예시입니다
goctl model mysql ddl -src user.sql -dir ./internal/model -cache
```

This 생성합니다:

```
internal/model/
├── usermodel.go        # 예시입니다
├── usermodel_gen.go    # CRUD 예시입니다
└── vars.go             # ErrNotFound 예시입니다
```

## 3. 설정

```yaml title="etc/app.yaml"
DataSource: "root:password@tcp(127.0.0.1:3306)/dbname?parseTime=true&loc=UTC"
CacheRedis:
  - Host: 127.0.0.1:6379
    Type: node
    Pass: ""
```

:::tip[연결 pool]

```go
conn := sqlx.NewMysql(c.DataSource)
conn.DB().SetMaxOpenConns(100)
conn.DB().SetMaxIdleConns(10)
conn.DB().SetConnMaxLifetime(time.Hour)
```
:::

## 4. 서비스 컨텍스트 Wiring

```go title="internal/svc/servicecontext.go"
func NewServiceContext(c config.Config) *ServiceContext {
    conn := sqlx.NewMysql(c.DataSource)
    return &ServiceContext{
        Config:    c,
        UserModel: model.NewUserModel(conn, c.CacheRedis),
    }
}
```

## 5. CRUD 예제

### Insert

```go
result, err := l.svcCtx.UserModel.Insert(l.ctx, &model.User{
    Username: req.Username,
    Password: hashPassword(req.Password),
    Mobile:   req.Mobile,
})
if err != nil {
    return nil, err
}
userId, _ := result.LastInsertId()
```

### FindOne

```go
// 기본 키로 조회합니다(-cache로 생성한 경우 캐시 사용)
user, err := l.svcCtx.UserModel.FindOne(l.ctx, userId)
if errors.Is(err, model.ErrNotFound) {
    return nil, errorx.NewCodeError(404, "user not found")
}
```

### FindOne 통해 Unique Index

```go
// goctl은 모든 UNIQUE KEY에 대해 FindOneBy<FieldName>을 생성합니다
user, err := l.svcCtx.UserModel.FindOneByUsername(l.ctx, req.Username)
```

### 업데이트

```go
err = l.svcCtx.UserModel.Update(l.ctx, &model.User{
    Id:       userId,
    Username: req.Username,
    Password: newHash,
    Mobile:   user.Mobile,
})
```

### Delete

```go
err = l.svcCtx.UserModel.Delete(l.ctx, userId)
```

## 6. Transactions

Wrap multiple operations 에서 single DB transaction 사용하여 `TransactCtx`:

```go
err = l.svcCtx.UserModel.TransactCtx(l.ctx, func(ctx context.Context, session sqlx.Session) error {
    // Insert 예시입니다
    result, err := insertUser(ctx, session, user)
    if err != nil {
        return err   // auto-rollback
    }
    userId, _ := result.LastInsertId()

    // 연관된 프로필을 삽입합니다
    if err := insertProfile(ctx, session, userId, profile); err != nil {
        return err   // auto-rollback
    }

    return nil       // commit
})
```

## 7. Custom Queries

추가 custom 메서드 로 `usermodel.go` (아님 `usermodel_gen.go`, which is overwritten 통해 goctl):

```go title="internal/model/usermodel.go"
type UserModel interface {
    userModelInterface                    // 예시입니다
    FindByMobileAndStatus(ctx context.Context, mobile string, status int64) (*User, error)
    CountActiveUsers(ctx context.Context) (int64, error)
}

func (m *defaultUserModel) FindByMobileAndStatus(ctx context.Context, mobile string, status int64) (*User, error) {
    var user User
    query := fmt.Sprintf("SELECT %s FROM %s WHERE `mobile` = ? AND `status` = ? LIMIT 1",
        userRows, m.table)
    err := m.conn.QueryRowCtx(ctx, &user, query, mobile, status)
    switch {
    case err == nil:
        return &user, nil
    case errors.Is(err, sqlx.ErrNotFound):
        return nil, ErrNotFound
    default:
        return nil, err
    }
}

func (m *defaultUserModel) CountActiveUsers(ctx context.Context) (int64, error) {
    var count int64
    query := fmt.Sprintf("SELECT COUNT(*) FROM %s WHERE `status` = 1", m.table)
    err := m.conn.QueryRowCtx(ctx, &count, query)
    return count, err
}
```

## 8. Bulk Insert


```go
inserter, err := sqlx.NewBulkInserter(conn,
    fmt.Sprintf("INSERT INTO %s (%s) VALUES (?, ?, ?)", tableName, userRowsExpectAutoSet))
if err != nil {
    return err
}
defer inserter.Flush()

for _, user := range users {
    if err := inserter.Insert(user.Username, user.Password, user.Mobile); err != nil {
        return err
    }
}
```
