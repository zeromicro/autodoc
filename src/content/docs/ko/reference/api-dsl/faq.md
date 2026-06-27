---
title: API FAQ
description: go-zero의 API FAQ에 대해 설명합니다.
sidebar:
  order: 12

---


## 1. 어떻게 experience 새로운 API 기능?


```bash
$ goctl env -w GOCTL_EXPERIMENTAL=on
```

새 기능 are supported starting 에서 버전 1.5.1, including:

1. 데이터 타입 지원합니다 array 타입
1. 지원 Tag Ignore
1. Pure numbers are supported 통해 라우트, e.g. `/abc/123/`
1. api resolver migrated 에서 antlr4 로 goparser

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

1. 문법 헤더 is 필수

위한 데이터 타입 usage 예제, see [타입 선언s • 예제](./type.md#examples).


```go {1,6}
service foo {
    @handler fooPing
    get /foo/ping
}

service bar {
    @handler barPing
    get /bar/ping
}
```


```go {1,6}
service foo {
    @handler fooPing
    get /foo/ping
}

service foo {
    @handler barPing
    get /bar/ping
}
```

## 3. goctl api does 아님 지원 `any` 타입

Generic과 weak types은 아님 supported 에서 api syntax입니다.
