---
title: API 타입
description: go-zero의 API 타입에 대해 설명합니다.
sidebar:
  order: 5

---


## 개요


## 타입 선언


1. 타입 declaration must 시작 사용하여 `type`
1. 없음 need 로 declare `structure`keywords
1. Nested Structural 선언s are 아님 supported
1. Alias 아님 supported

### 샘플

```go

type StructureExample {
    // 기본 예시
    BaseInt     int     `json:"base_int"`
    BaseBool    bool    `json:"base_bool"`
    BaseString  string  `json:"base_string"`
    BaseByte    byte    `json:"base_byte"`
    BaseFloat32 float32 `json:"base_float32"`
    BaseFloat64 float64 `json:"base_float64"`
    // 예시입니다
    BaseIntSlice     []int     `json:"base_int_slice"`
    BaseBoolSlice    []bool    `json:"base_bool_slice"`
    BaseStringSlice  []string  `json:"base_string_slice"`
    BaseByteSlice    []byte    `json:"base_byte_slice"`
    BaseFloat32Slice []float32 `json:"base_float32_slice"`
    BaseFloat64Slice []float64 `json:"base_float64_slice"`
    // map example
    BaseMapIntString      map[int]string               `json:"base_map_int_string"`
    BaseMapStringInt      map[string]int               `json:"base_map_string_int"`
    BaseMapStringStruct   map[string]*StructureExample `json:"base_map_string_struct"`
    BaseMapStringIntArray map[string][]int             `json:"base_map_string_int_array"`
    // 예시입니다
    *Base
    // 예시입니다
    Base4 *Base `json:"base4"`

    // 예시입니다
    // 예시입니다
    TagOmit string
}
```

:::tip
새로운 API 기능은 available since goctl 1.5.1 — see [새로운 API Feature FAQ](./faq.md)입니다.

참고: generic과 weak (any) types은 아님 supported입니다.

위한 discussion, see [go-zero/discussions/3121](https://github.com/zeromicro/go-zero/discussions/3121).
:::
