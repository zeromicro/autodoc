---
title: 요청 본문
description: go-zero HTTP handler에서 요청 본문을 parsing하는 방법입니다.
sidebar:
  order: 5

---

## 개요

go-zero에서는 `http.Request`에서 요청 매개변수를 가져올 수 있습니다. `Body`는 `application/json` 형식의 요청 매개변수를 받고, `Form`은 `application/x-www-form-urlencoded` 형식의 요청 매개변수를 받습니다. 이 밖에도 go-zero는 path parameter와 request header parameter를 가져오는 기능을 지원하며, 이 값들은 모두 `httpx.Parse` 메서드를 통해 구조체로 parsing됩니다.

## 매개변수 사용법

### Form 요청 매개변수

form 요청 매개변수는 `form` tag로 매개변수 이름을 정의합니다. `application/x-www-form-urlencoded` Content-Type과 GET method의 query argument를 지원합니다. 구조체 tag에 `form` keyword를 추가하며, tag는 k-v 구조입니다. key는 고정값 `form`이고 value는 query key입니다.

```go
type Request struct {
    Name    string  `form:"name"` // required
    Age     int     `form:"age,optional"` // optional
}


var req Request
err := httpx.Parse(r, &req)
```

### JSON 요청 매개변수

JSON 요청 매개변수는 `Content-Type`이 `application/json`인 POST 요청에서 전달된 값을 받습니다. 구조체 tag에 `json` keyword를 추가하며, tag는 k-v 구조입니다. key는 고정값 `json`이고 value는 대응되는 JSON key입니다.

```go
type Request struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

var req Request
err := httpx.Parse(r, &req)
```

### Path 요청 매개변수

path 매개변수는 구조체 tag에 `path` keyword를 추가해 정의합니다. 특정 path parameter를 가져오는 데 사용하며, tag는 k-v 형식입니다. key는 고정값 `path`이고 value는 path argument입니다.

```go
type Request struct {
    Name string `path:"name"`
}

// Path definitions
rest.Route{
    Method:  http.MethodGet,
    Path:    "/user/:name",
    Handler: handle,
}

var req Request
err := httpx.Parse(r, &req)
```

### Header 매개변수 가져오기

header 매개변수는 구조체 tag에 `header` keyword를 추가해 가져옵니다. tag는 k-v 형식이며, key는 고정값 `header`, value는 request header의 key입니다.

```go
type Request struct {
    Authorization string `header:"authorization"`
}

var req Request
err := httpx.Parse(r, &req)
```

## 매개변수 검증

### Optional 매개변수

go-zero에서는 구조체 tag의 `optional` keyword로 매개변수를 선택 사항으로 만들 수 있습니다. 필수가 아닌 매개변수에는 해당 매개변수 뒤에 `optional` keyword를 추가합니다. 추가하지 않으면 필수 매개변수로 간주합니다.

```go
type Request struct {
    Age int `form:"age,optional"`
}

var req Request
err := httpx.Parse(r, &req)
```

:::tip

필수 매개변수가 전달되지 않으면 다음 오류가 반환됩니다.

```
field age is not set
```

:::

### 매개변수 range 정의

go-zero는 매개변수 구간 정의를 제공합니다. 구조체 tag에 `range` keyword를 추가해 정의하며, 형식은 `range=$range_expression`입니다.

```go
type Request struct {
    Age int `form:"age,range=[18:35)"`
}

var req Request
err := httpx.Parse(r, &req)
```

매개변수 구간에 대한 자세한 내용은 API 문법의 [매개변수 규칙](../../../reference/api-dsl/parameter.md)을 참고하세요.

### 매개변수 enum 값

go-zero는 매개변수 enum 값 정의를 제공합니다. 구조체 tag에 `options` keyword를 추가해 정의하며, 형식은 `options=$option_expression`입니다. 여러 enum 값은 `options=18|19`처럼 구분해 작성하며, 정의되지 않은 값은 허용되지 않습니다.

```go
type Request struct {
    Age int `form:"age,options=18|19"`
}

var req Request
err := httpx.Parse(r, &req)
```

### 매개변수 기본값

go-zero는 매개변수 기본값을 제공합니다. 구조체 tag에 `default` keyword를 추가해 정의하며, 형식은 `default=$default_value`입니다. 이는 optional 매개변수의 확장 기능이며, optional 매개변수의 기본 zero value 대신 지정한 기본값을 사용할 수 있게 합니다.

```go
type Request struct {
    Age int `form:"age,default=18"`
}

var req Request
err := httpx.Parse(r, &req)
```

## 참고 자료

- [API | HTTP 요청 매개변수 규칙](../../../reference/api-dsl/parameter.md)
