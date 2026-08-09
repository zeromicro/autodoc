---
title: 更新日志
description: go-zero 版本历史、破坏性变更与迁移说明。
sidebar:
  order: 6

---

## v1.10.3 – 2026-08-01

- 修复 `stringx.FirstN`/`Substr` 边界情况、`mapping` 指针切片反序列化问题以及高并发下 Redis 熔断器误触发问题。
- 优化 `collection.Queue` 扩容策略，新增 Redis `XGroupSetID`/`XGroupSetIDCtx`。

## v1.10.2 – 2026-05-31

- 为 MCP 工具处理程序增加 HTTP 请求元数据提取能力。
- 修复 Go 1.26 的 etcd 服务发现目标 URL 以及重复 watch 事件导致的内存增长问题。

## v1.10.1 – 2026-03-28

- 新增 JSON5 配置支持和 Redis 通用命令 `Do`/`DoCtx`。
- 项目升级至 Go 1.24，并包含重要的 `core/codec` 安全修复。

每个 go-zero 版本的详细发布说明请查看[版本记录](../releases/)。

完整历史请查看 [GitHub Releases 页面](https://github.com/zeromicro/go-zero/releases)。

## 最新版本

| 版本 | 日期 | 亮点 |
|------|------|------|
| [v1.10.3](../releases/v1.10.3) | 2026-08-01 | stringx/mapping 修复、Redis 熔断器修复、Queue 扩容优化 |
| [v1.10.2](../releases/v1.10.2) | 2026-05-31 | MCP 请求元数据、Go 1.26 etcd 服务发现修复 |
| [v1.10.1](../releases/v1.10.1) | 2026-03-28 | JSON5 配置、Redis `Do`/`DoCtx`、Go 1.24、安全修复 |
| [v1.10.0](../releases/v1.10.0) | 2026-02-15 | MCP 支持、网关增强、SSE 改进 |
| [v1.9.4](../releases/v1.9.4) | 2025-12-24 | K8s EndpointSlice、Redis GETEX、etcd 重试冷却 |
| [v1.9.3](../releases/v1.9.3) | 2025-11-16 | 一致性哈希负载均衡、网关 trace header 修复 |
| [v1.9.2](../releases/v1.9.2) | 2025-10-11 | go-redis 版本回收修复 |
| [v1.9.1](../releases/v1.9.1) | 2025-10-02 | 自定义日志 key、SSE 稳定性、mapreduce panic 堆栈 |
| [v1.9.0](../releases/v1.9.0) | 2025-08-17 | 日志脱敏、SSE 支持、MCP 服务器 |
| [v1.8.5](../releases/v1.8.5) | 2025-07-12 | Bug 修复和稳定性改进 |
| [v1.8.0](../releases/v1.8.0) | 2025-01-28 | 1.8 大版本发布 |
| [v1.7.0](../releases/v1.7.0) | 2024-07-27 | 要求 Go 1.21+，OpenTelemetry SDK v1.24 |
| [v1.6.0](../releases/v1.6.0) | 2023-10-28 | Endpoints 配置、Prometheus 重命名、breaker 重构 |
| [v1.5.0](../releases/v1.5.0) | 2023-03-04 | OpenTelemetry 替代 OpenTracing/Jaeger |

查看[全部 48 个版本 →](../releases/)
