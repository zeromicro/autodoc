---
title: MapReduce
description: 使用 go-zero mr 进行并发 map-reduce。
sidebar:
  order: 3

---


# mr 文档

## 概述

`mr` 包提供了一个在 Go 语言中执行 MapReduce 操作的框架。它支持并发执行映射和归约函数，并且可以自定义设置。

### 错误

```go
var (
    ErrCancelWithNil = errors.New("mapreduce cancelled with nil")
    ErrReduceNoOutput = errors.New("reduce not writing value")
)
```

- **ErrCancelWithNil**：表示 MapReduce 操作被取消并且未返回错误。
- **ErrReduceNoOutput**：表示归约函数没有输出任何值。

## 类型

### ForEachFunc

```go
type ForEachFunc[T any] func(item T)
```

用于处理每个元素但没有输出的函数类型。

### GenerateFunc

```go
type GenerateFunc[T any] func(source chan<- T)
```

用于生成要处理的元素的函数类型。

### MapFunc

```go
type MapFunc[T, U any] func(item T, writer Writer[U])
```

用于处理元素并通过 writer 写出结果的函数类型。

### MapperFunc

```go
type MapperFunc[T, U any] func(item T, writer Writer[U], cancel func(error))
```

用于处理元素并支持取消功能的函数类型。

### ReducerFunc

```go
type ReducerFunc[U, V any] func(pipe <-chan U, writer Writer[V], cancel func(error))
```

用于将映射阶段的输出元素归约为最终结果的函数类型。

### VoidReducerFunc

```go
type VoidReducerFunc[U any] func(pipe <-chan U, cancel func(error))
```

用于归约输出元素但不产生最终结果的函数类型。

### Option

```go
type Option func(opts *mapReduceOptions)
```

自定义 MapReduce 选项的方法。

### Writer

```go
type Writer[T any] interface {
    Write(v T)
}
```

封装写入方法的接口。

## 函数

### Finish

```go
func Finish(fns ...func() error) error
```

并行运行函数，如果有任何错误则取消。

### FinishVoid

```go
func FinishVoid(fns ...func())
```

并行运行函数，不产生输出。

### ForEach

```go
func ForEach[T any](generate GenerateFunc[T], mapper ForEachFunc[T], opts ...Option)
```

映射所有由 generate 函数生成的元素，但不产生输出。

### MapReduce

```go
func MapReduce[T, U, V any](generate GenerateFunc[T], mapper MapperFunc[T, U], reducer ReducerFunc[U, V],
opts ...Option) (V, error)
```

使用给定的 generate 函数、mapper 和 reducer 执行 MapReduce 操作。

### MapReduceChan

```go
func MapReduceChan[T, U, V any](source <-chan T, mapper MapperFunc[T, U], reducer ReducerFunc[U, V],
opts ...Option) (V, error)
```

使用给定的源 channel、mapper 和 reducer 执行 MapReduce 操作。

### MapReduceVoid

```go
func MapReduceVoid[T, U any](generate GenerateFunc[T], mapper MapperFunc[T, U],
reducer VoidReducerFunc[U], opts ...Option) error
```

使用给定的 generate 函数和 mapper 执行 MapReduce 操作，但不产生最终结果。

### WithContext

```go
func WithContext(ctx context.Context) Option
```

自定义 MapReduce 操作以使用给定的上下文（context）。

### WithWorkers

```go
func WithWorkers(workers int) Option
```

自定义 MapReduce 操作以使用指定数量的 worker。

下面是一些使用 `mr` 包的示例代码来演示各种功能：

### 示例1：处理每个元素（ForEach）

```go
package main

import (
    "fmt"
    
    "github.com/zeromicro/go-zero/core/mr"
)

func main() {
    generateFunc := func(source chan<- int) {
        for i := 0; i < 10; i++ {
            source <- i
        }
    }

    mapperFunc := func(item int) {
        fmt.Println("Processing item:", item)
    }

    mr.ForEach(generateFunc, mapperFunc, mr.WithWorkers(4))
}
```

### 示例2：简单的 MapReduce 操作

```go
package main

import (
    "fmt"
    
    "github.com/zeromicro/go-zero/core/mr"
)

func main() {
    generateFunc := func(source chan<- int) {
        for i := 0; i < 10; i++ {
            source <- i
        }
    }

    mapperFunc := func(item int, writer mr.Writer[int], cancel func(error)) {
        writer.Write(item * 2)
    }

    reducerFunc := func(pipe <-chan int, writer mr.Writer[int], cancel func(error)) {
        sum := 0
        for v := range pipe {
            sum += v
        }
        writer.Write(sum)
    }

    result, err := mr.MapReduce(generateFunc, mapperFunc, reducerFunc, mr.WithWorkers(4))
    if err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("Result:", result) // Output: Result: 90
    }
}
```

### 示例3：带有取消功能的 MapReduce 操作

```go
package main

import (
    "context"
    "fmt"
    "time"
    
    "github.com/zeromicro/go-zero/core/mr"
)

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()

    generateFunc := func(source chan<- int) {
        for i := 0; i < 100; i++ {
            source <- i
            time.Sleep(100 * time.Millisecond)
        }
    }

    mapperFunc := func(item int, writer mr.Writer[int], cancel func(error)) {
        writer.Write(item * 2)
    }

    reducerFunc := func(pipe <-chan int, writer mr.Writer[int], cancel func(error)) {
        sum := 0
        for v := range pipe {
            sum += v
        }
        writer.Write(sum)
    }

    result, err := mr.MapReduce(generateFunc, mapperFunc, reducerFunc, mr.WithContext(ctx), mr.WithWorkers(4))
    if err != nil {
        fmt.Println("Error:", err) // Expected to timeout
    } else {
        fmt.Println("Result:", result)
    }
}
```

### 示例4：并行执行多个函数（Finish 和 FinishVoid）

```go
package main

import (
    "fmt"
    "errors"
    
    "github.com/zeromicro/go-zero/core/mr"
)

func main() {
    funcs := []func() error{
        func() error {
            fmt.Println("Function 1 executed")
            return nil
        },
        func() error {
            fmt.Println("Function 2 executed")
            return errors.New("error in function 2")
        },
    }

    err := mr.Finish(funcs...)
    if err != nil {
        fmt.Println("Finish encountered an error:", err)
    }

    voidFuncs := []func(){
        func() {
            fmt.Println("Void Function 1 executed")
        },
        func() {
            fmt.Println("Void Function 2 executed")
        },
    }

    mr.FinishVoid(voidFuncs...)
}
```

这些示例展示了 `go-zero` 中 `mr` 包的不同用法，包括基础的元素处理，基本的 MapReduce 操作，带有取消功能的 MapReduce 操作，以及并行执行多个函数。根据你的具体需求来选择和修改这些示例代码。
