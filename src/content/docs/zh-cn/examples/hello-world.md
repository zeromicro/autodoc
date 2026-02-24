---
title: Hello World
description: 最简单的 go-zero API 服务示例。
sidebar:
  order: 2

---

# Hello World

适合任何 go-zero 新手的入门示例。

## 前提条件

- Go 1.21+
- goctl 已安装

## 生成项目

```bash
goctl api new greet
cd greet
go mod tidy
```

## 项目结构

```text
greet/
├── etc/
│   └── greet-api.yaml
├── internal/
│   ├── config/
│   ├── handler/
│   ├── logic/
│   ├── svc/
│   └── types/
└── greet.go
```

## 启动

```bash
go run greet.go
```

## 测试

```bash
curl http://localhost:8888/from/you
# {"message":"Hello you"}
```

## 下一步

- 添加[中间件](../tutorials/http/middleware.md)实现日志记录
- 接入[数据库](../tutorials/database/mysql.md)
