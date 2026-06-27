---
title: goctl API
description: go-zero의 goctl API에 대해 설명합니다.
sidebar:
  order: 4

---


## 개요


## goctl api directive

```bash
$ goctl api --help
Generate api related files

Usage:
  goctl api [flags]
  goctl api [command]

Available 명령s:
  dart        Generate dart files for provided api in api file
  doc         Generate doc files
  format      Format api files
  go          Generate go files for provided api in api file
  kt          Generate kotlin code for provided api file
  new         Fast create api service
  plugin      Custom file generator
  swagger     Generate swagger file from api
  ts          Generate ts files for provided api in api file
  validate    Validate api file

Flags:
      --branch string   The branch of the remote repo, it does work with --remote
  -h, --help            help for api
      --home string     The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --o string        Output a sample api file
      --remote string   The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                        The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure


Use "goctl api [command] --help" for more information about a command.
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| branch                                               | string                                              | 없음                                             | Empty string                                       | 템플릿 repository branch, 사용하여 --remote usage            |
| home                                                 | string                                              | 없음                                             | `~/.goctl`                                         | 템플릿 repository 로컬 경로 higher than --remote        |
| o                                                    | string                                              | 없음                                             | Empty string                                       | 출력 api 파일                                            |
| 원격                                               | string                                              | 없음                                             | Empty string                                       | 템플릿 repository 원격 경로                            |

### dart

생성 date code 에서 api 파일.

```bash
$ goctl api dart --help
Generate dart files for provided api in api file

Usage:
  goctl api dart [flags]

Flags:
      --api string        The api file
      --dir string        The target dir
  -h, --help              help for dart
      --hostname string   hostname of the server
      --legacy            Legacy generator for flutter v1
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| api                                                  | string                                              | YES                                            | Empty string                                       | api 파일                                                   |
| dir                                                  | string                                              | YES                                            | Empty string                                       | 생성 Code 출력 디렉터리                             |
| hostname                                             | string                                              | 없음                                             | `go-zero.dev`                                      | 호스트 值                                                     |
| legacy                                               | boolean                                             | 없음                                             | `false`                                            | Whether 또는 아님 older 버전                              |

### doc

생성 markdown 문서화 based 에서 api 파일.

```bash
$ goctl api doc --help
Generate doc files

Usage:
  goctl api doc [flags]

Flags:
      --dir string   The target dir
  -h, --help         help for doc
      --o string     The output markdown directory
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={200} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| dir                                                  | string                                              | YES                                            | Empty string                                       | api 파일 디렉터리                                         |
| o                                                    | string                                              | 없음                                             | Current 작동 dir                                   | Document 출력 디렉터리                                  |

### format

Api 파일 에서 recursive formatting 디렉터리.

```bash
$ goctl api format --help
Format api files

Usage:
  goctl api format [flags]

Flags:
      --declare      Use to skip check api types already declare
      --dir string   The format target dir
  -h, --help         help for format
      --iu           Ignore update
      --stdin        Use stdin to input api doc content, press "ctrl + d" to send EOF
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| declare                                              | boolean                                             | 없음                                             | `false`                                            | Whether 로 detect 컨텍스트                                  |
| dir                                                  | string                                              | YES                                            | Empty string                                       | api 파일 디렉터리                                         |
| iu                                                   | -                                                   | -                                              | -                                                  | Unused 필드 pending removal                              |
| stdin                                                | boolean                                             | 없음                                             | `false`                                            | Format api content 위한 terminal 입력                      |

### go

생성 Go HTTP code 에서 api 파일.

```bash
$ goctl api go --help
Generate go files for provided api in api file

Usage:
  goctl api go [flags]

Flags:
      --api string      The api file
      --branch string   The branch of the remote repo, it does work with --remote
      --dir string      The target dir
  -h, --help            help for go
      --home string     The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --remote string   The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                        The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure
      --style string    The file naming format, see [https://github.com/zeromicro/go-zero/blob/master/tools/goctl/config/readme.md] (default "gozero")
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                                                        |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| api                                                  | string                                              | YES                                            | Empty string                                       | api 파일                                                                                                          |
| branch                                               | string                                              | 없음                                             | Empty string                                       | 원격 템플릿 name is 사용됨 만 경우 `remote` has value                                                           |
| dir                                                  | string                                              | 없음                                             | Current 작동 디렉터리                          | 생성 Code 출력 디렉터리                                                                                    |
| home                                                 | string                                              | 없음                                             | `${HOME}/.goctl`                                   | 로컬 템플릿 파일 디렉터리                                                                                     |
| 원격                                               | string                                              | 없음                                             | Empty string                                       |해당 항목의 동작과 사용법을 설명합니다. |
| 스타일                                                | string                                              | 없음                                             | `gozero`                                           | Named 스타일 symbols 위한 출력 파일과 디렉터리, see [파일 스타일](./style.md)                                |

### 새로운


```bash
$ goctl api new --help
Fast create api service

Usage:
  goctl api new [flags]

Examples:
goctl api new [options] service-name

Flags:
      --branch string   The branch of the remote repo, it does work with --remote
  -h, --help            help for new
      --home string     The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --remote string   The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                            The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure
      --style string    The file naming format, see [https://github.com/zeromicro/go-zero/blob/master/tools/goctl/config/readme.md] (default "gozero")
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                                                        |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| branch                                               | string                                              | 없음                                             | Empty string                                       | 원격 템플릿 name is 사용됨 만 경우 `remote` has value                                                           |
| home                                                 | string                                              | 없음                                             | `${HOME}/.goctl`                                   | 로컬 템플릿 파일 디렉터리                                                                                     |
| 원격                                               | string                                              | 없음                                             | Empty string                                       |해당 항목의 동작과 사용법을 설명합니다. |
| 스타일                                                | string                                              | 없음                                             | `gozero`                                           | Named 스타일 symbols 위한 출력 파일과 디렉터리, see [파일 스타일](./style.md)                                |

:::note reminder

```bash
$ goctl api new demo
```

:::

### 플러그인


```bash
$ goctl api plugin --help
Custom file generator

Usage:
  goctl api plugin [flags]

Flags:
      --api string      The api file
      --dir string      The target dir
  -h, --help            help for plugin
  -p, --plugin string   The plugin file
      --style string    The file naming format, see [https://github.com/zeromicro/go-zero/tree/master/tools/goctl/config/readme.md]
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                         |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| api                                                  | string                                              | YES                                            | Empty string                                       | api 파일                                                                           |
| dir                                                  | string                                              | 없음                                             | Current 작동 디렉터리                          | api 파일                                                                           |
| 플러그인                                               | string                                              | YES                                            | Empty string                                       | 경로 로 플러그인 executable, 지원 로컬과 HTML 파일                            |
| 스타일                                                | string                                              | 없음                                             | `gozero`                                           | Named 스타일 symbols 위한 출력 파일과 디렉터리, see [파일 스타일](./style.md) |

플러그인 resource 참조: [goctl 플러그인 resource](../../goctl-plugins.md)


### swagger


:::note Tips
이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.
1. 버전 의 goctl은 greater than 1.8.2입니다.
:::

```bash
goctl api swagger -h
Generate swagger file from api

Usage:
  goctl api swagger [flags]

Flags:
      --api string   The api file
      --dir string   The target dir
  -h, --help         help for swagger
      --yaml         Generate swagger yaml file, default to json
```

| <img width={100}/> 매개변수 필드 | <img width={150}/> 매개변수 타입 | <img width={200}/> 필수? | <img width={200}/> 기본값 value | <img width={800}/> 매개변수 설명 |
|-------------------------|-------------------------|------------------------------|----------------------------------|------------------------------------------|
| api                     | string                  | YES                          | empty string                     | api filename                             |
| dir                     | string                  | 없음                           | 작동 디렉터리                   | 출력 dir                               |
| yaml                    | bool                    | 없음                           | false                            |format to yaml file


### ts

생성 TypeScript code 에서 api 파일.

```bash
$ goctl api ts --help
Generate ts files for provided api in api file

Usage:
  goctl api ts [flags]

Flags:
      --api string      The api file
      --caller string   The web api caller
      --dir string      The target dir
  -h, --help            help for ts
      --unwrap          Unwrap the webapi caller for import
      --webapi string   The web api file path
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                         |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| api                                                  | string                                              | YES                                            | Empty string                                       | api 파일                                                                           |
| dir                                                  | string                                              | 없음                                             | Current 작동 디렉터리                          | api 파일                                                                           |
| caller                                               | string                                              | 없음                                             | `webapi`                                           | web caller，                                                                        |
| 플러그인                                               | string                                              | YES                                            | Empty string                                       | 경로 로 플러그인 executable, 지원 로컬과 HTML 파일                            |
| 스타일                                                | string                                              | 없음                                             | `gozero`                                           | Named 스타일 symbols 위한 출력 파일과 디렉터리, see [파일 스타일](./swagger.md) |

### 검증

확인 that api 파일 meet specifications.

```bash
goctl api validate --help
Validate api file

Usage:
  goctl api validate [flags]

Flags:
      --api string   Validate target api file
  -h, --help         help for validate
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| api                                                  | string                                              | YES                                            | Empty string                                       | api 파일                                                   |
