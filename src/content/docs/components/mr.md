---
title: MapReduce
description: Concurrent map-reduce for Go with go-zero mr.
sidebar:
  order: 3

---


# mr Package Documentation

## Overview

The `mr` package provides a framework for performing map-reduce operations in Go. It supports concurrent execution of mapping and reducing functions with customizable settings.

### Errors

```go
var (
    ErrCancelWithNil = errors.New("mapreduce cancelled with nil")
    ErrReduceNoOutput = errors.New("reduce not writing value")
)
```

- **ErrCancelWithNil**: Error indicating that the map-reduce operation was canceled with nil.
- **ErrReduceNoOutput**: Error indicating that the reduce function did not produce any output.

## Types

### ForEachFunc

```go
type ForEachFunc[T any] func(item T)
```

Function type for processing each element without output.

### GenerateFunc

```go
type GenerateFunc[T any] func(source chan<- T)
```

Function type for generating elements to be processed.

### MapFunc

```go
type MapFunc[T, U any] func(item T, writer Writer[U])
```

Function type for processing an element and writing the output using a writer.

### MapperFunc

```go
type MapperFunc[T, U any] func(item T, writer Writer[U], cancel func(error))
```

Function type for processing an element with support for cancellation.

### ReducerFunc

```go
type ReducerFunc[U, V any] func(pipe <-chan U, writer Writer[V], cancel func(error))
```

Function type for reducing output elements from the mapping stage into a final result.

### VoidReducerFunc

```go
type VoidReducerFunc[U any] func(pipe <-chan U, cancel func(error))
```

Function type for reducing output elements without producing a final result.

### Option

```go
type Option func(opts *mapReduceOptions)
```

Function type for customizing map-reduce options.

### Writer

```go
type Writer[T any] interface {
    Write(v T)
}
```

Interface for writing values.

## Functions

### Finish

```go
func Finish(fns ...func() error) error
```

Runs functions in parallel and cancels on any error.

### FinishVoid

```go
func FinishVoid(fns ...func())
```

Runs functions in parallel without output.

### ForEach

```go
func ForEach[T any](generate GenerateFunc[T], mapper ForEachFunc[T], opts ...Option)
```

Maps all elements from the generate function but produces no output.

### MapReduce

```go
func MapReduce[T, U, V any](generate GenerateFunc[T], mapper MapperFunc[T, U], reducer ReducerFunc[U, V],
opts ...Option) (V, error)
```

Performs map-reduce operation using the provided generate function, mapper, and reducer.

### MapReduceChan

```go
func MapReduceChan[T, U, V any](source <-chan T, mapper MapperFunc[T, U], reducer ReducerFunc[U, V],
opts ...Option) (V, error)
```

Performs map-reduce operation using the provided source channel, mapper, and reducer.

### MapReduceVoid

```go
func MapReduceVoid[T, U any](generate GenerateFunc[T], mapper MapperFunc[T, U],
reducer VoidReducerFunc[U], opts ...Option) error
```

Performs map-reduce operation using the provided generate function and mapper, but produces no final result.

### WithContext

```go
func WithContext(ctx context.Context) Option
```

Customizes a map-reduce operation to use a given context.

### WithWorkers

```go
func WithWorkers(workers int) Option
```

Customizes a map-reduce operation to use a specified number of workers.

Below are some examples demonstrating various functionalities of the mr package:

### Example 1: Processing Each Element (ForEach)

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

### Example 2: Simple MapReduce Operation

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

### Example 3: MapReduce Operation with Cancellation

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

### Example 4: Parallel Execution of Multiple Functions (Finish and FinishVoid)

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

These examples showcase different usages of the `mr` package from `go-zero`, including basic element processing, simple MapReduce operations, MapReduce operations with cancellation, and parallel execution of multiple functions. Choose and modify these examples according to your specific requirements.
