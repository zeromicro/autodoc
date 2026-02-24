---
title: Limit
sidebar:
  order: 10

---

# syncx.Limit

`syncx` 包提供了一种管理并发请求的限流机制。通过定义一个 `Limit` 类型，可以控制同时进行的请求数量。

## 变量

### ErrLimitReturn

```go
var ErrLimitReturn = errors.New("discarding limited token, resource pool is full, someone returned multiple times")
```

`ErrLimitReturn` 表示当归还的元素超过借用的数量时，资源池已满的错误信息。

## 类型

### Limit

```go
type Limit struct {
    pool chan lang.PlaceholderType
}
```

`Limit` 是一个包含带缓冲通道 `pool` 的结构体，用于控制并发请求的数量。

## 函数

### NewLimit

```go
func NewLimit(n int) Limit
```

`NewLimit` 创建一个可以同时借用 `n` 个元素的 `Limit` 实例。

#### 参数

- `n` (`int`): 可同时借用的元素数量。

#### 返回值

- `Limit`: 一个新的 `Limit` 实例。

### Borrow

```go
func (l Limit) Borrow()
```

`Borrow` 方法以阻塞模式借用一个元素。

### Return

```go
func (l Limit) Return() error
```

`Return` 方法归还借用的资源。如果归还的资源超过借用的数量，则返回错误 `ErrLimitReturn`。

#### 返回值

- `error`: 如果归还成功返回 `nil`，否则返回 `ErrLimitReturn` 错误。

### TryBorrow

```go
func (l Limit) TryBorrow() bool
```

`TryBorrow` 方法以非阻塞模式尝试借用一个元素。

#### 返回值

- `bool`: 如果成功借用，返回 `true`，否则返回 `false`。

## 用法示例

```go
package main

import (
	"fmt"
	"log"
	"syncx"
)

func main() {
	limit := syncx.NewLimit(2)

	if limit.TryBorrow() {
		fmt.Println("Successfully borrowed the first token.")
	} else {
		fmt.Println("Failed to borrow the first token.")
	}

	if limit.TryBorrow() {
		fmt.Println("Successfully borrowed the second token.")
	} else {
		fmt.Println("Failed to borrow the second token.")
	}

	if limit.TryBorrow() {
		fmt.Println("Successfully borrowed the third token.")
	} else {
		fmt.Println("Failed to borrow the third token.")
	}

	err := limit.Return()
	if err != nil {
		log.Println("Error returning token:", err)
	} else {
		fmt.Println("Successfully returned a token.")
	}

	err = limit.Return()
	if err != nil {
		log.Println("Error returning token:", err)
	} else {
		fmt.Println("Successfully returned a token.")
	}
}
```
