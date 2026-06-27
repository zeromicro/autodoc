---
title: goctl RPC
description: go-zero의 goctl RPC에 대해 설명합니다.
sidebar:
  order: 5

---


## 개요


## goctl rpc directive

```bash
$ goctl rpc --help
Generate rpc code

Usage:
  goctl rpc [flags]
  goctl rpc [command]

Available 명령s:
  new         Generate rpc demo service
  protoc      Generate grpc code
  template    Generate proto template

Flags:
      --branch string   The branch of the remote repo, it does work with --remote
  -h, --help            help for rpc
      --home string     The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --o string        Output a sample proto file
      --remote string   The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                            The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure


Use "goctl rpc [command] --help" for more information about a command.
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| branch                                               | string                                              | 없음                                             | Empty string                                       | 템플릿 repository branch, 사용하여 --remote usage            |
| home                                                 | string                                              | 없음                                             | `~/.goctl`                                         | 템플릿 repository 로컬 경로 higher than --remote        |
| o                                                    | string                                              | 없음                                             | Empty string                                       | 출력 api 파일                                            |
| 원격                                               | string                                              | 없음                                             | Empty string                                       | 템플릿 repository 원격 경로                            |

예제：생성합니다 proto 파일

```bash
$ goctl rpc --o greet.proto
```

### goctl rpc 새로운


```bash
$ goctl rpc new --help
Generate rpc demo service

Usage:
  goctl rpc new [flags]

Flags:
      --branch string   The branch of the remote repo, it does work with --remote
  -h, --help            help for new
      --home string     The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --idea            Whether the command execution environment is from idea plugin.
      --remote string   The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                            The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure
      --style string    The file naming format, see [https://github.com/zeromicro/go-zero/tree/master/tools/goctl/config/readme.md] (default "gozero")
  -v, --verbose         Enable log output
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| branch                                               | string                                              | 없음                                             | Empty string                                       | 템플릿 repository branch, 사용하여 --remote usage            |
| home                                                 | string                                              | 없음                                             | `~/.goctl`                                         | 템플릿 repository 로컬 경로 higher than --remote        |
| idea                                                 | bool                                                | 없음                                             | false                                              | 사용 this 필드 만 위한 플러그인, please ignore this 필드  |
| 원격                                               | string                                              | 없음                                             | Empty string                                       | 템플릿 repository 원격 경로                            |
| 스타일                                                | string                                              | 없음                                             | gozero                                             | Filename 스타일, see [파일 스타일](./style.md)         |

### goctl rpc protoc

생성 rpc 서비스 based 에서 protobefer 파일.

```bash
$ goctl rpc protoc --help
Generate grpc code

Usage:
  goctl rpc protoc [flags]

Examples:
goctl rpc protoc xx.proto --go_out=./pb --go-grpc_out=./pb --zrpc_out=.

Flags:
      --branch string     The branch of the remote repo, it does work with --remote
  -h, --help              help for protoc
      --home string       The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
  -m, --multiple          Generated in multiple rpc service mode
      --remote string     The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                            The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure
      --style string      The file naming format, see [https://github.com/zeromicro/go-zero/tree/master/tools/goctl/config/readme.md] (default "gozero")
  -v, --verbose           Enable log output
      --zrpc_out string   The zrpc output directory
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| branch                                               | string                                              | 없음                                             | Empty string                                       | 템플릿 repository branch, 사용하여 --remote usage            |
| home                                                 | string                                              | 없음                                             | `~/.goctl`                                         | 템플릿 repository 로컬 경로 higher than --remote        |
| multiple                                             | bool                                                | 없음                                             | false                                              | Whether 로 생성 multiple rpc 서비스                  |
| 원격                                               | string                                              | 없음                                             | Empty string                                       | 템플릿 repository 원격 경로                            |
| 스타일                                                | string                                              | 없음                                             | gozero                                             | Filename 스타일, see [파일 스타일](./style.md)         |                                             | string                                              | 없음                                             | Empty string                                       | 출력 디렉터리                                           |


예제:

```bash
# 예시입니다
$ goctl rpc protoc greet.proto --go_out=./pb --go-grpc_out=./pb --zrpc_out=.
# 예시입니다
$ goctl rpc protoc greet.proto --go_out=./pb --go-grpc_out=./pb --zrpc_out=. -m
```

:::tip
:::

:::tip

:::

:::caution

2. 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.
:::

### goctl rpc 템플릿


:::caution
:::

```bash
$ goctl rpc template --help
Generate proto template

Usage:
  goctl rpc template [flags]

Flags:
      --branch string   The branch of the remote repo, it does work with --remote
  -h, --help            help for template
      --home string     The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --o string        Output a sample proto file
      --remote string   The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                            The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| branch                                               | string                                              | 없음                                             | Empty string                                       | 템플릿 repository branch, 사용하여 --remote usage            |
| home                                                 | string                                              | 없음                                             | `~/.goctl`                                         | 템플릿 repository 로컬 경로 higher than --remote        |
| o                                                    | string                                              | 없음                                             | Empty string                                       | 출력 파일 경로                                           |
| 원격                                               | string                                              | 없음                                             | Empty string                                       | 템플릿 repository 원격 경로                            |

예제:

```bash
$ goctl rpc template -o greet.proto
```

## 참조

- [파일 스타일](https://developers.google.com/protocol-buffers/docs/reference/go-generated#invocation)
- [서비스 group](../../proto-dsl/services-group.md)
- [Go 생성된 코드 가이드](./style.md)
- [Protocol Buffers 문서화](../../proto-dsl/services-group.md)
