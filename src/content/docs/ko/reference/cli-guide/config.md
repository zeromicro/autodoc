---
title: goctl 설정
description: go-zero의 goctl 설정에 대해 설명합니다.
sidebar:
  order: 10

---


##개요

Goctl config은 사용되어 manage goctl static 설정 파일s입니다.
경우 there is 없음 go 모듈 에서 current 작동 디렉터리, `go.mod` file은 자동으로 created based 에서 작동 디렉터리 name입니다.

## goctl 설정 명령

```bash
$ goctl config --help
Usage:
  goctl config [command]

Available 명령s:
  clean       Clean goctl config file
  init        Initialize goctl config file

Flags:
  -h, --help   help for config


Use "goctl config [command] --help" for more information about a command.
```

### init

Initialize goctl static 설정 파일.

```bash
$ goctl config init --help
Initialize goctl config file

Usage:
  goctl config init [flags]

Flags:
  -h, --help   help for init
```

### clean

Delete goctl 설정 파일.

```bash
$ goctl config clean --help
Clean goctl config file

Usage:
  goctl config clean [flags]

Flags:
  -h, --help   help for clean
```

## 설정 instructions


```yaml
model:
  types_map:
    bigint:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    dec:
      null_type: sql.NullFloat64
      type: float64
    decimal:
      null_type: sql.NullFloat64
      type: float64
    double:
      null_type: sql.NullFloat64
      type: float64
    float:
      null_type: sql.NullFloat64
      type: float64
    float4:
      null_type: sql.NullFloat64
      type: float64
    float8:
      null_type: sql.NullFloat64
      type: float64
    int:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    int1:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    int2:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    int3:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    int4:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    int8:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    integer:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    mediumint:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    middleint:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    smallint:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    tinyint:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    date:
      null_type: sql.NullTime
      type: time.Time
    datetime:
      null_type: sql.NullTime
      type: time.Time
    timestamp:
      null_type: sql.NullTime
      type: time.Time
    time:
      null_type: sql.NullString
      type: string
    year:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    bit:
      null_type: sql.NullByte
      type: byte
      unsigned_type: byte
    bool:
      null_type: sql.NullBool
      type: bool
    boolean:
      null_type: sql.NullBool
      type: bool
    char:
      null_type: sql.NullString
      type: string
    varchar:
      null_type: sql.NullString
      type: string
    nvarchar:
      null_type: sql.NullString
      type: string
    nchar:
      null_type: sql.NullString
      type: string
    character:
      null_type: sql.NullString
      type: string
    longvarchar:
      null_type: sql.NullString
      type: string
    linestring:
      null_type: sql.NullString
      type: string
    multilinestring:
      null_type: sql.NullString
      type: string
    binary:
      null_type: sql.NullString
      type: string
    varbinary:
      null_type: sql.NullString
      type: string
    tinytext:
      null_type: sql.NullString
      type: string
    text:
      null_type: sql.NullString
      type: string
    mediumtext:
      null_type: sql.NullString
      type: string
    longtext:
      null_type: sql.NullString
      type: string
    enum:
      null_type: sql.NullString
      type: string
    set:
      null_type: sql.NullString
      type: string
    json:
      null_type: sql.NullString
      type: string
    blob:
      null_type: sql.NullString
      type: string
    longblob:
      null_type: sql.NullString
      type: string
    mediumblob:
      null_type: sql.NullString
      type: string
    tinyblob:
      null_type: sql.NullString
      type: string
```

| <img width={100}/> 필드 | <img width={200}/> 설명                                |
|--------------------------|---------------------------------------------------------------|
| 모델                    | 모델 코드 생성 related 설정                                                       |
| 모델.types_map          | 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다. |

모델 golang structure

```go
// Model 예시입니다
Model struct {
    // 예시입니다
    TypesMap map[string]ModelTypeMapOption `yaml:"types_map,omitempty" `
}

// ModelTypeMapOption, Type, Options 예시입니다
ModelTypeMapOption struct {
    // Database 예시입니다
    Type string `yaml:"type"`

    // 예시입니다
    UnsignedType string `yaml:"unsigned_type,omitempty"`

    // 예시입니다
    NullType string `yaml:"null_type,omitempty"`

    // 예시입니다
    Pkg string `yaml:"pkg,omitempty"`
}
```


```yaml {10-13}
model:
  types_map:
    bigint: # 예시입니다
      # If, NullInt64 예시입니다
      # If 예시입니다
      # If 예시입니다
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    dec:
      null_type: sql.NullFloat64
      type: float64
    decimal:
      null_type: decimal.NullDecimal
      pkg: github.com/shopspring/decimal
      type: decimal.Decimal
    ...
```

## 예제

### Initialize 설정 에서 디렉터리 where there is 없음 go 모듈

```bash
$ ll
total 0
$ goctl config init
goctl.yaml generated in ~/demo/goctl-config/goctl.yaml
$ ls
go.mod     goctl.yaml
$ cat go.mod
module goctl-config

go 1.20
```

### Initialize 설정 에서 디렉터리 where go 모듈 exists

```bash
$ ll
total 8
-rw-r--r--  1 ***  staff    29B Apr 10 16:35 go.mod
$ goctl config init
goctl.yaml generated in ~/demo/goctl-config/goctl.yaml
$ ll
total 16
-rw-r--r--  1 ***  staff    29B Apr 10 16:35 go.mod
-rw-r--r--  1 ***  staff   3.3K Apr 10 16:37 goctl.yaml
```

### clear 설정

```bash
$ ll
total 16
-rw-r--r--  1 ***  staff    29B Apr 10 16:35 go.mod
-rw-r--r--  1 ***  staff   3.3K Apr 10 16:37 goctl.yaml
$ goctl config clean
$ ll
total 8
-rw-r--r--  1 ***  staff    29B Apr 10 16:35 go.mod
```
