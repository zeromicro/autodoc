---
title: 服务韧性组件
description: "Fault tolerance components for go-zero: circuit breaker, rate limiter, timeout, load shedding."
sidebar:
  order: 9

---

## 内容

- [熔断器](circuit-breaker.md) — 阻止级联故障
- [滑动窗口限流](rate-limiter.md) — 滑动窗口限流器
- [周期限流](period-limiter.md) — 基于 Redis 的周期限流器
- [令牌桶限流](token-limiter.md) — 令牌桶限流器
- [超时](timeout.md) — 强制操作超时
- [负载削减](load-shedding.md) — 拒绝超额负载
