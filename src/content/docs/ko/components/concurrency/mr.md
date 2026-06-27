---
title: MapReduce
description: go-zero의 mr 패키지로 Go에서 동시 MapReduce 작업을 수행하는 방법입니다.
sidebar:
  order: 3

---

## 개요

`mr` 패키지는 Go에서 MapReduce 작업을 수행하기 위한 프레임워크입니다. 매핑 함수와 리듀싱 함수를 동시에 실행할 수 있으며, 워커 수와 컨텍스트 같은 옵션을 조정할 수 있습니다.

### 오류

```go
var (
    ErrCancelWithNil = errors.New("mapreduce cancelled with nil")
    ErrReduceNoOutput = errors.New("reduce not writing value")
)
```

- **ErrCancelWithNil**: MapReduce 작업이 `nil` 오류로 취소되었음을 나타냅니다.
- **ErrReduceNoOutput**: reduce 함수가 아무 출력도 만들지 않았음을 나타냅니다.

## 타입

### ForEachFunc

```go
type ForEachFunc[T any] func(item T)
```

출력 없이 각 요소를 처리하는 함수 타입입니다.

### GenerateFunc

```go
type GenerateFunc[T any] func(source chan<- T)
```

처리할 요소를 생성하는 함수 타입입니다.

### MapFunc

```go
type MapFunc[T, U any] func(item T, writer Writer[U])
```

요소 하나를 처리하고 `writer`로 결과를 쓰는 함수 타입입니다.

### MapperFunc

```go
type MapperFunc[T, U any] func(item T, writer Writer[U], cancel func(error))
```

취소를 지원하면서 요소 하나를 처리하는 함수 타입입니다.

### ReducerFunc

```go
type ReducerFunc[U, V any] func(pipe <-chan U, writer Writer[V], cancel func(error))
```

매핑 단계에서 나온 요소들을 최종 결과로 줄이는 함수 타입입니다.

### VoidReducerFunc

```go
type VoidReducerFunc[U any] func(pipe <-chan U, cancel func(error))
```

최종 결과를 만들지 않고 매핑 단계의 출력 요소를 소비하는 리듀서 함수 타입입니다.

### Option

```go
type Option func(opts *mapReduceOptions)
```

MapReduce 옵션을 조정하는 함수 타입입니다.

### Writer

```go
type Writer[T any] interface {
    Write(v T)
}
```

값을 쓰기 위한 인터페이스입니다.

## 함수

### Finish

```go
func Finish(fns ...func() error) error
```

여러 함수를 병렬로 실행하고, 어느 하나라도 오류를 반환하면 나머지 작업을 취소합니다.

### FinishVoid

```go
func FinishVoid(fns ...func())
```

반환값이 없는 여러 함수를 병렬로 실행합니다.

### ForEach

```go
func ForEach[T any](generate GenerateFunc[T], mapper ForEachFunc[T], opts ...Option)
```

`generate` 함수가 만든 모든 요소에 `mapper`를 적용하지만 출력은 만들지 않습니다.

### MapReduce

```go
func MapReduce[T, U, V any](generate GenerateFunc[T], mapper MapperFunc[T, U], reducer ReducerFunc[U, V],
opts ...Option) (V, error)
```

제공한 `generate` 함수, `mapper`, `reducer`로 MapReduce 작업을 수행합니다.

### MapReduceChan

```go
func MapReduceChan[T, U, V any](source <-chan T, mapper MapperFunc[T, U], reducer ReducerFunc[U, V],
opts ...Option) (V, error)
```

제공한 소스 채널, `mapper`, `reducer`로 MapReduce 작업을 수행합니다.

### MapReduceVoid

```go
func MapReduceVoid[T, U any](generate GenerateFunc[T], mapper MapperFunc[T, U],
reducer VoidReducerFunc[U], opts ...Option) error
```

제공한 `generate` 함수와 `mapper`로 MapReduce 작업을 수행하지만 최종 결과는 만들지 않습니다.

### WithContext

```go
func WithContext(ctx context.Context) Option
```

지정한 컨텍스트를 사용하도록 MapReduce 작업을 설정합니다.

### WithWorkers

```go
func WithWorkers(workers int) Option
```

지정한 수의 워커를 사용하도록 MapReduce 작업을 설정합니다.

아래 예제들은 `mr` 패키지의 여러 기능을 보여 줍니다.

### 예제 1: 각 요소 처리하기(ForEach)

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

### 예제 2: 간단한 MapReduce 작업

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
        fmt.Println("Result:", result) // 출력: Result: 90
    }
}
```

### 예제 3: 취소를 사용하는 MapReduce 작업

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
        fmt.Println("Error:", err) // 시간 초과가 발생할 수 있습니다
    } else {
        fmt.Println("Result:", result)
    }
}
```

### 예제 4: 여러 함수 병렬 실행(Finish와 FinishVoid)

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

이 예제들은 기본 요소 처리, 간단한 MapReduce 작업, 컨텍스트 취소를 사용하는 MapReduce 작업, 여러 함수의 병렬 실행 등 `go-zero`의 `mr` 패키지를 활용하는 여러 방법을 보여 줍니다. 실제 요구 사항에 맞게 예제를 선택해 수정하세요.
