---
title: 代码规范
description: go-zero 贡献者的编码约定与风格指南。
sidebar:
  order: 2

---

go-zero 遵循标准 Go 约定，同时有一些额外的规范。

## 格式化

所有代码必须通过 `gofmt` / `goimports` 格式化：

```bash
goimports -w ./...
```

CI 会拒绝存在格式问题的 PR。

## 命名规范

| 元素 | 约定 | 示例 |
|------|------|------|
| 包名 | 简短、小写、无下划线 | `logx`、`httpx` |
| 接口 | 描述性名词或 `-er` 后缀 | `UserModel`、`Breaker` |
| 构造函数 | `NewXxx` 或 `MustNewXxx` | `NewCache`、`MustNewServer` |
| 错误变量 | `ErrXxx` | `ErrNotFound`、`ErrTimeout` |
| 配置结构体 | 嵌入标准基础结构体 | `RestConf`、`RpcServerConf` |

## 错误处理

- 永远不要静默忽略错误。
- 使用上下文包装错误：`fmt.Errorf("createUser: %w", err)`。
- 在包级别定义哨兵错误用于类型断言。

## 测试

- 单元测试与源文件放在同一包中：`foo_test.go`。
- 优先使用表驱动测试。
- Mock 通过 `mockgen` 生成或手写最小桩。
- 新包最低覆盖率目标：**80%**。

```bash
go test -race -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## 注释

- 所有导出符号必须有文档注释。
- 注释使用完整的句子，以符号名称开头。
- 非显而易见的逻辑应添加行内注释解释*原因*。
