---
title: 配置自动校验
description: 在 go-zero 启动时自动校验配置。
sidebar:
  order: 6

---


## 自动配置验证

go-zero 支持通过简单的接口实现来进行自动配置验证。当您需要确保配置值在应用程序启动前满足特定条件时，这个功能特别有用。

## 工作原理

这项新功能引入了一个在加载后自动检查配置的验证机制。以下是使用方法：

1. 在您的配置结构体中实现 `Validator` 接口：

```go
type YourConfig struct {
    Name     string
    MaxUsers int
}

// 实现 Validator 接口
func (c YourConfig) Validate() error {
    if len(c.Name) == 0 {
        return errors.New("name 不能为空")
    }
    if c.MaxUsers <= 0 {
        return errors.New("max users 必须为正数")
    }
    return nil
}
```

2. 像往常一样使用配置 - 验证会自动进行：

```go
var config YourConfig
err := conf.Load("config.yaml", &config)
if err != nil {
    // 这里会捕获加载错误和验证错误
    log.Fatal(err)
}
```

## 主要优势

1. **早期错误检测**：在应用程序启动时立即发现配置错误
2. **自定义验证规则**：根据应用程序需求定义专属的验证逻辑
3. **简洁集成**：无需额外的函数调用 - 验证在加载后自动进行
4. **类型安全**：验证与配置结构体紧密绑定

## 使用示例

这里是一个实际的使用示例：

```go
type DatabaseConfig struct {
    Host     string
    Port     int
    MaxConns int
}

func (c DatabaseConfig) Validate() error {
    if len(c.Host) == 0 {
        return errors.New("数据库主机地址不能为空")
    }
    if c.Port <= 0 || c.Port > 65535 {
        return errors.New("端口号无效")
    }
    if c.MaxConns <= 0 {
        return errors.New("最大连接数必须为正数")
    }
    return nil
}
```

## 实现细节

该功能通过在加载配置值后检查配置类型是否实现了 `Validator` 接口来工作。如果实现了该接口，验证就会自动执行。这种方法保持了向后兼容性，同时为新代码提供了增强的功能。

## 快速开始

要使用这个功能，只需更新到最新版本的 go-zero 即可。不需要额外的依赖。验证功能适用于所有现有的配置加载方式，包括 JSON、YAML 和 TOML 格式。

## 最佳实践

1. 保持验证规则简单，专注于配置有效性
2. 使用清晰的错误消息，准确指出问题所在
3. 考虑为所有关键配置值添加验证
4. 记住验证在启动时运行 - 避免耗时操作