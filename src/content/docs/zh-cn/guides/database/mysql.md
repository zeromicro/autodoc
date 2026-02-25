---
title: MySQL
description: 在 go-zero 中连接并操作 MySQL。
sidebar:
  order: 9
---


go-zero 使用 `goctl` 从 DDL 生成类型安全、零反射的数据访问代码。生成的 model 透明处理连接池、缓存、指标和链路追踪。

## 1. 定义表结构

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

## 2. 生成 Model

```bash
# 不带缓存
goctl model mysql ddl -src user.sql -dir ./internal/model

# 带 Redis 缓存（生产环境推荐）
goctl model mysql ddl -src user.sql -dir ./internal/model -cache
```

生成文件结构：

```
internal/model/
├── usermodel.go        # 接口 + 实现
├── usermodel_gen.go    # CRUD 方法（由 goctl 重新生成）
└── vars.go             # ErrNotFound 哨兵错误
```

## 3. 配置

```yaml title="etc/app.yaml"
DataSource: "root:password@tcp(127.0.0.1:3306)/dbname?parseTime=true&loc=UTC"
CacheRedis:
  - Host: 127.0.0.1:6379
    Type: node
    Pass: ""
```

## 4. ServiceContext 注入

```go title="internal/svc/servicecontext.go"
func NewServiceContext(c config.Config) *ServiceContext {
    conn := sqlx.NewMysql(c.DataSource)
    return &ServiceContext{
        Config:    c,
        UserModel: model.NewUserModel(conn, c.CacheRedis),
    }
}
```

## 5. CRUD 示例

### 插入

```go
result, err := l.svcCtx.UserModel.Insert(l.ctx, &model.User{
    Username: req.Username,
    Password: hashPassword(req.Password),
    Mobile:   req.Mobile,
})
userId, _ := result.LastInsertId()
```

### 按主键查询（使用缓存）

```go
user, err := l.svcCtx.UserModel.FindOne(l.ctx, userId)
if errors.Is(err, model.ErrNotFound) {
    return nil, errorx.NewCodeError(404, "用户不存在")
}
```

### 按唯一索引查询

```go
// goctl 为每个 UNIQUE KEY 生成 FindOneBy<字段名> 方法
user, err := l.svcCtx.UserModel.FindOneByUsername(l.ctx, req.Username)
```

### 更新

```go
err = l.svcCtx.UserModel.Update(l.ctx, &model.User{
    Id:       userId,
    Username: req.Username,
    Password: newHash,
    Mobile:   user.Mobile,
})
```

### 删除

```go
err = l.svcCtx.UserModel.Delete(l.ctx, userId)
```

## 6. 事务

```go
err = l.svcCtx.UserModel.TransactCtx(l.ctx, func(ctx context.Context, session sqlx.Session) error {
    result, err := insertUser(ctx, session, user)
    if err != nil {
        return err  // 自动回滚
    }
    userId, _ := result.LastInsertId()
    if err := insertProfile(ctx, session, userId, profile); err != nil {
        return err  // 自动回滚
    }
    return nil  // 提交
})
```

## 7. 自定义查询

向 `usermodel.go`（非 `usermodel_gen.go`）添加自定义方法：

```go title="internal/model/usermodel.go"
func (m *defaultUserModel) CountActiveUsers(ctx context.Context) (int64, error) {
    var count int64
    query := fmt.Sprintf("SELECT COUNT(*) FROM %s WHERE `status` = 1", m.table)
    err := m.conn.QueryRowCtx(ctx, &count, query)
    return count, err
}
```

## 8. 批量插入

```go
inserter, _ := sqlx.NewBulkInserter(conn,
    fmt.Sprintf("INSERT INTO %s (%s) VALUES (?, ?, ?)",
        tableName, userRowsExpectAutoSet))
defer inserter.Flush()

for _, user := range users {
    inserter.Insert(user.Username, user.Password, user.Mobile)
}
```
