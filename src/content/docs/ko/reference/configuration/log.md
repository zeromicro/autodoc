---
title: 로그 설정
description: go-zero의 로그 설정에 대해 설명합니다.
sidebar:
  order: 6

---


## 로그 개요


```go
var c logc.LogConf
logc.Must설정(c)

logc.Info(context.Background(), "log")
// do your job
```

Our 로그 is 참조d 통해 serviceConf과 will be 자동으로 initialized 때 service은 started입니다.

## Definition 의 매개변수

LogConf 설정 definition below：

```go
package logx

// A, LogConf 예시입니다
type LogConf struct {
    ServiceName         string `json:",optional"`
    Mode                string `json:",default=console,options=[console,file,volume]"`
    Encoding            string `json:",default=json,options=[json,plain]"`
    TimeFormat          string `json:",optional"`
    Path                string `json:",default=logs"`
    Level               string `json:",default=info,options=[debug,info,error,severe]"`
    MaxContentLength    uint32 `json:",optional"`
    Compress            bool   `json:",optional"`
    Stat                bool   `json:",default=true"` // go-zero 版本 >= 1.5.0 才支持
    KeepDays            int    `json:",optional"`
    StackCooldownMillis int    `json:",default=100"`
    // MaxBackups 예시입니다
    // size, Only, RotationRuleType 예시입니다
    // MaxBackups, Even 예시입니다
    // KeepDays 예시입니다
    MaxBackups int `json:",default=0"`
    // MB, MaxSize 예시입니다
    // size, Only, RotationRuleType 예시입니다
    MaxSize int `json:",default=0"`
    // daily, RotationRuleType, Default 예시입니다
    // 예시입니다
    // 예시입니다
    Rotation string `json:",default=daily,options=[daily,size]"`
}

```

| Params              | DataType | 기본값 value | 참고                                                                                    | Enum Values             |
| ------------------- | -------- | ------------- | --------------------------------------------------------------------------------------- | ----------------------- |
| ServiceName         | string   |               | Service Name                                                                            |                         |
| Mode                | string   | console       | 로그 Printing Mode, console Console                                                      | 파일, console           |
| Encoding            | string   | json          | 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.                                             | json, plain             |
| TimeFormat          | string   |               | Date Format                                                                             |                         |
| 경로                | string   | 로그          | 로그 출력 경로 에서 파일 출력 mode                                                     |                         |
| Level               | string   | info          | 로그 출력 level                                                                        | debug,info,오류,severe |
| MaxContentLength    | uint32   | 0             | 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다. |                         |
| Compress            | bool     | false         | Whether 로 compress 로그                                                                |                         |
| Stat                | bool     | true          | Whether 로 비활성화 stat 로그, go-zero 버전 is greater than 1.5.0                      |                         |
| KeepDays            | int      | 0             | 로그 number 의 days left, 만 에서 파일 mode                                              |                         |
| StackCooldownMillis | int      | 100           | Stack print cooldown time                                                               |                         |
| MaxBackups          | int      | 0             | 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.              |                         |
| MaxSize             | int      | 0             | 파일 출력 mode, single 파일 크기 때 split 통해 크기                                   |                         |
| Rotation            | string   | daily         | 파일 split mode, daily 통해 date                                                          | daily,크기              |
