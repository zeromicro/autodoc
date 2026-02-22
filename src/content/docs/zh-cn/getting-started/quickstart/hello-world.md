---
title: Hello World
description: 通过最小示例快速运行一个 go-zero API 服务。
sidebar:
  order: 8
---

# Hello World

## 前置条件

- [x] Go 已安装
- [x] goctl 已安装

## 第一步：创建项目

```bash
goctl api new greet
cd greet
go mod tidy
```

## 第二步：运行服务

```bash
go run greet.go
```

## 第三步：验证

```bash
curl http://localhost:8888/from/you
```

预期输出：

```json
{"message":"Hello you"}
```
