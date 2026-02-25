---
title: 缓存组件
description: go-zero 进程内和分布式缓存组件。
sidebar:
  order: 4

---

go-zero 提供进程内和分布式两种缓存，用于降低数据库负载并提升响应速度。缓存与 `goctl model` 生成的数据库查询自动集成。

## 内容

- [内存缓存](memory-cache.md) — 进程内 LRU 缓存，适用于热点数据
- [Redis 缓存](redis-cache.md) — 分布式 Redis 缓存，支持自动失效
