---
title: 配置参考
description: go-zero 服务的完整配置参考 — 加载方式、校验、服务配置及所有配置字段。
sidebar:
  order: 2

---

go-zero 服务的完整配置参考，涵盖配置加载机制、YAML 字段参考和各组件配置。

## 内容

- [配置概览](overview/) — `conf.MustLoad` 的工作原理、支持格式、环境变量、tag 规则和配置继承
- [API 服务配置](api-config/) — HTTP 服务配置（`rest.RestConf`）
- [RPC 服务配置](rpc-config/) — gRPC 服务配置（`zrpc.RpcServerConf` / `zrpc.RpcClientConf`）
- [服务配置](service-config/) — 所有服务类型共享的基础服务配置（`service.ServiceConf`）
- [日志配置](log/) — 结构化日志配置（`logx.LogConf`）
- [配置自动校验](auto-validation/) — 通过 `Validator` 接口在启动时自动校验配置
