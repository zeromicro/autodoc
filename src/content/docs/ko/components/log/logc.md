---
title: logc
description: go-zero의 logc에 대해 설명합니다.
sidebar:
  order: 3

---


## 타입 Definitions

```go
type (
	LogConf  = logx.LogConf
	LogField = logx.LogField
)
```

## 함수

### AddGlobalFields

모든 로그에 표시될 전역 필드를 추가합니다.

```go
func AddGlobalFields(fields ...LogField)
```

예제:

```go
logc.AddGlobalFields(logc.Field("app", "exampleApp"))
```

### Alert

alert 레벨로 로그 메시지를 남기며, 메시지는 오류 로그에 기록됩니다.

```go
func Alert(_ context.Context, v string)
```

예제:

```go
logc.Alert(context.Background(), "This is an alert message")
```

### 닫기

Closes 로깅 시스템.

```go
func Close() error
```

예제:

```go
if err := logc.Close(); err != nil {
    fmt.Println("Error closing log system:", err)
}
```

### Debug

debug 레벨로 로그 메시지를 남깁니다.

```go
func Debug(ctx context.Context, v ...interface{})
```

예제:

```go
logc.Debug(context.Background(), "This is a debug message")
```

### Debugf

debug 레벨로 포맷된 로그 메시지를 남깁니다.

```go
func Debugf(ctx context.Context, format string, v ...interface{})
```

예제:

```go
logc.Debugf(context.Background(), "This is a %s message", "formatted debug")
```

### Debugv

debug 레벨로 JSON 내용을 로그에 남깁니다.

```go
func Debugv(ctx context.Context, v interface{})
```

예제:

```go
logc.Debugv(context.Background(), map[string]interface{}{"key": "value"})
```

### Debugw

debug 레벨로 필드가 포함된 로그 메시지를 남깁니다.

```go
func Debugw(ctx context.Context, msg string, fields ...LogField)
```

예제:

```go
logc.Debugw(context.Background(), "Debug message with fields", logc.Field("key", "value"))
```

### 오류

로그 메시지 at 오류 level.

```go
func Error(ctx context.Context, v ...any)
```

예제:

```go
logc.Error(context.Background(), "This is an error message")
```

### Errorf

error 레벨로 포맷된 로그 메시지를 남깁니다.

```go
func Errorf(ctx context.Context, format string, v ...any)
```

예제:

```go
logc.Errorf(context.Background(), "This is a %s message", "formatted error")
```

### Errorv

error 레벨로 JSON 내용을 로그에 남깁니다.

```go
func Errorv(ctx context.Context, v any)
```

예제:

```go
logc.Errorv(context.Background(), map[string]interface{}{"error": "something went wrong"})
```

### Errorw

로그 메시지 사용하여 필드 at 오류 level.

```go
func Errorw(ctx context.Context, msg string, fields ...LogField)
```

예제:

```go
logc.Errorw(context.Background(), "Error message with fields", logc.Field("key", "value"))
```

### 필드

반환 로그 필드 위한 given key과 value.

```go
func Field(key string, value any) LogField
```

예제:

```go
field := logc.Field("key", "value")
```

### Info

info 레벨로 로그 메시지를 남깁니다.

```go
func Info(ctx context.Context, v ...any)
```

예제:

```go
logc.Info(context.Background(), "This is an info message")
```

### Infof

info 레벨로 포맷된 로그 메시지를 남깁니다.

```go
func Infof(ctx context.Context, format string, v ...any)
```

예제:

```go
logc.Infof(context.Background(), "This is a %s message", "formatted info")
```

### Infov

info 레벨로 JSON 내용을 로그에 남깁니다.

```go
func Infov(ctx context.Context, v any)
```

예제:

```go
logc.Infov(context.Background(), map[string]interface{}{"info": "some information"})
```

### Infow

info 레벨로 필드가 포함된 로그 메시지를 남깁니다.

```go
func Infow(ctx context.Context, msg string, fields ...LogField)
```

예제:

```go
logc.Infow(context.Background(), "Info message with fields", logc.Field("key", "value"))
```

### Must

error가 nil인지 확인하고, nil이 아니면 오류를 기록한 뒤 프로그램을 종료합니다.

```go
func Must(err error)
```

예제:

```go
logc.Must(errors.New("fatal error"))
```

### Must설정

주어진 설정으로 로깅을 초기화합니다. 오류가 있으면 종료합니다.

```go
func Must설정(c logx.LogConf)
```

예제:

```go
config := logx.LogConf{
    ServiceName: "exampleService",
    Mode:        "console",
}
logc.Must설정(config)
```

### SetLevel

일부 로그를 숨기도록 로그 레벨을 설정합니다.

```go
func SetLevel(level uint32)
```

예제:

```go
logc.SetLevel(logx.LevelInfo)
```

### SetUp


```go
func SetUp(c LogConf) error
```

예제:

```go
config := logc.LogConf{
    ServiceName: "exampleService",
    Mode:        "console",
}
if err := logc.SetUp(config); err != nil {
    fmt.Println("Error setting up log system:", err)
}
```

### 느린

로그 메시지 at 느린 로그 level.

```go
func Slow(ctx context.Context, v ...any)
```

예제:

```go
logc.Slow(context.Background(), "This is a slow log message")
```

### Slowf

slow 로그 레벨로 포맷된 로그 메시지를 남깁니다.

```go
func Slowf(ctx context.Context, format string, v ...any)
```

예제:

```go
logc.Slowf(context.Background(), "This is a %s message", "formatted slow log")
```

### Slowv

slow 로그 레벨로 JSON 내용을 로그에 남깁니다.

```go
func Slowv(ctx context.Context, v any)
```

예제:

```go
logc.Slowv(context.Background(), map[string]interface{}{"slow": "operation details"})
```

### Sloww

로그 메시지 사용하여 필드 at 느린 로그 level.

```go
func Sloww(ctx context.Context, msg string, fields ...LogField)
```

예제:

```go
logc.Sloww(context.Background(), "Slow log message with fields", logc.Field("key", "value"))
```
