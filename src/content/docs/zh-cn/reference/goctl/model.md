---
title: goctl model
description: 使用 goctl model 从 DDL、数据源或 MongoDB 生成数据库访问层代码。
sidebar:
  order: 5

---

# goctl model

`goctl model` 从 MySQL DDL、在线数据源或 MongoDB 集合生成完整的 Go 数据访问层代码，内置两级缓存（内存 LRU + Redis）。

## MySQL DDL → 代码

```bash
goctl model mysql ddl \
  --src ./deploy/sql/user.sql \
  --dir ./internal/model \
  --cache
```

| 参数 | 说明 |
|---|---|
| `--src` | SQL DDL 文件路径 |
| `--dir` | 输出目录 |
| `--cache` | 启用 Redis 缓存层（推荐） |
| `--style` | 文件命名风格，默认 `goZero` |
| `--home` | 自定义模板目录 |
| `--idea` | 以机器可读格式输出错误（IDE 集成用） |

生成的文件结构：

```
internal/model/
├── usermodel.go         ← CRUD 方法
├── usermodel_gen.go     ← 自动生成代码（请勿手动修改）
└── vars.go              ← 错误变量（ErrNotFound 等）
```

## MySQL 数据源（在线生成）

直接连接到现有数据库进行代码生成：

```bash
goctl model mysql datasource \
  --url "root:password@tcp(localhost:3306)/mydb" \
  --table "user,order" \
  --dir ./internal/model \
  --cache
```

| 参数 | 说明 |
|---|---|
| `--url` | DSN 连接字符串 |
| `--table` | 表名，逗号分隔；支持通配符 `*` |
| `--dir` | 输出目录 |
| `--cache` | 启用缓存层 |
| `--strict` | 将 null 列映射为 Go 指针类型 |

## PostgreSQL 数据源

```bash
goctl model pg datasource \
  --url "postgres://user:pass@localhost:5432/mydb?sslmode=disable" \
  --table "public.users" \
  --dir ./internal/model \
  --cache
```

| 参数 | 说明 |
|---|---|
| `--url` | PostgreSQL DSN |
| `--table` | `schema.table` 格式 |
| `--schema` | Schema 名称，默认 `public` |
| `--dir` | 输出目录 |
| `--cache` | 启用缓存层 |

## MongoDB

```bash
goctl model mongo \
  --type User \
  --dir ./internal/model \
  --easy
```

| 参数 | 说明 |
|---|---|
| `--type` | Go 类型名称 |
| `--dir` | 输出目录 |
| `--easy` | 生成 `FindOne`/`Insert`/`Update`/`Delete` 简化方法 |
| `--home` | 自定义模板目录 |

## 缓存层说明

使用 `--cache` 生成的 model 包含两级缓存：

1. **内存 LRU**：进程级热数据缓存，减少 Redis 访问
2. **Redis**：跨实例分布式缓存，WriteThrough 策略

缓存管理遵循以下规则：
- 每次写操作（Create/Update/Delete）自动失效对应缓存 key
- 缓存 key 格式：`cache:<db>:<table>:<主键>:<值>`
- TTL 默认 7 天，可通过 `CacheConf` 覆盖

使用缓存时，config 需要添加 `CacheConf`：

```go
type Config struct {
    rest.RestConf
    DB struct {
        DataSource string
    }
    CacheRedis cache.CacheConf
}
```

## 自定义模板

导出默认模板并按需修改：

```bash
# 导出 model 模板到 ~/.goctl/
goctl template init --category model

# 修改模板后重新生成代码
goctl model mysql ddl \
  --src user.sql \
  --dir ./internal/model \
  --home ~/.goctl
```

## 延伸阅读

- [goctl 命令参考](./commands) — 全部子命令与参数
- [MySQL 教程](../../tutorials/database/mysql) — 在 go-zero 服务中使用生成的 model
