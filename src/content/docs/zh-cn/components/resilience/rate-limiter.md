---
title: 限流器
description: 自适应限流器的使用与配置。
sidebar:
  order: 2
---

# 限流器

## 基础用法

```go
import "github.com/zeromicro/go-zero/core/limit"

limiter := limit.NewTokenLimiter(100, 100, store, "api:login")
if limiter.Allow() {
  // handle request
}
```

## 最佳实践

- 按接口粒度设置 key
- 结合业务峰值设计 burst
