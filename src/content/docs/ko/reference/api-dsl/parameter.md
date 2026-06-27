---
title: API 매개변수
description: go-zero의 API 매개변수에 대해 설명합니다.
sidebar:
  order: 6

---


## 개요


## 인자 수신 규칙


| <img width={100} /> Receive rules | 참고                                                                                                                                                | <img width={150} /> Scope 의 entry | 샘플                          |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------- |
| json                                              | json serialization                                                                                                                                  | 요청 본문&응답                              | \`json:"foo"\`              |
| 경로                                              | 라우트 매개변수                                                                                                                                    | 요청 본문                                       | \`path:"id"\`               |
| form                                              |해당 항목의 동작과 사용법을 설명합니다. | 요청 본문                                       | \`form:"name"\`             |
| 헤더                                            | HTTP Request Receipt Identifier                                                                                                                     | 요청 본문                                       | \`header:"Content-Length"\` |

:::note Warm reminder

```go
type Foo {
    Name string `json:"name" form:"name"`
}
```

:::

## 매개변수 verification rules


| <img width={100} /> Receive rules | 참고                                                                                                                  | 샘플                            |
|----------------------------------| --------------------------------------------------------------------------------------------------------------------- |-----------------------------------|
| optional                         | 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.                                          | \`json:"foo,optional"\`           |
| 옵션                          | Current 매개변수 can 만 receive enumeration value                                                               | \`json:"gender,options=foo\|bar"\` |
| 기본값                          | Current Argument 기본값                                                                                              | \`json:"gender,default=male"\`    |
| range                            |해당 항목의 동작과 사용법을 설명합니다. | \`json:"age,range=[0:120]"\`      |

:::note Range expression rules

1. 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.
:::
