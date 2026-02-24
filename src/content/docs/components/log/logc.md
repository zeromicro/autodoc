---
title: logc
description: Context-aware structured logging with go-zero logc.
sidebar:
  order: 3

---


The `logc` package encapsulates the logging functionalities of the `logx` package from `go-zero`, providing convenient methods to log messages at various levels.

## Type Definitions

```go
type (
	LogConf  = logx.LogConf
	LogField = logx.LogField
)
```

## Functions

### AddGlobalFields

Adds global fields that appear in all logs.

```go
func AddGlobalFields(fields ...LogField)
```

Example:

```go
logc.AddGlobalFields(logc.Field("app", "exampleApp"))
```

### Alert

Logs a message at alert level, and the message is written to the error log.

```go
func Alert(_ context.Context, v string)
```

Example:

```go
logc.Alert(context.Background(), "This is an alert message")
```

### Close

Closes the logging system.

```go
func Close() error
```

Example:

```go
if err := logc.Close(); err != nil {
    fmt.Println("Error closing log system:", err)
}
```

### Debug

Logs a message at debug level.

```go
func Debug(ctx context.Context, v ...interface{})
```

Example:

```go
logc.Debug(context.Background(), "This is a debug message")
```

### Debugf

Logs a formatted message at debug level.

```go
func Debugf(ctx context.Context, format string, v ...interface{})
```

Example:

```go
logc.Debugf(context.Background(), "This is a %s message", "formatted debug")
```

### Debugv

Logs a message at debug level with JSON content.

```go
func Debugv(ctx context.Context, v interface{})
```

Example:

```go
logc.Debugv(context.Background(), map[string]interface{}{"key": "value"})
```

### Debugw

Logs a message with fields at debug level.

```go
func Debugw(ctx context.Context, msg string, fields ...LogField)
```

Example:

```go
logc.Debugw(context.Background(), "Debug message with fields", logc.Field("key", "value"))
```

### Error

Logs a message at error level.

```go
func Error(ctx context.Context, v ...any)
```

Example:

```go
logc.Error(context.Background(), "This is an error message")
```

### Errorf

Logs a formatted message at error level.

```go
func Errorf(ctx context.Context, format string, v ...any)
```

Example:

```go
logc.Errorf(context.Background(), "This is a %s message", "formatted error")
```

### Errorv

Logs a message at error level with JSON content.

```go
func Errorv(ctx context.Context, v any)
```

Example:

```go
logc.Errorv(context.Background(), map[string]interface{}{"error": "something went wrong"})
```

### Errorw

Logs a message with fields at error level.

```go
func Errorw(ctx context.Context, msg string, fields ...LogField)
```

Example:

```go
logc.Errorw(context.Background(), "Error message with fields", logc.Field("key", "value"))
```

### Field

Returns a log field for the given key and value.

```go
func Field(key string, value any) LogField
```

Example:

```go
field := logc.Field("key", "value")
```

### Info

Logs a message at info level.

```go
func Info(ctx context.Context, v ...any)
```

Example:

```go
logc.Info(context.Background(), "This is an info message")
```

### Infof

Logs a formatted message at info level.

```go
func Infof(ctx context.Context, format string, v ...any)
```

Example:

```go
logc.Infof(context.Background(), "This is a %s message", "formatted info")
```

### Infov

Logs a message at info level with JSON content.

```go
func Infov(ctx context.Context, v any)
```

Example:

```go
logc.Infov(context.Background(), map[string]interface{}{"info": "some information"})
```

### Infow

Logs a message with fields at info level.

```go
func Infow(ctx context.Context, msg string, fields ...LogField)
```

Example:

```go
logc.Infow(context.Background(), "Info message with fields", logc.Field("key", "value"))
```

### Must

Checks if an error is nil; otherwise, logs the error and exits the program.

```go
func Must(err error)
```

Example:

```go
logc.Must(errors.New("fatal error"))
```

### MustSetup

Sets up logging with the given configuration. Exits on error.

```go
func MustSetup(c logx.LogConf)
```

Example:

```go
config := logx.LogConf{
    ServiceName: "exampleService",
    Mode:        "console",
}
logc.MustSetup(config)
```

### SetLevel

Sets the logging level to suppress some logs.

```go
func SetLevel(level uint32)
```

Example:

```go
logc.SetLevel(logx.LevelInfo)
```

### SetUp

Sets up the logging system with the given configuration. If already set up, it returns nil. Allows multiple setups by different service frameworks.

```go
func SetUp(c LogConf) error
```

Example:

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

Logs a message at slow log level.

```go
func Slow(ctx context.Context, v ...any)
```

Example:

```go
logc.Slow(context.Background(), "This is a slow log message")
```

### Slowf

Logs a formatted message at slow log level.

```go
func Slowf(ctx context.Context, format string, v ...any)
```

Example:

```go
logc.Slowf(context.Background(), "This is a %s message", "formatted slow log")
```

### Slowv

Logs a message at slow log level with JSON content.

```go
func Slowv(ctx context.Context, v any)
```

Example:

```go
logc.Slowv(context.Background(), map[string]interface{}{"slow": "operation details"})
```

### Sloww

Logs a message with fields at slow log level.

```go
func Sloww(ctx context.Context, msg string, fields ...LogField)
```

Example:

```go
logc.Sloww(context.Background(), "Slow log message with fields", logc.Field("key", "value"))
```
