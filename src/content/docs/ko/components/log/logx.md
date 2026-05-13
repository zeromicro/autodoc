---
title: logx
description: go-zero logx를 사용한 구조화 로깅입니다.
sidebar:
  order: 2

---


## 타입과 메서드 설명

### 1. `LogConf`

`LogConf`는 로그와 관련된 여러 매개변수를 설정하는 로깅 설정 구조체입니다.

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

`plain` encoding 문자열에 색상을 추가합니다.

```go
func WithColor(text string, colour color.Color) string
```

- **매개변수**:
  - `text`: 색상을 적용할 텍스트입니다.
  - `colour`: 색상 객체입니다.

- **반환**: 색상이 적용된 문자열을 반환합니다.

### 예제 코드

```go
import "github.com/fatih/color"

text := "Hello, World!"
coloredText := logx.WithColor(text, color.FgRed)
fmt.Println(coloredText)
```

### 3. `AddGlobalFields`

모든 로그 항목에 붙을 전역 필드를 추가합니다.

```go
func AddGlobalFields(fields ...LogField)
```

- **매개변수**:
  - `fields`: 추가할 전역 필드입니다.

### 예제 코드

```go
logx.AddGlobalFields(logx.Field("service", "my-service"))
```

### 4. `ContextWithFields`

주어진 필드가 포함된 새 context를 반환합니다.

```go
func ContextWithFields(ctx context.Context, fields ...LogField) context.Context
```

- **매개변수**:
  - `ctx`: context 객체입니다.
  - `fields`: context에 추가할 필드입니다.

- **반환**: 새 context 객체를 반환합니다.

### 예제 코드

```go
ctx := context.Background()
ctx = logx.ContextWithFields(ctx, logx.Field("request_id", "12345"))
```

### 5. `Logger` 인터페이스

`Logger` 인터페이스는 로깅 메서드를 정의합니다.

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

### 예제 코드

```go
var logger logx.Logger = logx.WithContext(context.Background())

logger.Info("This is an info log")
logger.Debugf("Debug log with value: %d", 42)
logger.Errorw("Error occurred", logx.Field("error_code", 500))
```

### 6. `NewLessLogger`

주어진 기간 동안 최대 한 번만 로그를 남기는 `LessLogger`를 생성합니다.

```go
func NewLessLogger(milliseconds int) *LessLogger
```

- **매개변수**:
  - `milliseconds`: 밀리초 단위 시간 간격입니다.

- **반환**: `LessLogger` 객체를 반환합니다.

### 예제 코드

```go
lessLogger := logx.NewLessLogger(1000)

lessLogger.Error("This error will be logged at most once per second")
```

### 7. `NewWriter`

새 `Writer` 인스턴스를 생성합니다.

```go
func NewWriter(w io.Writer) Writer
```

- **매개변수**:
  - `w`: `io.Writer` 인터페이스를 구현한 인스턴스입니다.

- **반환**: `Writer` 인터페이스 구현체를 반환합니다.

### 예제 코드

```go
file, err := os.Create("app.log")
if err != nil {
	log.Fatal(err)
}
writer := logx.NewWriter(file)
logx.SetWriter(writer)
```

## 로깅 설정 예제

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
