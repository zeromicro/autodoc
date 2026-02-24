---
title: MySQL Tutorials
description: Connect and interact with MySQL in go-zero services.
sidebar:
  order: 12

---

## 概览

go-zero 提供 `sqlx` 用于 MySQL 访问，并通过 `sqlc` 和 Redis 支持自动缓存。

## 内容

- [连接](connection.md) — 连接 MySQL
- [CRUD](curd.md) — 查询和修改数据
- [缓存](cache.md) — 为查询添加 Redis 缓存
- [批量插入](bulk-insert.md) — 高效批量插入
- [本地事务](local-transaction.md) — ACID 事务
- [分布式事务](distribute-transaction.md) — 跨服务事务
