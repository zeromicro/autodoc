---
title: goctl Model
description: go-zero의 goctl Model에 대해 설명합니다.
sidebar:
  order: 6

---

## 개요


## goctl 모델 directive

```bash
$ goctl model  --help
Generate model code

Usage:
  goctl model [command]

Available 명령s:
  mongo       Generate mongo model
  mysql       Generate mysql model
  pg          Generate postgresql model

Flags:
  -h, --help   help for model

Use "goctl model [command] --help" for more information about a command.
```

### goctl 모델 mono directive


```bash
$ goctl model mongo --help
Generate mongo model

Usage:
  goctl model mongo [flags]

Flags:
      --branch string   The branch of the remote repo, it does work with --remote
  -c, --cache           Generate code with cache [optional]
  -d, --dir string      The target dir
  -e, --easy            Generate code with auto generated CollectionName for easy declare [optional]
  -h, --help            help for mongo
      --home string     The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --remote string   The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                        The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure
      --style string    The file naming format, see [https://github.com/zeromicro/go-zero/tree/master/tools/goctl/config/readme.md]
  -t, --type strings    Specified model type name
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                                                        |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| branch                                               | string                                              | 없음                                             | Empty string                                       | 원격 템플릿 name is 사용됨 만 경우 `remote` has value                                                           |
| 캐시                                                | boolean                                             | 없음                                             | `false`                                            | Whether 또는 아님 로 생성 code 사용하여 캐시                                                                        |
| dir                                                  | string                                              | 없음                                             | Current 작동 디렉터리                          | 생성 Code 출력 디렉터리                                                                                    |
| easy                                                 | boolean                                             | 없음                                             | `false`                                            | Exposure pool name variable                                                                                       |
| home                                                 | string                                              | 없음                                             | `${HOME}/.goctl`                                   | 로컬 템플릿 파일 디렉터리                                                                                     |
| 원격                                               | string                                              | 없음                                             | Empty string                                       |해당 항목의 동작과 사용법을 설명합니다. |
| 스타일                                                | string                                              | 없음                                             | `gozero`                                           | Named 스타일 symbols 위한 출력 파일과 디렉터리, see [파일 스타일](./style.md)                                |
| 타입                                                 | []string                                            | YES                                            | `nil`                                              | Structure 타입 Name                                                                                               |

#### 예제

Below은 예제 의 generating user structure입니다.

1 Whether 또는 아님 로 생성 code 사용하여 캐시

```bash
# 예시입니다
$ cd ~

# 예시입니다
$ mkdir demo && cd demo

# 예시입니다
$ goctl model mongo --type User --dir cache --cache

# 예시입니다
$ tree
.
└── cache
    ├── error.go
    ├── usermodel.go
    ├── usermodelgen.go
    └── usertypes.go

1 directory, 4 files

```

View code

**오류.go**
```go
package model

import (
    "errors"

    "github.com/zeromicro/go-zero/core/stores/mon"
)

var (
    ErrNotFound        = mon.ErrNotFound
    ErrInvalidObjectId = errors.New("invalid objectId")
)
```

**usermodel.go**
```go
package model

import (
    "github.com/zeromicro/go-zero/core/stores/cache"
    "github.com/zeromicro/go-zero/core/stores/monc"
)

var _ UserModel = (*customUserModel)(nil)

type (
    // 사용합니다
    // 예시입니다
    UserModel interface {
        userModel
    }

    customUserModel struct {
        *defaultUserModel
    }
)

// NewUserModel 예시입니다
func NewUserModel(url, db, collection string, c cache.CacheConf) UserModel {
    conn := monc.MustNewModel(url, db, collection, c)
    return &customUserModel{
        defaultUserModel: newDefaultUserModel(conn),
    }
}
```

**usermodelgen.go**
```go
// 이 코드는 직접 수정하지 마세요
package model

import (
    "context"
    "time"

    "github.com/zeromicro/go-zero/core/stores/monc"
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/bson/primitive"
)

var prefixUserCacheKey = "cache:user:"

type userModel interface {
    Insert(ctx context.Context, data *User) error
    FindOne(ctx context.Context, id string) (*User, error)
    Update(ctx context.Context, data *User) error
    Delete(ctx context.Context, id string) error
}

type defaultUserModel struct {
    conn *monc.Model
}

func newDefaultUserModel(conn *monc.Model) *defaultUserModel {
    return &defaultUserModel{conn: conn}
}

func (m *defaultUserModel) Insert(ctx context.Context, data *User) error {
    if data.ID.IsZero() {
        data.ID = primitive.NewObjectID()
        data.CreateAt = time.Now()
        data.UpdateAt = time.Now()
    }

    key := prefixUserCacheKey + data.ID.Hex()
    _, err := m.conn.InsertOne(ctx, key, data)
    return err
}

func (m *defaultUserModel) FindOne(ctx context.Context, id string) (*User, error) {
    oid, err := primitive.ObjectIDFromHex(id)
    if err != nil {
        return nil, ErrInvalidObjectId
    }

    var data User
    key := prefixUserCacheKey + id
    err = m.conn.FindOne(ctx, key, &data, bson.M{"_id": oid})
    switch err {
    case nil:
        return &data, nil
    case monc.ErrNotFound:
        return nil, ErrNotFound
    default:
        return nil, err
    }
}

func (m *defaultUserModel) Update(ctx context.Context, data *User) error {
    data.UpdateAt = time.Now()
    key := prefixUserCacheKey + data.ID.Hex()
    _, err := m.conn.ReplaceOne(ctx, key, bson.M{"_id": data.ID}, data)
    return err
}

func (m *defaultUserModel) Delete(ctx context.Context, id string) error {
    oid, err := primitive.ObjectIDFromHex(id)
    if err != nil {
        return ErrInvalidObjectId
    }
    key := prefixUserCacheKey + id
    _, err = m.conn.DeleteOne(ctx, key, bson.M{"_id": oid})
    return err
}
```

**usertypes.go**
```go
package model

import (
    "time"

    "go.mongodb.org/mongo-driver/bson/primitive"
)

type User struct {
    ID primitive.ObjectID `bson:"_id,omitempty" json:"id,omitempty"`
    // TODO: 필요한 로직을 작성하세요
    UpdateAt time.Time `bson:"updateAt,omitempty" json:"updateAt,omitempty"`
    CreateAt time.Time `bson:"createAt,omitempty" json:"createAt,omitempty"`
}
```

2 생성 code 없이 캐시

```bash
# 예시입니다
$ cd ~

# 예시입니다
$ mkdir demo && cd demo

# 예시입니다
$ goctl model mongo --type User --dir nocache

# 예시입니다
$ tree
.
└── nocache
    ├── error.go
    ├── usermodel.go
    ├── usermodelgen.go
    └── usertypes.go

1 directory, 4 files
```

View code

**오류.go**
```go
package model

import (
    "errors"

    "github.com/zeromicro/go-zero/core/stores/mon"
)

var (
    ErrNotFound        = mon.ErrNotFound
    ErrInvalidObjectId = errors.New("invalid objectId")
)
```

**usermodel.go**
```go
package model

import "github.com/zeromicro/go-zero/core/stores/mon"

var _ UserModel = (*customUserModel)(nil)

type (
    // 사용합니다
    // 예시입니다
    UserModel interface {
        userModel
    }

    customUserModel struct {
        *defaultUserModel
    }
)

// NewUserModel 예시입니다
func NewUserModel(url, db, collection string) UserModel {
    conn := mon.MustNewModel(url, db, collection)
    return &customUserModel{
        defaultUserModel: newDefaultUserModel(conn),
    }
}
```

**usermodelgen.go**
```go
// 이 코드는 직접 수정하지 마세요
package model

import (
    "context"
    "time"

    "github.com/zeromicro/go-zero/core/stores/mon"
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/bson/primitive"
)

type userModel interface {
    Insert(ctx context.Context, data *User) error
    FindOne(ctx context.Context, id string) (*User, error)
    Update(ctx context.Context, data *User) error
    Delete(ctx context.Context, id string) error
}

type defaultUserModel struct {
    conn *mon.Model
}

func newDefaultUserModel(conn *mon.Model) *defaultUserModel {
    return &defaultUserModel{conn: conn}
}

func (m *defaultUserModel) Insert(ctx context.Context, data *User) error {
    if data.ID.IsZero() {
        data.ID = primitive.NewObjectID()
        data.CreateAt = time.Now()
        data.UpdateAt = time.Now()
    }

    _, err := m.conn.InsertOne(ctx, data)
    return err
}

func (m *defaultUserModel) FindOne(ctx context.Context, id string) (*User, error) {
    oid, err := primitive.ObjectIDFromHex(id)
    if err != nil {
        return nil, ErrInvalidObjectId
    }

    var data User

    err = m.conn.FindOne(ctx, &data, bson.M{"_id": oid})
    switch err {
    case nil:
        return &data, nil
    case mon.ErrNotFound:
        return nil, ErrNotFound
    default:
        return nil, err
    }
}

func (m *defaultUserModel) Update(ctx context.Context, data *User) error {
    data.UpdateAt = time.Now()

    _, err := m.conn.ReplaceOne(ctx, bson.M{"_id": data.ID}, data)
    return err
}

func (m *defaultUserModel) Delete(ctx context.Context, id string) error {
    oid, err := primitive.ObjectIDFromHex(id)
    if err != nil {
        return ErrInvalidObjectId
    }

    _, err = m.conn.DeleteOne(ctx, bson.M{"_id": oid})
    return err
}
```

**usertypes.go**
```go
package model

import (
    "time"

    "go.mongodb.org/mongo-driver/bson/primitive"
)

type User struct {
    ID primitive.ObjectID `bson:"_id,omitempty" json:"id,omitempty"`
    // TODO: 필요한 로직을 작성하세요
    UpdateAt time.Time `bson:"updateAt,omitempty" json:"updateAt,omitempty"`
    CreateAt time.Time `bson:"createAt,omitempty" json:"createAt,omitempty"`
}
```

### goctl 모델 mysql directive


```bash
$ goctl model mysql --help
Generate mysql model

Usage:
  goctl model mysql [command]

Available 명령s:
  datasource  Generate model from datasource
  ddl         Generate mysql model from ddl

Flags:
  -h, --help                     help for mysql
  -i, --ignore-columns strings   Ignore columns while creating or updating rows (default [create_at,created_at,create_time,update_at,updated_at,update_time])
      --strict                   Generate model in strict mode
      -p, --prefix string            The cache prefix, effective when --cache is true (default "cache")

Use "goctl model mysql [command] --help" for more information about a command.
```

#### goctl 모델 mysql datasource directive

goctl 모델 mysql datasource instructions은 사용되어 생성 모델 code 에서 데이터베이스 connections입니다.

```bash
$ goctl model mysql datasource --help
Generate model from datasource

Usage:
  goctl model mysql datasource [flags]

Flags:
      --branch string   The branch of the remote repo, it does work with --remote
  -c, --cache           Generate code with cache [optional]
  -d, --dir string      The target dir
  -h, --help            help for datasource
      --home string     The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --idea            For idea plugin [optional]
      --remote string   The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                        The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure
      --style string    The file naming format, see [https://github.com/zeromicro/go-zero/tree/master/tools/goctl/config/readme.md]
  -t, --table strings   The table or table globbing patterns in the database
      --url string      The data source of database,like "root:password@tcp(127.0.0.1:3306)/database"

Global Flags:
  -i, --ignore-columns strings   Ignore columns while creating or updating rows (default [create_at,created_at,create_time,update_at,updated_at,update_time])
      --strict                   Generate model in strict mode
      -p, --prefix string        The cache prefix, effective when --cache is true (default "cache")
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                                                                                                                                                                                                                                                                                                                                 |
|-------------------------------------|------------------------------------| ---------------------------------------------- |-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| branch                              | string                             | 없음                                             | Empty string                      | 원격 템플릿 name is 사용됨 만 경우 `remote` has value                                                                                                                                                                                                                                                                                                                   |
| 캐시                               | boolean                            | 없음                                             | `false`                           | Whether 또는 아님 로 생성 code 사용하여 캐시                                                                                                                                                                                                                                                                                                                                |
| dir                                 | string                             | 없음                                             | Current 작동 디렉터리         | 생성 Code 출력 디렉터리                                                                                                                                                                                                                                                                                                                                            |
| easy                                | boolean                            | 없음                                             | `false`                           | Exposure pool name variable                                                                                                                                                                                                                                                                                                                                               |
| home                                | string                             | 없음                                             | `${HOME}/.goctl`                  | 로컬 템플릿 파일 디렉터리                                                                                                                                                                                                                                                                                                                                             |
| 원격                              | string                             | 없음                                             | Empty string                      |해당 항목의 동작과 사용법을 설명합니다.                                                                                                                                                                                                                                                         |
| 스타일                               | string                             | 없음                                             | `gozero`                          | Named 스타일 symbols 위한 출력 파일과 디렉터리, see [파일 스타일](./style.md)                                                                                                                                                                                                                                                                                        |
| table                               | []string                           | YES                                            | `nil`                             | Table 로 생성 code                                                                                                                                                                                                                                                                                                                                                    |
| URL                                 | string                             | YES                                            | Empty string                      | 데이터베이스 연결,format{{username}}:{{password}}@tcp({{host_port}}) /{{db}}                                                                                                                                                                                                                                                                                            |
| ignore-columns                      | []string                           | 없음                                             | `nil`                             |해당 항목의 동작과 사용법을 설명합니다.                                                                                                                                                                                                                                                                                                |
| strict                              | boolean                            | 없음                                             | `false`                           |해당 항목의 동작과 사용법을 설명합니다. |
| prefix                              | string                             | 없음                                             | `cache`                           |  캐시 prefix, effective 때 --cache is true (기본값 "캐시"), goctl 버전 > 1.7.6                                                                                                                                                                                                                                                                                 |

#### goctl 모델 mysql ddl directive


```bash
$ goctl model mysql ddl --help
Generate mysql model from ddl

Usage:
  goctl model mysql ddl [flags]

Flags:
      --branch string     The branch of the remote repo, it does work with --remote
  -c, --cache             Generate code with cache [optional]
      --database string   The name of database [optional]
  -d, --dir string        The target dir
  -h, --help              help for ddl
      --home string       The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --idea              For idea plugin [optional]
      --remote string     The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                          The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure
  -s, --src string        The path or path globbing patterns of the ddl
      --style string      The file naming format, see [https://github.com/zeromicro/go-zero/tree/master/tools/goctl/config/readme.md]

Global Flags:
  -i, --ignore-columns strings   Ignore columns while creating or updating rows (default [create_at,created_at,create_time,update_at,updated_at,update_time])
      --strict                   Generate model in strict mode
      -p, --prefix string        The cache prefix, effective when --cache is true (default "cache")
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                                                                                                                                                                                                                                                                                                                                 |
|-------------------------------------|------------------------------------| ---------------------------------------------- |-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| branch                              | string                             | 없음                                             | Empty string                      | 원격 템플릿 name is 사용됨 만 경우 `remote` has value                                                                                                                                                                                                                                                                                                                   |
| 캐시                               | boolean                            | 없음                                             | `false`                           | Whether 또는 아님 로 생성 code 사용하여 캐시                                                                                                                                                                                                                                                                                                                                |
| dir                                 | string                             | 없음                                             | Current 작동 디렉터리         | 생성 Code 출력 디렉터리                                                                                                                                                                                                                                                                                                                                            |
| easy                                | boolean                            | 없음                                             | `false`                           | Exposure pool name variable                                                                                                                                                                                                                                                                                                                                               |
| home                                | string                             | 없음                                             | `${HOME}/.goctl`                  | 로컬 템플릿 파일 디렉터리                                                                                                                                                                                                                                                                                                                                             |
| 원격                              | string                             | 없음                                             | Empty string                      |해당 항목의 동작과 사용법을 설명합니다.                                                                                                                                                                                                                                                         |
| src                                 | string                             | YES                                            | Empty string                      | sql 파일 경로                                                                                                                                                                                                                                                                                                                                                             |
| 스타일                               | string                             | 없음                                             | `gozero`                          | Named 스타일 symbols 위한 출력 파일과 디렉터리, see [파일 스타일](./style.md)                                                                                                                                                                                                                                                                                        |
| ignore-columns                      | []string                           | 없음                                             | `nil`                             |해당 항목의 동작과 사용법을 설명합니다.                                                                                                                                                                                                                                                                                                |
| strict                              | boolean                            | 없음                                             | `false`                           |해당 항목의 동작과 사용법을 설명합니다. |
| prefix                              | string                             | 없음                                             | `cache`                           |  캐시 prefix, effective 때 --cache is true (기본값 "캐시"), goctl 버전 > 1.7.6                                                                                                                                                                                                                                                                                 |

#### MySQL 타입 mapping relationships

**strict 为 true 时，且 unsigned 修饰**
| <img width={100} /> MySQL DataType | <img width={200} /> is null constraint? | <img width={400} /> Golang DataType|
| --- | --- | --- |
| bit | 없음 | byte |
| tinyint | 없음 | uint64 |
| tinyint | YES | sql.NullInt64 |
| smallint | 없음 | uint64 |
| smallint | YES | sql.NullInt64 |
| mediumint | 없음 | uint64 |
| mediumint | YES | sql.NullInt64 |
| int | 없음 | uint64 |
| int | YES | sql.NullInt64 |
| middleint | 없음 | uint64 |
| middleint | YES | sql.NullInt64 |
| int1 | 없음 | uint64 |
| int1 | YES | sql.NullInt64 |
| int2 | 없음 | uint64 |
| int2 | YES | sql.NullInt64 |
| int3 | 없음 | uint64 |
| int3 | YES | sql.NullInt64 |
| int4 | 없음 | uint64 |
| int4 | YES | sql.NullInt64 |
| int8 | 없음 | iunt64 |
| int8 | YES | sql.NullInt64 |
| integer | 없음 | uint64 |
| integer | YES | sql.NullInt64 |
| bigint | 없음 | uint64 |
| bigint | YES | sql.NullInt64 |
| float | 없음 | float64 |
| float | YES | sql.NullFloat64 |
| float4 | 없음 | float64 |
| float4 | YES | sql.NullFloat64 |
| float8 | 없음 | float64 |
| float8 | YES | sql.NullFloat64 |
| date | 없음 | time.Time |
| datetime | 없음 | time.Time |
| timstamp | 없음 | time.Time |
| time | 없음 | string |
| year | 없음 | int64 |
| char | 없음 | string |
| varchar | 없음 | string |
| nvarchar | 없음 | string |
| nchar | 없음 | string |
| character | 없음 | string |
| longvarchar | 없음 | string |
| linestring | 없음 | string |
| multilinestring | 없음 | string |
| 바이너리 | 없음 | string |
| varbinary | 없음 | string |
| tinytext | 없음 | string |
| text | 없음 | string |
| mediumtext | 없음 | string |
| longtext | 없음 | string |
| enum | 없음 | string |
| set | 없음 | string |
| json | 없음 | string |
| blob | 없음 | string |
| longblob | 없음 | string |
| mediumblob | 없음 | string |
| tinyblob | 없음 | string |
| bool | 없음 | bool |
| bllean | 없음 | bool |

**strict 不为 true 时**
| <img width={100} /> MySQL 类型 | <img width={200} /> 是否为 null 约束 | <img width={400} /> Golang 类型 |
| --- | --- | --- |
| bit | 없음 | byte |
| tinyint | 없음 | int64 |
| tinyint | YES | sql.NullInt64 |
| smallint | 없음 | int64 |
| smallint | YES | sql.NullInt64 |
| mediumint | 없음 | int64 |
| mediumint | YES | sql.NullInt64 |
| int | 없음 | int64 |
| int | YES | sql.NullInt64 |
| middleint | 없음 | int64 |
| middleint | YES | sql.NullInt64 |
| int1 | 없음 | int64 |
| int1 | YES | sql.NullInt64 |
| int2 | 없음 | int64 |
| int2 | YES | sql.NullInt64 |
| int3 | 없음 | int64 |
| int3 | YES | sql.NullInt64 |
| int4 | 없음 | int64 |
| int4 | YES | sql.NullInt64 |
| int8 | 없음 | int64 |
| int8 | YES | sql.NullInt64 |
| integer | 없음 | int64 |
| integer | YES | sql.NullInt64 |
| bigint | 없음 | int64 |
| bigint | YES | sql.NullInt64 |
| float | 없음 | float64 |
| float | YES | sql.NullFloat64 |
| float4 | 없음 | float64 |
| float4 | YES | sql.NullFloat64 |
| float8 | 없음 | float64 |
| float8 | YES | sql.NullFloat64 |
| date | 없음 | time.Time |
| datetime | 없음 | time.Time |
| timstamp | 없음 | time.Time |
| time | 없음 | string |
| year | 없음 | int64 |
| char | 없음 | string |
| varchar | 없음 | string |
| nvarchar | 없음 | string |
| nchar | 없음 | string |
| character | 없음 | string |
| longvarchar | 없음 | string |
| linestring | 없음 | string |
| multilinestring | 없음 | string |
| 바이너리 | 없음 | string |
| varbinary | 없음 | string |
| tinytext | 없음 | string |
| text | 없음 | string |
| mediumtext | 없음 | string |
| longtext | 없음 | string |
| enum | 없음 | string |
| set | 없음 | string |
| json | 없음 | string |
| blob | 없음 | string |
| longblob | 없음 | string |
| mediumblob | 없음 | string |
| tinyblob | 없음 | string |
| bool | 없음 | bool |
| bllean | 없음 | bool |

### goctl 모델 pg directive

goctl 모델 pg instructions은 사용되어 생성 Go language code 에서 PostgreSQL 데이터베이스입니다.

```bash
$ goctl model pg --help
Generate postgresql model

Usage:
  goctl model pg [flags]
  goctl model pg [command]

Available 명령s:
  datasource  Generate model from datasource

Flags:
  -h, --help   help for pg

Use "goctl model pg [command] --help" for more information about a command.
```

#### goctl 모델 pg datasource directive

```bash
$ goctl model pg datasource --help
Generate model from datasource

Usage:
  goctl model pg datasource [flags]

Flags:
      --branch string   The branch of the remote repo, it does work with --remote
  -c, --cache           Generate code with cache [optional]
  -d, --dir string      The target dir
  -h, --help            help for datasource
      --home string     The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --idea            For idea plugin [optional]
      --remote string   The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                            The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure
  -s, --schema string   The table schema (default "public")
      --strict          Generate model in strict mode
      --style string    The file naming format, see [https://github.com/zeromicro/go-zero/tree/master/tools/goctl/config/readme.md]
  -t, --table string    The table or table globbing patterns in the database
      --url string      The data source of database,like "postgres:// 예시입니다
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                                                                                                                                                                                                                                                                                                                |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| branch                                               | string                                              | 없음                                             | Empty string                                       | 원격 템플릿 name is 사용됨 만 경우 `remote` has value                                                                                                                                                                                                                                                                                                                   |
| 캐시                                                | boolean                                             | 없음                                             | `false`                                            | Whether 또는 아님 로 생성 code 사용하여 캐시                                                                                                                                                                                                                                                                                                                                |
| dir                                                  | string                                              | 없음                                             | Current 작동 디렉터리                          | 생성 Code 출력 디렉터리                                                                                                                                                                                                                                                                                                                                            |
| easy                                                 | boolean                                             | 없음                                             | `false`                                            | Exposure pool name variable                                                                                                                                                                                                                                                                                                                                               |
| home                                                 | string                                              | 없음                                             | `${HOME}/.goctl`                                   | 로컬 템플릿 파일 디렉터리                                                                                                                                                                                                                                                                                                                                             |
| idea                                                 | boolean                                             | 없음                                             | `false`                                            | Whether 로 사용 로서 idea, please ignore this 필드                                                                                                                                                                                                                                                                                                                          |
| 원격                                               | string                                              | 없음                                             | Empty string                                       |해당 항목의 동작과 사용법을 설명합니다.                                                                                                                                                                                                                                                         |
| strict                                               | boolean                                             | 없음                                             | `false`                                            |해당 항목의 동작과 사용법을 설명합니다. |
| 스타일                                                | string                                              | 없음                                             | `gozero`                                           | Named 스타일 symbols 위한 출력 파일과 디렉터리, see [파일 스타일](./style.md)                                                                                                                                                                                                                                                                                        |
| table                                                | []string                                            | YES                                            | `nil`                                              | Table 로 생성 code                                                                                                                                                                                                                                                                                                                                                    |
| URL                                                  | string                                              | YES                                            | Empty string                                       | 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.                                                                                                                                                                                                                                                                  |

#### PostgreSQL 타입 Map Relationships

| <img width={100} /> PostgreSQL 타입 | <img width={800} /> Golang 타입 |
| ---------------------------------------------------- | ------------------------------------------------ |
| bool                                                 | bool                                             |
| _bool                                                | pq.BoolArray                                     |
| boolean                                              | bool                                             |
| tinyint                                              | int64                                            |
| smallint                                             | int64                                            |
| mediumint                                            | int64                                            |
| int                                                  | int64                                            |
| int1                                                 | int64                                            |
| int2                                                 | int64                                            |
| _int2                                                | pq.Int64Array                                    |
| int3                                                 | int64                                            |
| int4                                                 | int64                                            |
| _int4                                                | pq.Int64Array                                    |
| int8                                                 | int64                                            |
| _int8                                                | pq.Int64Array                                    |
| integer                                              | int64                                            |
| _integer                                             | pq.Int64Array                                    |
| bigint                                               | int64                                            |
| float                                                | float64                                          |
| float4                                               | float64                                          |
| _float4                                              | pq.Float64Array                                  |
| float8                                               | float64                                          |
| _float8                                              | pq.Float64Array                                  |
| double                                               | float64                                          |
| decimal                                              | float64                                          |
| dec                                                  | float64                                          |
| fixed                                                | float64                                          |
| real                                                 | float64                                          |
| bit                                                  | byte                                             |
| date                                                 | time.Time                                        |
| datetime                                             | time.Time                                        |
| timestamp                                            | time.Time                                        |
| time                                                 | string                                           |
| year                                                 | int64                                            |
| linestring                                           | string                                           |
| multilinestring                                      | string                                           |
| nvarchar                                             | string                                           |
| nchar                                                | string                                           |
| char                                                 | string                                           |
| _char                                                | pq.StringArray                                   |
| character                                            | string                                           |
| varchar                                              | string                                           |
| _varchar                                             | pq.StringArray                                   |
| 바이너리                                               | string                                           |
| bytea                                                | string                                           |
| longvarbinary                                        | string                                           |
| varbinary                                            | string                                           |
| tinytext                                             | string                                           |
| text                                                 | string                                           |
| _text                                                | pq.StringArray                                   |
| mediumtext                                           | string                                           |
| longtext                                             | string                                           |
| enum                                                 | string                                           |
| set                                                  | string                                           |
| json                                                 | string                                           |
| jsonb                                                | string                                           |
| blob                                                 | string                                           |
| longblob                                             | string                                           |
| mediumblob                                           | string                                           |
| tinyblob                                             | string                                           |
| ltree                                                | []byte                                           |

### 타입 mapping 커스터마이징


예제 1. Modify decimal 로 decimal. Decimal 타입

1. Initialize 설정 에서 projects that need 로 생성 모델
```bash
$ goctl config init
goctl.yaml generated in ~/workspace/go-zero/tools/goctl/goctl.yaml
```
2. Modify 타입 mapping relationship

grey shading은 custom mapping type입니다.

```yaml {10-13}
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
      null_type: decimal.NullDecimal
      pkg: github.com/shopspring/decimal
      type: decimal.Decimal
    ...
```

### 추가 타입 mappings 아님 supported 통해 goctl built-in

We have pg 에서 table 사용하여 데이터 타입 `inet`.

```sql
-- auto-generated definition
create table student
(
    id          integer                               not null
        constraint student_pk
            primary key,
    name        varchar default ''::character varying not null,
    age         integer default 0                     not null,
    description integer                               not null,
    ip_address  inet    default '0.0.0.0'::inet       not null
);

alter table student
    owner to postgres;

```


```bash
$ goctl model pg datasource --url="postgres:// 예시입니다
Error: unsupported database type: inet
```


1. 체크 경우 goctl 버전 meets conditions

```bash
$ goctl env
GOCTL_OS=darwin
GOCTL_ARCH=arm64
GOCTL_HOME=/Users/sh00414ml/.goctl
GOCTL_DEBUG=False
GOCTL_CACHE=/Users/sh00414ml/.goctl/cache
GOCTL_EXPERIMENTAL=on # If, GOCTL_EXPERIMENTAL 예시입니다
GOCTL_VERSION=1.6.5 # goctl version
PROTOC_VERSION=3.19.4
PROTOC_GEN_GO_VERSION=v1.28.0
PROTO_GEN_GO_GRPC_VERSION=1.2.0
```

2. Initialize goctl 설정 에서 target 프로젝트

```bash
$ goctl config
goctl.yaml generated in ~/demo/goctl-config/goctl.yaml # 예시입니다
```

3. Modify goctl.yaml


```yaml {8-10}
model:
  types_map:
    bigint:
      null_type: sql.NullInt64
      type: int64
      unsigned_type: uint64
    ...
    inet:
      null_type: sql.NullString
      type: string
```

4. 생성 모델 code again

```bash
goctl model pg datasource --url="postgres:// 예시입니다
Done.
```
