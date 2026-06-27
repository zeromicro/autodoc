---
title: goctl 템플릿
description: go-zero의 goctl 템플릿에 대해 설명합니다.
sidebar:
  order: 11

---


## 개요


## goctl 템플릿 directive

```bash
$ goctl template --help
Template operation

Usage:
  goctl template [command]

Available 명령s:
  clean       Clean the all cache templates
  init        Initialize the all templates(force update)
  revert      Revert the target template to the latest
  update      Update template of the target category to the latest

Flags:
  -h, --help   help for template


Use "goctl template [command] --help" for more information about a command.
```

### goctl 템플릿 clean directive

goctl 템플릿 clean은 사용되어 delete persistent 로컬 템플릿 files입니다.

```bash
$ goctl template clean --help
Clean the all cache templates

Usage:
  goctl template clean [flags]

Flags:
  -h, --help          help for clean
      --home string   The goctl home path of the template
```

### goctl 템플릿 init directive


```bash
$ goctl template init --help
Initialize the all templates(force update)

Usage:
  goctl template init [flags]

Flags:
  -h, --help          help for init
      --home string   The goctl home path of the template
```

### goctl 템플릿 revert directive

goctl 템플릿 revert은 사용되어 roll back specified 템플릿 파일 에서 category입니다.

```bash
$ goctl template revert --help
Revert the target template to the latest

Usage:
  goctl template revert [flags]

Flags:
  -c, --category string   The category of template, enum [api,rpc,model,docker,kube]
  -h, --help              help for revert
      --home string       The goctl home path of the template
  -n, --name string       The target file name of template
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| category                                             | string                                              | YES                                            | Empty string                                       | 模板分类，api\|rpc\|모델\|Docker\|kube                     |
| home                                                 | string                                              | YES                                            | `${HOME}/.goctl`                                   | 파일 location stored 에서 템플릿                           |
| name                                                 | string                                              | YES                                            | Empty string                                       | 템플릿 파일 Name                                         |

### goctl 템플릿 업데이트 instruction

goctl 템플릿 update은 사용되어 roll back 모든 템플릿 파일 under category입니다.

```bash
$ goctl template update --help
Update template of the target category to the latest

Usage:
  goctl template update [flags]

Flags:
  -c, --category string   The category of template, enum [api,rpc,model,docker,kube]
  -h, --help              help for update
      --home string       The goctl home path of the template
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명 |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| category                                             | string                                              | YES                                            | Empty string                                       | 템플릿 Category,api\|rpc\|모델\|Docker\|kube        |
| home                                                 | string                                              | YES                                            | `${HOME}/.goctl`                                   | 파일 location stored 에서 템플릿                           |
