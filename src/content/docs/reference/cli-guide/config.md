---
title: goctl Configuration
description: Manage goctl configuration.
sidebar:
  order: 10

---


##Overview

Goctl config is used to manage goctl static configuration files.
The directory of goctl config is found according to the project. In the working directory where the goctl executable is currently located, find the go module or go where the current working directory is located.
Path space, and then manage `goctl.yaml` under that space.
If there is no go module in the current working directory, a `go.mod` file is automatically created based on the working directory name.

## goctl config command

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

Initialize the goctl static configuration file.

```bash
$ goctl config init --help
Initialize goctl config file

Usage:
  goctl config init [flags]

Flags:
  -h, --help   help for init
```

### clean

Delete the goctl configuration file.

```bash
$ goctl config clean --help
Clean goctl config file

Usage:
  goctl config clean [flags]

Flags:
  -h, --help   help for clean
```

## configuration instructions

The goctl config currently only supports the configuration of the model data type mapping, and other configurations will be added as needed.

After goctl config is initialized, a goctl.yaml file will be created in the project, with the following contents:

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

| <img width={100}/> Field | <img width={200}/> Description                                |
|--------------------------|---------------------------------------------------------------|
| model                    | Model code generation related configuration                                                       |
| model.types_map          | The type mapping rule of the model configuration is a map <string, obj> structure, the key is the database type, and the value is the mapping object |

Model golang structure

```go
// Model defines the configuration for the model code generation.
Model struct {
    // type mapping
    TypesMap map[string]ModelTypeMapOption `yaml:"types_map,omitempty" `
}

// ModelTypeMapOption custom Type Options.
ModelTypeMapOption struct {
    // Database type name, no additional constraints (e.g. length, etc.) such as bigint, varchar
    Type string `yaml:"type"`

    // The golang mapping type that needs to be mapped when the data type is unsigned
    UnsignedType string `yaml:"unsigned_type,omitempty"`

    // The golang mapped type that needs to be mapped when the data type is allowed to be null and there is no default value, this takes precedence over the unsigned constraint
    NullType string `yaml:"null_type,omitempty"`

    // When the mapped golang type is an external package, you need to specify the package name.
    Pkg string `yaml:"pkg,omitempty"`
}
```

Database type mapping example: Mapping decimal to a three-way decimal. Decimal package, which appears as a gray shading section in yaml:

```yaml {10-13}
model:
  types_map:
    bigint: # When the data field type is bigint,
      # 1. If null is allowed and there is no default value, the golang type maps to sql.NullInt64.
      # 2. If null is not allowed or there is a default value, the golang type maps to int64.
      # 3. If null is not allowed or has a default value and is unsigned, the golang type maps to uint64.
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

## Example

### Initialize the configuration in a directory where there is no go module

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

### Initialize the configuration in the directory where the go module exists

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

### clear configuration

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
