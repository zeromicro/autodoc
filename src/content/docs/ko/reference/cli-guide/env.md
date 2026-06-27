---
title: goctl 환경
description: go-zero의 goctl 환경에 대해 설명합니다.
sidebar:
  order: 9

---

## 개요


## goctl env directive

```bash
$ goctl env --help
Check or edit goctl environment

Usage:
  goctl env [flags]
  goctl env [command]

Available 명령s:
  check       Detect goctl env and dependency tools
  install     Goctl env installation

Flags:
  -f, --force           Silent installation of non-existent dependencies
  -h, --help            help for env
  -v, --verbose         Enable log output
  -w, --write strings   Edit goctl environment

Use "goctl env [command] --help" for more information about a command.
```

### goctl env


```bash
$ goctl env
GOCTL_OS=darwin
GOCTL_ARCH=arm64
GOCTL_HOME=/Users/sh00414ml/.goctl
GOCTL_DEBUG=False
GOCTL_CACHE=/Users/sh00414ml/.goctl/cache
GOCTL_EXPERIMENTAL=off
GOCTL_VERSION=1.6.5
PROTOC_VERSION=3.19.4
PROTOC_GEN_GO_VERSION=v1.28.0
PROTO_GEN_GO_GRPC_VERSION=1.2.0
```

| <img width={100}/> 필드 | <img width={200}/> 기본값 Value | <img width={800}/> 설명 |
| -- | --- | --- |
| GOCTL_OS | Empty string | Operating 시스템 |
| GOCTL_ARCH | Empty string | 시스템 아키텍처 |
| GOCTL_HOME | Empty string | goctl 설정 디렉터리 |
| GOCTL_DEBUG | Empty string |해당 항목의 동작과 사용법을 설명합니다. |
| GOCTL_CACHE | Empty string | 캐시 디렉터리 |
| GOCTL_EXPERIMENTAL | off | Whether 로 활성화 experimental 함수, enumeration values [에서,off] |
| GOCTL_VERSION | Empty string | goctl 버전 |
| PROTOC_VERSION | Empty string | protoc 버전 |
| PROTOC_GEN_GO_VERSION | Empty string | protoc_gen_go 플러그인 버전 |
| PROTO_GEN_GO_GRPC_VERSION | Empty string | protoc_gen_go_grpc 플러그인 버전 |

### goctl env 체크 directive


```bash
$ goctl env check --help
Detect goctl env and dependency tools

Usage:
  goctl env check [flags]

Flags:
  -h, --help      help for check
  -i, --install   Install dependencies if not found

Global Flags:
  -f, --force     Silent installation of non-existent dependencies
  -v, --verbose   Enable log output
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                                                                  |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| i                                                    | boolean                                             | 없음                                             | false                                              | 설치 의존성                                                                                                        |
| force                                                | boolean                                             | 없음                                             | false                                              |해당 항목의 동작과 사용법을 설명합니다. |
| verbose                                              | boolean                                             | 없음                                             | false                                              | Export execution 로그                                                                                                        |

**예제**：

예제 1： detect goctl 의존성

**goctl 环境依赖已经安装**
```bash
$ goctl env check --verbose
[goctl-env]: preparing to check env

[goctl-env]: looking up "protoc"
[goctl-env]: "protoc" is installed

[goctl-env]: looking up "protoc-gen-go"
[goctl-env]: "protoc-gen-go" is installed

[goctl-env]: looking up "protoc-gen-go-grpc"
[goctl-env]: "protoc-gen-go-grpc" is installed

[goctl-env]: congratulations! your goctl environment is ready!
```

**goctl 环境依赖未安装**
```bash
$ goctl env check --verbose
[goctl-env]: preparing to check env

[goctl-env]: looking up "protoc"
[goctl-env]: "protoc" is not found in PATH

[goctl-env]: looking up "protoc-gen-go"
[goctl-env]: "protoc-gen-go" is not found in PATH

[goctl-env]: looking up "protoc-gen-go-grpc"
[goctl-env]: "protoc-gen-go-grpc" is not found in PATH

[goctl-env]: check env finish, some dependencies is not found in PATH, you can execute
command 'goctl env check --install' to install it, for details, please execute command
'goctl env check --help'
```

예제 2： detect goctl 의존성과 설치 missing 의존성

**不静默安装**
```bash
$ goctl env check --verbose --install
[goctl-env]: preparing to check env

[goctl-env]: looking up "protoc"
[goctl-env]: "protoc" is not found in PATH
[goctl-env]: do you want to install "protoc" [y: YES, n: No]
y
[goctl-env]: preparing to install "protoc"
[goctl-env]: "protoc" is already installed in "/Users/keson/go/bin/protoc"

[goctl-env]: looking up "protoc-gen-go"
[goctl-env]: "protoc-gen-go" is not found in PATH
[goctl-env]: do you want to install "protoc-gen-go" [y: YES, n: No]
y
[goctl-env]: preparing to install "protoc-gen-go"
"protoc-gen-go" installed from cache
[goctl-env]: "protoc-gen-go" is already installed in "/Users/keson/go/bin/protoc-gen-go"

[goctl-env]: looking up "protoc-gen-go-grpc"
[goctl-env]: "protoc-gen-go-grpc" is not found in PATH
[goctl-env]: do you want to install "protoc-gen-go-grpc" [y: YES, n: No]
y
[goctl-env]: preparing to install "protoc-gen-go-grpc"
"protoc-gen-go-grpc" installed from cache
[goctl-env]: "protoc-gen-go-grpc" is already installed in "/Users/keson/go/bin/protoc-gen-go-grpc"

[goctl-env]: congratulations! your goctl environment is ready!
```

**静默安装**
```bash
$ goctl env check --verbose --install --force
[goctl-env]: preparing to check env

[goctl-env]: looking up "protoc"
[goctl-env]: "protoc" is not found in PATH
[goctl-env]: preparing to install "protoc"
"protoc" installed from cache
[goctl-env]: "protoc" is already installed in "/Users/keson/go/bin/protoc"

[goctl-env]: looking up "protoc-gen-go"
[goctl-env]: "protoc-gen-go" is not found in PATH
[goctl-env]: preparing to install "protoc-gen-go"
"protoc-gen-go" installed from cache
[goctl-env]: "protoc-gen-go" is already installed in "/Users/keson/go/bin/protoc-gen-go"

[goctl-env]: looking up "protoc-gen-go-grpc"
[goctl-env]: "protoc-gen-go-grpc" is not found in PATH
[goctl-env]: preparing to install "protoc-gen-go-grpc"
"protoc-gen-go-grpc" installed from cache
[goctl-env]: "protoc-gen-go-grpc" is already installed in "/Users/keson/go/bin/protoc-gen-go-grpc"

[goctl-env]: congratulations! your goctl environment is ready!
```

### goctl env 설치 directive


```bash
$ goctl env install --help
Goctl env installation

Usage:
  goctl env install [flags]

Flags:
  -h, --help   help for install

Global Flags:
  -f, --force     Silent installation of non-existent dependencies
  -v, --verbose   Enable log output
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                                                                  |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| force                                                | boolean                                             | 없음                                             | false                                              |해당 항목의 동작과 사용법을 설명합니다. |
| verbose                                              | boolean                                             | 없음                                             | false                                              | Export execution 로그                                                                                                        |
