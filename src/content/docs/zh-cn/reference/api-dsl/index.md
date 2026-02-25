---
title: API DSL 参考
description: go-zero .api DSL 参考 — 参数、类型、路由分组、中间件、JWT 等。
sidebar:
  order: 5

---

## 概览

`.api` DSL 是 go-zero 用于描述 HTTP API 的领域特定语言。本节涵盖了 DSL 的所有特性。

## 内容

- [路由规则](route-rule.md) — 定义 URL 模式、方法和处理器
- [路由分组](route-group.md) — 使用共享配置组织路由
- [路由前缀](route-prefix.md) — 为分组添加 URL 前缀
- [参数](parameter.md) — 请求和响应的字段类型与标签
- [类型定义](type.md) — 定义共享的请求/响应结构体
- [JWT 鉴权](jwt.md) — 使用 JWT 保护路由
- [中间件](middleware.md) — 为路由添加前/后处理
- [请求签名](signature.md) — HMAC 签名验证
- [Import](import.md) — 通过 import 拆分 `.api` 文件
- [SSE 路由](route-sse.md) — Server-Sent Events 端点
- [FAQ](faq.md) — 常见问题解答
