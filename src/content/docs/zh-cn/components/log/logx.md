---
title: logx
description: 使用 go-zero logx 进行结构化日志记录。
sidebar:
  order: 2

---


## 类型与方法说明

### 1. `LogConf`

`LogConf` 是日志配置结构体，用于设置日志相关的各项参数。

```go
type LogConf struct {
	ServiceName         string `json:",optional"`
	Mode                string `json:",default=console,options=[console,file,volume]"`
	Encoding            string `json:",default=json,options=[json,plain]"`
	TimeFormat          string `json:",optional"`
	Path                string `json:",default=logs"`
	Level               string `json:",default=info,options=[debug,info,error,severe]"`
	MaxContentLength    uint32 `json:",optional"`
	Compress            bool   `json:",optional"`
	Stat                bool   `json:",default=true"`
	KeepDays            int    `json:",optional"`
	StackCooldownMillis int    `json:",default=100"`
	MaxBackups          int    `json:",default=0"`
	MaxSize             int    `json:",default=0"`
	Rotation            string `json:",default=daily,options=[daily,size]"`
}
```

### 2. `WithColor`

在纯文本编码时，给字符串添加颜色。

```go
func WithColor(text string, colour color.Color) string
```

- **参数**:
    - `text`: 要添加颜色的文本。
    - `colour`: 颜色对象。

- **返回值**: 返回带颜色的字符串。

### 示例代码

```go
import "github.com/fatih/color"

text := "Hello, World!"
coloredText := logx.WithColor(text, color.FgRed)
fmt.Println(coloredText)
```

### 3. `AddGlobalFields`

添加全局字段，这些字段将被添加到所有日志条目中。

```go
func AddGlobalFields(fields ...LogField)
```

- **参数**:
    - `fields`: 要添加的全局字段。

### 示例代码

```go
logx.AddGlobalFields(logx.Field("service", "my-service"))
```

### 4. `ContextWithFields`

返回包含给定字段的上下文。

```go
func ContextWithFields(ctx context.Context, fields ...LogField) context.Context
```

- **参数**:
    - `ctx`: 上下文对象。
    - `fields`: 要添加到上下文中的字段。

- **返回值**: 返回新的上下文对象。

### 示例代码

```go
ctx := context.Background()
ctx = logx.ContextWithFields(ctx, logx.Field("request_id", "12345"))
```

### 5. `Logger` 接口

`Logger` 接口定义了日志记录的方法。

```go
type Logger interface {
	Debug(...any)
	Debugf(string, ...any)
	Debugv(any)
	Debugw(string, ...LogField)
	Error(...any)
	Errorf(string, ...any)
	Errorv(any)
	Errorw(string, ...LogField)
	Info(...any)
	Infof(string, ...any)
	Infov(any)
	Infow(string, ...LogField)
	Slow(...any)
	Slowf(string, ...any)
	Slowv(any)
	Sloww(string, ...LogField)
	WithCallerSkip(skip int) Logger
	WithContext(ctx context.Context) Logger
	WithDuration(d time.Duration) Logger
	WithFields(fields ...LogField) Logger
}
```

### 示例代码

```go
var logger logx.Logger = logx.WithContext(context.Background())

logger.Info("This is an info log")
logger.Debugf("Debug log with value: %d", 42)
logger.Errorw("Error occurred", logx.Field("error_code", 500))
```

### 6. `NewLessLogger`

创建一个间隔一定时间内只记录一次日志的 `LessLogger`。

```go
func NewLessLogger(milliseconds int) *LessLogger
```

- **参数**:
    - `milliseconds`: 时间间隔（毫秒）。

- **返回值**: 返回 `LessLogger` 对象。

### 示例代码

```go
lessLogger := logx.NewLessLogger(1000)

lessLogger.Error("This error will be logged at most once per second")
```

### 7. `NewWriter`

创建一个新的 `Writer` 实例。

```go
func NewWriter(w io.Writer) Writer
```

- **参数**:
    - `w`: 一个实现了 `io.Writer` 接口的实例。

- **返回值**: 返回 `Writer` 接口的实现。

### 示例代码

```go
file, err := os.Create("app.log")
if err != nil {
	log.Fatal(err)
}
writer := logx.NewWriter(file)
logx.SetWriter(writer)
```

## 日志配置示例

```go
logConf := logx.LogConf{
	ServiceName:      "example-service",
	Mode:             "file",
	Encoding:         "json",
	Path:             "/var/logs",
	Level:            "debug",
	KeepDays:         7,
	MaxContentLength: 1024,
	Compress:         true,
}

err := logx.SetUp(logConf)
if err != nil {
	log.Fatalf("Failed to set up logging: %v", err)
}
```
