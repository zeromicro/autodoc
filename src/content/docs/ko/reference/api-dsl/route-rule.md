---
title: API 라우트 규칙
description: go-zero의 API 라우트 규칙에 대해 설명합니다.
sidebar:
  order: 2

---


## 개요


## 라우트 규칙

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

1. 라우트 must 시작 사용하여 `/`
1. 라우트 node must be separated 통해 `/`

라우트 예제：

```go {29,33,37,41,45,49,53}
syntax = "v1"

type DemoPath3Req {
    Id int64 `path:"id"`
}

type DemoPath4Req {
    Id   int64  `path:"id"`
    Name string `path:"name"`
}

type DemoPath5Req {
    Id   int64  `path:"id"`
    Name string `path:"name"`
    Age  int    `path:"age"`
}

type DemoReq {}

type DemoResp {}

service Demo {
    // 예시입니다
    @handler demoPath1
    get /foo (DemoReq) returns (DemoResp)

    // 예시입니다
    @handler demoPath2
    get /foo/bar (DemoReq) returns (DemoResp)

    // 예시입니다
    @handler demoPath3
    get /foo/bar/:id (DemoPath3Req) returns (DemoResp)

    // 예시입니다
    @handler demoPath4
    get /foo/bar/:id/:name (DemoPath4Req) returns (DemoResp)

    // 예시입니다
    @handler demoPath5
    get /foo/bar/:id/:name/:age (DemoPath5Req) returns (DemoResp)

    // 예시입니다
    @handler demoPath6
    get /foo/bar/baz-qux (DemoReq) returns (DemoResp)

    // 예시입니다
    @handler demoPath7
    get /foo/bar_baz/123 (DemoReq) returns (DemoResp)
}


```
