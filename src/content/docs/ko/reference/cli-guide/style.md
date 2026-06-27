---
title: goctl 스타일
description: go-zero의 goctl 스타일에 대해 설명합니다.
sidebar:
  order: 12

---


## 개요


## 포맷팅 symbols


- lowercase: `gozero`
- camelcase: `goZero`
- snakecase: `go_zero`

## 포맷팅 Symbol Table 참조


| 포맷팅 symbols | Formatted string       | 참고                                                                                     |
| ------------------ | ---------------------- | ---------------------------------------------------------------------------------------- |
| `gozero`           | `welcometogozero`      | lower case                                                                               |
| `goZero`           | `welcomeToGoZero`      | camel case                                                                               |
| `go_zero`          | `welcome_to_go_zero`   | snake case                                                                               |
| `Go#zero`          | `Welcome#to#go#zero`   | Custom separator like separator `#`                                                      |
| `GOZERO`           | `WELCOMETOGOZERO`      | upper case                                                                               |
| `_go#zero_`        | `_welcome#to#go#zero_` |해당 항목의 동작과 사용법을 설명합니다. |

:::note Illegal symbols

- go
- gOZero
- zero
- goZEro
- goZERo
- goZeRo
- foo
:::

## 사용법


```bash
$ goctl api new demo --style gozero
$ goctl api new demo --style go_zero
$ goctl api new demo --style goZero
```
