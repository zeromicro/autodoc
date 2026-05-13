---
title: 설정 개요
description: go-zero의 설정 개요에 대해 설명합니다.
sidebar:
  order: 2

---

## 개요


## 어떻게 사용

다음 패키지를 사용합니다: 패키지 [github.com/zeromicro/go-zero/core/conf](https://github.com/zeromicro/go-zero/tree/master/core/conf) conf 로 부하 it.

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

 두 번째 단계 goes 에서 로 prepare 설정 파일 based 에서 설정.

세 번째 party loading 설정 via conf.MustLoad

특정 Usage:

**main.go**
```go
package main

import (
    "flag"

    "github.com/zeromicro/go-zero/core/conf"
)

type Config struct {
    Host string `json:",default=0.0.0.0"`
    Port int
}

var f = flag.String("f", "config.yaml", "config file")

func main() {
    flag.Parse()
    var c Config
    conf.MustLoad(*f, &c)
    println(c.Host)
}
```

**설정.yaml**
```yaml
Host: 127.0.0.1
Port: 8888
```


이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

```go
func Load(file string, v interface{}, opts ...Option) error
```

## Other formatting profiles

현재 지원하는 설정 format below：

- json
- yaml | yml
- toml
- json5 (since v1.10.1)


또한 로드하는 방법을 제공합니다 바이너리 데이터 에서 conf 패키지：

```go

func LoadFromJsonBytes(content []byte, v interface{}) error

func LoadFromTomlBytes(content []byte, v interface{}) error

func LoadFromYamlBytes(content []byte, v interface{}) error

func LoadFromJson5Bytes(content []byte, v interface{}) error
```

간단한 예제：

```go
text := []byte(`a: foo
B: bar`)

var val struct {
    A string
    B string
}
_ = LoadFromYamlBytes(text, &val)
```

:::note
이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.
:::

## Case insensitive

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

```yaml
Host: "127.0.0.1"

host: "127.0.0.1"
```

## 환경 Variables


### 1. **conf.UseEnv()**

```go

var c struct {
    Name string
}

conf.MustLoad("config.yaml", &c, conf.UseEnv())

```

```config.yaml
Name: ${SERVER_NAME}
```


### 2. env Tag


```go
var c struct {
    Name string `json:",env=SERVER_NAME"`
}

conf.MustLoad("config.yaml", &c)
```


:::note
:::

## tag checksum rule


```go
type Config struct {
    Name string // No 예시입니다
    Port int64 `json:",default=8080"` // If 예시입니다
    Path string `json:",optional"`
}
```

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.


| Receive rules | 참고                                                                                                                  | 샘플                          |
| ------------- | --------------------------------------------------------------------------------------------------------------------- |---------------------------------|
| optional      | 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.                                          | \`json:"foo,optional"\`         |
| 옵션       | Current 매개변수 can 만 receive enumeration value                                                               | **Protestant 1**：portrait line\ |split,\`json:`gender,옵션=foo\|해당 항목의 동작과 사용법을 설명합니다. |
| 기본값       | Current Argument 기본값                                                                                              | \`json:"gender,default=male"\`  |
| range         |해당 항목의 동작과 사용법을 설명합니다. | \`json:"age,range=[0:120]"\`    |
| env           | Current 매개변수 are taken 에서 environmental variables                                                             | \`json:"mode,env=MODE"\`        |

:::note Range expression rules

1. 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.
:::

More 참조 [unmarshaler_test.go](https://github.com/zeromicro/go-zero/releases/tag/v1.4.3)

## inherit 配置继承

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

```goc
type Config struct {
    Etcd     discov.EtcdConf
    UserRpc  zrpc.RpcClientConf
    PortRpc  zrpc.RpcClientConf
    OtherRpc zrpc.RpcClientConf
}

const str = `
Etcd:
  Key: rpcServer"
  Hosts:
    - "127.0.0.1:6379"
    - "127.0.0.1:6377"
    - "127.0.0.1:6376"

UserRpc:
  Etcd:
    Key: UserRpc
    Hosts:
    - "127.0.0.1:6379"
    - "127.0.0.1:6377"
    - "127.0.0.1:6376"

PortRpc:
  Etcd:
    Key: PortRpc
    Hosts:
    - "127.0.0.1:6379"
    - "127.0.0.1:6377"
    - "127.0.0.1:6376"

OtherRpc:
  Etcd:
    Key: OtherRpc
    Hosts:
    - "127.0.0.1:6379"
    - "127.0.0.1:6377"
    - "127.0.0.1:6376"
`

```

We must 추가 Hosts 로 모든 Etcd과 other base configurations.


```go
// A, RpcClientConf 예시입니다
    RpcClientConf struct {
        Etcd          discov.EtcdConf `json:",optional,inherit"`
        ....
    }
```


```go
const str = `
Etcd:
  Key: rpcServer"
  Hosts:
    - "127.0.0.1:6379"
    - "127.0.0.1:6377"
    - "127.0.0.1:6376"

UserRpc:
  Etcd:
    Key: UserRpc

PortRpc:
  Etcd:
    Key: PortRpc

OtherRpc:
  Etcd:
    Key: OtherRpc
`
```

## JSON5 설정 (since v1.10.1)


**Key differences 에서 plain JSON:**

| Feature | JSON | JSON5 |
|---------|------|-------|
| 주석 | ❌ | ✅ (`//`과 `/* */`) |
| Trailing commas | ❌ | ✅ |
| Unquoted keys | ❌ | ✅ |
| Single-quoted strings | ❌ | ✅ |

### 예제 설정.json5

```json5
{
  // Service 예시입니다
  Host: "0.0.0.0",
  Port: 8080,   // 예시입니다
  Name: "my-service",
}
```

```go
var c Config
conf.MustLoad("config.json5", &c)
```

### Inline loading

```go
data := []byte(`{
  // comment
  Host: "localhost",
  Port: 8080,
}`)

var c Config
conf.LoadFromJson5Bytes(data, &c)
```

:::note
:::
