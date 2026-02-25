---
title: goctl 配置
description: 管理 goctl 配置。
sidebar:
  order: 10

---


## 概述

goctl config 是 用于对 goctl 静态配置文件做管理。
goctl config 的目录是根据工程项目来寻找的，以 goctl 可执行文件当前所在工作目录，寻找当前工作目录处在的 go module 或者 go
path空间，然后在该空间下对 `goctl.yaml` 进行管理。
如果当前工作目录下没有 go module 则会自动根据工作目录名称创建 go.mod 文件。

## goctl config 指令

```bash
$ goctl config --help
Usage:
  goctl config [command]

Available Commands:
  clean       Clean goctl config file
  init        Initialize goctl config file

Flags:
  -h, --help   help for config


Use "goctl config [command] --help" for more information about a command.
```

### init

初始化 goctl 静态配置文件。

```bash
$ goctl config init --help
Initialize goctl config file

Usage:
  goctl config init [flags]

Flags:
  -h, --help   help for init
```

### clean

删除 goctl 配置文件。

```bash
$ goctl config clean --help
Clean goctl config file

Usage:
  goctl config clean [flags]

Flags:
  -h, --help   help for clean
```

## 配置说明

goctl config 目前暂时仅支持对 model 数据类型映射的配置，其他配置将根据需要加入。

goctl config 初始化后会在项目工程中创建一个 goctl.yaml 文件，其内容如下：

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

| <img width={100}/> 字段名称 | <img width={200}/> 说明                                         |
|-------------------------|---------------------------------------------------------------|
| model                   | model 配置                                                      |
| model.types_map         | model 配置之类型映射规则，是一个 map<string,obj> 结构，key 为数据库类型，value 为映射对象 |

model 的 golang 结构体

```go
// Model defines the configuration for the model code generation.
Model struct {
    // 类型映射
    TypesMap map[string]ModelTypeMapOption `yaml:"types_map,omitempty" `
}

// ModelTypeMapOption custom Type Options.
ModelTypeMapOption struct {
    // 数据库类型名称，不需要附加约束（如：长度等）如 bigint,varchar
    Type string `yaml:"type"`

    // 当数据类型为 unsigned 修饰时需要映射的 golang 映射类型
    UnsignedType string `yaml:"unsigned_type,omitempty"`

    // 当数据类型允许为 null且没有默认值时需要映射的 golang 映射类型，此优先级高于 unsigned 约束
    NullType string `yaml:"null_type,omitempty"`

    // 当被映射的 golang 类型为外部包时，需要指定包名。
    Pkg string `yaml:"pkg,omitempty"`
}
```

数据库类型映射示例：将 decimal 映射为三方的 decimal.Decimal 包，其在 yaml 的表现为灰色底纹部分：

```yaml {10-13}
model:
  types_map:
    bigint: # 当数据字段类型为 bigint 时，
      # 1. 如果允许 null 且没有默认值时 golang 类型映射为 sql.NullInt64
      # 2. 如果不允许 null 或者有默认值，则 golang 类型映射为 int64
      # 3. 如果不允许 null 或者有默认值，且为 unsigned 修饰，则 golang 类型映射为 uint64
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

## 使用示例

### 在不存在 go module 的目录下初始化配置

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

### 在存在 go module 的目录下初始化配置

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

### 清除配置

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
