---
title: logx
description: Structured logging with go-zero logx.
sidebar:
  order: 2

---


## Types and Method Descriptions

### 1. `LogConf`

`LogConf` is a logging configuration struct used to set various log-related parameters.

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

Add color to a string in plain encoding.

```go
func WithColor(text string, colour color.Color) string
```

- **Parameters**:
    - `text`: The text to be colored.
    - `colour`: The color object.

- **Returns**: Returns the colored string.

### Example Code

```go
import "github.com/fatih/color"

text := "Hello, World!"
coloredText := logx.WithColor(text, color.FgRed)
fmt.Println(coloredText)
```

### 3. `AddGlobalFields`

Add global fields which will be appended to all log entries.

```go
func AddGlobalFields(fields ...LogField)
```

- **Parameters**:
    - `fields`: The global fields to add.

### Example Code

```go
logx.AddGlobalFields(logx.Field("service", "my-service"))
```

### 4. `ContextWithFields`

Return a new context with the given fields.

```go
func ContextWithFields(ctx context.Context, fields ...LogField) context.Context
```

- **Parameters**:
    - `ctx`: The context object.
    - `fields`: The fields to add to the context.

- **Returns**: Returns a new context object.

### Example Code

```go
ctx := context.Background()
ctx = logx.ContextWithFields(ctx, logx.Field("request_id", "12345"))
```

### 5. `Logger` Interface

The `Logger` interface defines methods for logging.

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

### Example Code

```go
var logger logx.Logger = logx.WithContext(context.Background())

logger.Info("This is an info log")
logger.Debugf("Debug log with value: %d", 42)
logger.Errorw("Error occurred", logx.Field("error_code", 500))
```

### 6. `NewLessLogger`

Create a `LessLogger` that logs at most once during the given duration.

```go
func NewLessLogger(milliseconds int) *LessLogger
```

- **Parameters**:
    - `milliseconds`: Time interval in milliseconds.

- **Returns**: Returns a `LessLogger` object.

### Example Code

```go
lessLogger := logx.NewLessLogger(1000)

lessLogger.Error("This error will be logged at most once per second")
```

### 7. `NewWriter`

Create a new instance of `Writer`.

```go
func NewWriter(w io.Writer) Writer
```

- **Parameters**:
    - `w`: An instance implementing the `io.Writer` interface.

- **Returns**: Returns an implementation of the `Writer` interface.

### Example Code

```go
file, err := os.Create("app.log")
if err != nil {
	log.Fatal(err)
}
writer := logx.NewWriter(file)
logx.SetWriter(writer)
```

## Logging Configuration Example

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
