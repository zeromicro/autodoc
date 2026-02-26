---
title: 服务韧性组件
description: go-zero 容错组件：熔断器、限流器、超时控制、负载削减。
sidebar:
  order: 9

---

## 内容

- [熔断器](circuit-breaker/) — 阻止级联故障
- [滑动窗口限流](rate-limiter/) — 滑动窗口限流器
- [周期限流](period-limiter/) — 基于 Redis 的周期限流器
- [令牌桶限流](token-limiter/) — 令牌桶限流器
- [超时](timeout/) — 强制操作超时
- [负载削减](load-shedding/) — 拒绝超额负载
