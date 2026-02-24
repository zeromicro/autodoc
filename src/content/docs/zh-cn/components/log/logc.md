---
title: logc
description: 使用 go-zero logc 进行上下文感知的结构化日志记录。
sidebar:
  order: 3

---


`logc` 包封装了 `go-zero` 中 `logx` 包的日志功能，提供了一些便捷的方法来记录不同级别的日志。

## 类型定义

```go
type (
	LogConf  = logx.LogConf
	LogField = logx.LogField
)
```

## 函数列表

### AddGlobalFields

添加全局字段，这些字段会出现在所有的日志中。

```go
func AddGlobalFields(fields ...LogField)
```

示例：

```go
logc.AddGlobalFields(logc.Field("app", "exampleApp"))
```

### Alert

以警告级别记录日志信息，该信息会写入错误日志。

```go
func Alert(_ context.Context, v string)
```

示例：

```go
logc.Alert(context.Background(), "This is an alert message")
```

### Close

关闭日志记录系统。

```go
func Close() error
```

示例：

```go
if err := logc.Close(); err != nil {
    fmt.Println("Error closing log system:", err)
}
```

### Debug

记录调试级别的日志信息。

```go
func Debug(ctx context.Context, v ...interface{})
```

示例：

```go
logc.Debug(context.Background(), "This is a debug message")
```

### Debugf

格式化记录调试级别的日志信息。

```go
func Debugf(ctx context.Context, format string, v ...interface{})
```

示例：

```go
logc.Debugf(context.Background(), "This is a %s message", "formatted debug")
```

### Debugv

以 JSON 格式记录调试级别的日志信息。

```go
func Debugv(ctx context.Context, v interface{})
```

示例：

```go
logc.Debugv(context.Background(), map[string]interface{}{"key": "value"})
```

### Debugw

记录带字段的调试级别的日志信息。

```go
func Debugw(ctx context.Context, msg string, fields ...LogField)
```

示例：

```go
logc.Debugw(context.Background(), "Debug message with fields", logc.Field("key", "value"))
```

### Error

记录错误级别的日志信息。

```go
func Error(ctx context.Context, v ...any)
```

示例：

```go
logc.Error(context.Background(), "This is an error message")
```

### Errorf

格式化记录错误级别的日志信息。

```go
func Errorf(ctx context.Context, format string, v ...any)
```

示例：

```go
logc.Errorf(context.Background(), "This is a %s message", "formatted error")
```

### Errorv

以 JSON 格式记录错误级别的日志信息。

```go
func Errorv(ctx context.Context, v any)
```

示例：

```go
logc.Errorv(context.Background(), map[string]interface{}{"error": "something went wrong"})
```

### Errorw

记录带字段的错误级别的日志信息。

```go
func Errorw(ctx context.Context, msg string, fields ...LogField)
```

示例：

```go
logc.Errorw(context.Background(), "Error message with fields", logc.Field("key", "value"))
```

### Field

返回一个日志字段。

```go
func Field(key string, value any) LogField
```

示例：

```go
field := logc.Field("key", "value")
```

### Info

记录信息级别的日志信息。

```go
func Info(ctx context.Context, v ...any)
```

示例：

```go
logc.Info(context.Background(), "This is an info message")
```

### Infof

格式化记录信息级别的日志信息。

```go
func Infof(ctx context.Context, format string, v ...any)
```

示例：

```go
logc.Infof(context.Background(), "This is a %s message", "formatted info")
```

### Infov

以 JSON 格式记录信息级别的日志信息。

```go
func Infov(ctx context.Context, v any)
```

示例：

```go
logc.Infov(context.Background(), map[string]interface{}{"info": "some information"})
```

### Infow

记录带字段的信息级别的日志信息。

```go
func Infow(ctx context.Context, msg string, fields ...LogField)
```

示例：

```go
logc.Infow(context.Background(), "Info message with fields", logc.Field("key", "value"))
```

### Must

检查错误，如果发生错误则记录错误并退出程序。

```go
func Must(err error)
```

示例：

```go
logc.Must(errors.New("fatal error"))
```

### MustSetup

根据给定的配置初始化日志系统，如有错误则退出程序。

```go
func MustSetup(c logx.LogConf)
```

示例：

```go
config := logx.LogConf{
    ServiceName: "exampleService",
    Mode:        "console",
}
logc.MustSetup(config)
```

### SetLevel

设置日志级别，可以用来抑制某些日志。

```go
func SetLevel(level uint32)
```

示例：

```go
logc.SetLevel(logx.LevelInfo)
```

### SetUp

根据给定的配置初始化日志系统。如果已经初始化，将不再重复初始化。

```go
func SetUp(c LogConf) error
```

示例：

```go
config := logc.LogConf{
    ServiceName: "exampleService",
    Mode:        "console",
}
if err := logc.SetUp(config); err != nil {
    fmt.Println("Error setting up log system:", err)
}
```

### Slow

记录慢日志。

```go
func Slow(ctx context.Context, v ...any)
```

示例：

```go
logc.Slow(context.Background(), "This is a slow log message")
```

### Slowf

格式化记录慢日志。

```go
func Slowf(ctx context.Context, format string, v ...any)
```

示例：

```go
logc.Slowf(context.Background(), "This is a %s message", "formatted slow log")
```

### Slowv

以 JSON 格式记录慢日志。

```go
func Slowv(ctx context.Context, v any)
```

示例：

```go
logc.Slowv(context.Background(), map[string]interface{}{"slow": "operation details"})
```

### Sloww

记录带字段的慢日志。

```go
func Sloww(ctx context.Context, msg string, fields ...LogField)
```

示例：

```go
logc.Sloww(context.Background(), "Slow log message with fields", logc.Field("key", "value"))
```
