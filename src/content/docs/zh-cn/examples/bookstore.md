---
title: 书店示例
description: 完整示例：API 网关调用 RPC 服务，后端使用 MySQL 存储。
sidebar:
  order: 4
---

# 书店示例

go-zero 官方示例：HTTP API 网关委托给后端 gRPC 服务，使用 MySQL 持久化数据。

## 架构

```text
客户端 → bookstore-api (HTTP) → bookstore-rpc (gRPC) → MySQL
```

## 获取代码

```bash
git clone https://github.com/zeromicro/go-zero.git
cd go-zero/example/bookstore
```

## 服务说明

| 服务 | 端口 | 说明 |
|------|------|------|
| `api/` | 8888 | HTTP 网关 |
| `rpc/` | 8080 | gRPC 书籍服务 |

## 启动 RPC

```bash
cd rpc
go run bookstore.go -f etc/bookstore.yaml
```

## 启动 API

```bash
cd api
go run bookstore.go -f etc/bookstore-api.yaml
```

## 测试

```bash
# 添加书籍
curl -X POST http://localhost:8888/add \
  -H "Content-Type: application/json" \
  -d '{"book":"The Go Programming Language","price":42}'

# 查询库存
curl "http://localhost:8888/check?book=The+Go+Programming+Language"
```

## 核心知识点

- API 网关路由到 RPC 后端
- goctl 从 MySQL DDL 生成 model
- ServiceContext 注入 RPC 客户端
