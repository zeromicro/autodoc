---
title: 설정 자동 검증
description: go-zero의 설정 자동 검증에 대해 설명합니다.
sidebar:
  order: 7

---


## 자동 설정 검증


## 작동 방식


1. Implement `Validator` interface 에서 your 설정 struct:

```go
type YourConfig struct {
    Name     string
    MaxUsers int
}

// Implement, Validator 예시입니다
func (c YourConfig) Validate() error {
    if len(c.Name) == 0 {
        return errors.New("name cannot be empty")
    }
    if c.MaxUsers <= 0 {
        return errors.New("max users must be positive")
    }
    return nil
}
```

2. 사용 설정 로서 usual - 검증 happens 자동으로:

```go
var config YourConfig
err := conf.Load("config.yaml", &config)
if err != nil {
    // AND 예시입니다
    log.Fatal(err)
}
```

## Key Benefits

4. **타입 Safety**: 검증 is tied 로 your 설정 structs

## 예제 사용 Cases


```go
type DatabaseConfig struct {
    Host     string
    Port     int
    MaxConns int
}

func (c DatabaseConfig) Validate() error {
    if len(c.Host) == 0 {
        return errors.New("database host cannot be empty")
    }
    if c.Port <= 0 || c.Port > 65535 {
        return errors.New("invalid port number")
    }
    if c.MaxConns <= 0 {
        return errors.New("max connections must be positive")
    }
    return nil
}
```

## 구현 세부 사항


## 시작하기


## 모범 사례

1. Keep 검증 rules 간단한과 focused 에서 설정 validity
2. 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.
3. Consider adding 검증 위한 모든 critical 설정 values
