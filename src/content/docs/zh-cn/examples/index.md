---
title: 示例
description: 基于 go-zero 构建的真实项目示例，从简单 API 到完整微服务系统。
sidebar:
  order: 1
---


本节收录了可直接运行的实用示例，帮助你将 go-zero 的模式应用到真实问题中。

## 示例列表

| 示例 | 难度 | 说明 |
|------|------|------|
| [Hello World](./hello-world/) | 入门 | 最简 API 服务 |
| [REST API + JWT](./rest-api-jwt/) | 中级 | 带鉴权的 HTTP 接口 |
| [书店](./bookstore/) | 中级 | 完整 API + RPC 服务 |
| [微服务系统](./microservice-system/) | 高级 | 多服务 + 服务发现 |

## 运行准备

所有示例需要 Go 1.21+ 及 goctl。

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
```

克隆官方示例仓库：

```bash
git clone https://github.com/zeromicro/go-zero.git
cd go-zero/example
```
