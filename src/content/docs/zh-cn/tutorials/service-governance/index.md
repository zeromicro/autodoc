---
title: Service Governance
description: "Implement resilience patterns in go-zero: circuit breaking, rate limiting, and load balancing."
sidebar:
  order: 11

---

## 概览

go-zero 提供内置的服务治理功能，帮助服务在高负载和故障期间保持稳定。

## 内容

- [熔断器](breaker.md) — 阻止级联故障
- [限流器](limiter.md) — 保护服务免受过载
- [负载均衡](loadbalance.md) — 分发 RPC 流量
