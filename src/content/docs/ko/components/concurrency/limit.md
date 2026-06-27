---
title: syncx Limit
description: go-zero syncx의 borrow/return semaphore를 사용한 동시성 제한입니다.
sidebar:
  order: 10

---

## syncx.Limit

`syncx` 패키지는 `Limit` 타입을 통해 동시성 제한 primitive를 제공합니다. 내부적으로 buffered channel을 semaphore처럼 사용해 동시에 처리 중인 요청 수를 제한합니다.

## 변수

### ErrLimitReturn

```go
var ErrLimitReturn = errors.New("discarding limited token, resource pool is full, someone returned multiple times")
```

빌린 토큰보다 더 많은 토큰을 반환하려고 할 때 반환됩니다. 즉, resource pool이 이미 가득 찬 상태입니다.

## 타입

### Limit

```go
type Limit struct {
    pool chan lang.PlaceholderType
}
```

`Limit`은 동시 요청 수를 제어하는 buffered channel `pool`을 감싼 타입입니다.

## 함수

### NewLimit

```go
func NewLimit(n int) Limit
```

동시에 최대 `n`개까지 borrow할 수 있는 `Limit`을 생성합니다.

**매개변수**

- `n` (`int`): 동시에 빌릴 수 있는 최대 개수입니다.

**반환**

- `Limit`: 새 `Limit` 인스턴스입니다.

### Borrow

```go
func (l Limit) Borrow()
```

토큰을 사용할 수 있을 때까지 대기한 뒤 획득합니다.

### Return

```go
func (l Limit) Return() error
```

이전에 빌린 토큰을 반환합니다. pool이 이미 가득 차 있으면, 즉 빌린 횟수보다 더 많이 반환하면 `ErrLimitReturn`을 반환합니다.

**반환**

- `error`: 성공하면 `nil`, 초과 반환이면 `ErrLimitReturn`입니다.

### TryBorrow

```go
func (l Limit) TryBorrow() bool
```

대기하지 않고 토큰 획득을 시도합니다.

**반환**

- `bool`: 토큰을 획득했으면 `true`, 사용할 수 있는 토큰이 없으면 `false`입니다.

## 예제

```go
package main

import (
    "fmt"

    "github.com/zeromicro/go-zero/core/syncx"
)

func main() {
    limit := syncx.NewLimit(3) // 동시 작업을 최대 3개로 제한합니다

    // 대기하지 않고 시도합니다
    if limit.TryBorrow() {
        fmt.Println("acquired token")
        if err := limit.Return(); err != nil {
            fmt.Println("return error:", err)
        }
    }

    // 토큰을 얻을 때까지 대기합니다
    limit.Borrow()
    defer limit.Return()
    fmt.Println("doing work under limit")
}
```
