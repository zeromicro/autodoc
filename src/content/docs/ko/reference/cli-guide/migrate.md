---
title: goctl 마이그레이션
description: go-zero의 goctl 마이그레이션에 대해 설명합니다.
sidebar:
  order: 15

---


## 개요

goctl migrates 로 go-zero 에서 `tal-tech` 로 `zeroicro`.

## goctl 마이그레이션 directive

```bash
goctl migrate --help
Migrate is a transition command to help users migrate their projects from tal-tech to zeromicro version

Usage:
  goctl migrate [flags]

Flags:
  -h, --help             help for migrate
  -v, --verbose          Verbose enables extra logging
      --version string   The target release version of github.com/zeromicro/go-zero to migrate (default "v1.3.0")
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                      |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------- |
| verbose                                              | boolean                                             | 없음                                             | false                                              | Whether 로 출력 로그                                                           |
| 버전                                              | string                                              | 없음                                             | `v1.3.0`                                           | 마이그레이션 에서 `tal-tech` 로 `zeroicro` 후에 organization, 기본값 is `v1.3.0` |

참고: [go-zero 릴리스](https://github.com/zeromicro/go-zero/releases) 위한 전체 list 의 버전 organized 통해 zeromicro.
