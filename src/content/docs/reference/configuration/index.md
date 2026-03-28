---
title: Configuration Reference
description: Complete configuration reference for go-zero services — loading, validation, service settings, and all config fields.
sidebar:
  order: 2

---

Complete configuration reference for go-zero services, covering how configuration loading works, YAML field references, and per-component settings.

## Contents

- [Configuration Overview](overview/) — How `conf.MustLoad` works, supported formats, environment variables, tag rules, and config inheritance
- [API Service Configuration](api-config/) — HTTP service configuration (`rest.RestConf`)
- [RPC Service Configuration](rpc-config/) — gRPC service configuration (`zrpc.RpcServerConf` / `zrpc.RpcClientConf`)
- [Service Configuration](service-config/) — Base service configuration shared by all service types (`service.ServiceConf`)
- [Log Configuration](log/) — Structured logging settings (`logx.LogConf`)
- [Config Auto-Validation](auto-validation/) — Validate configuration on startup via the `Validator` interface
