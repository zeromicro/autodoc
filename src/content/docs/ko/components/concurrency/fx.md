---
title: FX 파이프라인
description: go-zero의 FX 스트리밍 유틸리티로 데이터 파이프라인을 구성하는 방법입니다.
sidebar:
  order: 2

---

`fx` 패키지는 스트림 처리를 위한 강력하고 유연한 API를 제공합니다. 필터링, 매핑, 리듀싱, 그룹화 등 다양한 연산을 스트림 위에서 조합해 수행할 수 있습니다.

### 함수 타입

#### `FilterFunc`

스트림을 필터링하는 함수 타입입니다.

```go
type FilterFunc func(item any) bool
```

#### `ForAllFunc`

스트림의 모든 요소를 처리하는 함수 타입입니다.

```go
type ForAllFunc func(pipe <-chan any)
```

#### `ForEachFunc`

스트림의 각 요소를 처리하는 함수 타입입니다.

```go
type ForEachFunc func(item any)
```

#### `GenerateFunc`

스트림으로 요소를 보내는 함수 타입입니다.

```go
type GenerateFunc func(source chan<- any)
```

#### `KeyFunc`

스트림 요소의 키를 생성하는 함수 타입입니다.

```go
type KeyFunc func(item any) any
```

#### `LessFunc`

스트림 요소를 비교하는 함수 타입입니다.

```go
type LessFunc func(a, b any) bool
```

#### `MapFunc`

스트림의 각 요소를 다른 객체로 매핑하는 함수 타입입니다.

```go
type MapFunc func(item any) any
```

#### `Option`

스트림 동작을 조정하는 함수 타입입니다.

```go
type Option func(opts *rxOptions)
```

#### `ParallelFunc`

요소를 병렬로 처리하는 함수 타입입니다.

```go
type ParallelFunc func(item any)
```

#### `ReduceFunc`

스트림의 모든 요소를 리듀싱하는 함수 타입입니다.

```go
type ReduceFunc func(pipe <-chan any) (any, error)
```

#### `WalkFunc`

스트림의 모든 요소를 순회하는 함수 타입입니다.

```go
type WalkFunc func(item any, pipe chan<- any)
```

### `Stream`

`Stream`은 스트림 처리를 수행하는 데 사용할 수 있는 데이터 흐름입니다.

```go
type Stream struct {
    source <-chan any
}
```

## 함수

### `Concat`

여러 스트림을 이어 붙인 스트림을 반환합니다.

```go
func Concat(s Stream, others ...Stream) Stream
```

### `From`

주어진 `GenerateFunc`로 스트림을 생성합니다.

```go
func From(generate GenerateFunc) Stream
```

### `Just`

주어진 임의의 항목들을 스트림으로 변환합니다.

```go
func Just(items ...any) Stream
```

### `Range`

주어진 채널을 스트림으로 변환합니다.

```go
func Range(source <-chan any) Stream
```

### Stream 메서드

#### `AllMatch`

스트림의 모든 요소가 제공한 조건 함수와 일치하는지 반환합니다.

```go
func (s Stream) AllMatch(predicate func(item any) bool) bool
```

#### `AnyMatch`

스트림의 요소 중 하나라도 제공한 조건 함수와 일치하는지 반환합니다.

```go
func (s Stream) AnyMatch(predicate func(item any) bool) bool
```

#### `Buffer`

항목을 크기 `n`의 큐에 버퍼링합니다.

```go
func (s Stream) Buffer(n int) Stream
```

#### `Concat`

다른 스트림들을 이어 붙인 스트림을 반환합니다.

```go
func (s Stream) Concat(others ...Stream) Stream
```

#### `Count`

결과의 요소 수를 계산합니다.

```go
func (s Stream) Count() (count int)
```

#### `Distinct`

주어진 `KeyFunc`를 기준으로 중복 항목을 제거합니다.

```go
func (s Stream) Distinct(fn KeyFunc) Stream
```

#### `Done`

모든 상위 단계 작업이 끝날 때까지 기다립니다.

```go
func (s Stream) Done()
```

#### `Filter`

주어진 `FilterFunc`로 항목을 필터링합니다.

```go
func (s Stream) Filter(fn FilterFunc, opts ...Option) Stream
```

#### `First`

첫 번째 항목을 반환하며, 항목이 없으면 `nil`을 반환합니다.

```go
func (s Stream) First() any
```

#### `ForAll`

소스에서 흘러오는 스트림 요소를 처리하고, 이후 스트림으로 이어지지 않습니다.

```go
func (s Stream) ForAll(fn ForAllFunc)
```

#### `ForEach`

각 항목에 `ForEachFunc`를 적용하고 스트림을 종료합니다. 이후 연산은 없습니다.

```go
func (s Stream) ForEach(fn ForEachFunc)
```

#### `Group`

각 요소의 키를 기준으로 서로 다른 그룹으로 묶습니다.

```go
func (s Stream) Group(fn KeyFunc) Stream
```

#### `Head`

처음 `n`개 요소를 반환합니다.

```go
func (s Stream) Head(n int64) Stream
```

#### `Last`

마지막 항목을 반환하며, 항목이 없으면 `nil`을 반환합니다.

```go
func (s Stream) Last() (item any)
```

#### `Map`

각 항목을 대응되는 다른 항목으로 변환합니다. 즉, 1:1 매핑 모델입니다.

```go
func (s Stream) Map(fn MapFunc, opts ...Option) Stream
```

#### `Max`

내부 소스에서 최댓값 항목을 반환합니다.

```go
func (s Stream) Max(less LessFunc) any
```

#### `Merge`

모든 항목을 슬라이스로 합쳐 새 스트림을 생성합니다.

```go
func (s Stream) Merge() Stream
```

#### `Min`

내부 소스에서 최솟값 항목을 반환합니다.

```go
func (s Stream) Min(less LessFunc) any
```

#### `NoneMatch`

스트림의 모든 요소가 제공한 조건 함수와 일치하지 않는지 반환합니다.

```go
func (s Stream) NoneMatch(predicate func(item any) bool) bool
```

#### `Parallel`

주어진 `ParallelFunc`를 각 항목에 병렬로 적용하며, 옵션으로 워커 수를 지정할 수 있습니다.

```go
func (s Stream) Parallel(fn ParallelFunc, opts ...Option)
```

#### `Reduce`

호출자가 내부 채널을 직접 처리할 수 있게 하는 유틸리티 메서드입니다.

```go
func (s Stream) Reduce(fn ReduceFunc) (any, error)
```

#### `Reverse`

스트림의 요소 순서를 뒤집습니다.

```go
func (s Stream) Reverse() Stream
```

#### `Skip`

앞의 `n`개 요소를 건너뛴 스트림을 반환합니다.

```go
func (s Stream) Skip(n int64) Stream
```

#### `Sort`

내부 소스의 항목을 정렬합니다.

```go
func (s Stream) Sort(less LessFunc) Stream
```

#### `Split`

요소를 최대 `n`개 크기의 묶음으로 나눕니다.

```go
func (s Stream) Split(n int) Stream
```

#### `Tail`

마지막 `n`개 요소를 반환합니다.

```go
func (s Stream) Tail(n int64) Stream
```

#### `Walk`

호출자가 각 항목을 처리하도록 합니다. 주어진 항목을 기준으로 0개, 1개 또는 여러 항목을 출력할 수 있습니다.

```go
func (s Stream) Walk(fn WalkFunc, opts ...Option) Stream
```

## 옵션

### `UnlimitedWorkers`

작업 수만큼 워커를 사용할 수 있게 합니다.

```go
func UnlimitedWorkers() Option
```

### `WithWorkers`

동시에 실행할 워커 수를 지정합니다.

```go
func WithWorkers(workers int) Option
```

## 예제

다음 예제들은 `fx` 패키지를 사용해 스트림 처리 작업을 수행하는 방법을 보여 줍니다.

### 예제 1: 배열에서 스트림을 만들고 요소 필터링하기

```go
package main

import (
	"fmt"

	"github.com/zeromicro/go-zero/core/fx"
)

func main() {
	items := []any{1, 2, 3, 4, 5}

	stream := fx.Just(items...).
		Filter(func(item any) bool {
			return item.(int)%2 == 0
		})

	for item := range stream.source {
		fmt.Println(item)
	}
}
```

**설명:**

1. `Just` 메서드로 배열을 스트림으로 변환합니다.
2. `Filter` 메서드로 짝수만 남깁니다.
3. 스트림을 순회하며 결과를 출력합니다.

### 예제 2: 스트림 요소를 병렬로 처리하기

```go
package main

import (
	"fmt"

	"github.com/zeromicro/go-zero/core/fx"
)

func main() {
	items := []any{1, 2, 3, 4, 5}

	fx.Just(items...).
		Parallel(func(item any) {
			fmt.Printf("Processing %v\n", item)
		}, fx.WithWorkers(3))
}
```

**설명:**

1. `Just` 메서드로 배열을 스트림으로 변환합니다.
2. `Parallel` 메서드로 각 요소를 병렬 처리하고 워커 수를 3으로 지정합니다.
3. 처리 중인 각 요소를 출력합니다.

### 예제 3: 스트림 요소 정렬하기

```go
package main

import (
	"fmt"

	"github.com/zeromicro/go-zero/core/fx"
)

func main() {
	items := []any{4, 2, 5, 1, 3}

	stream := fx.Just(items...).
		Sort(func(a, b any) bool {
			return a.(int) < b.(int)
		})

	for item := range stream.source {
		fmt.Println(item)
	}
}
```

**설명:**

1. `Just` 메서드로 배열을 스트림으로 변환합니다.
2. `Sort` 메서드로 요소를 정렬합니다.
3. 스트림을 순회하며 정렬된 결과를 출력합니다.

### 예제 4: 스트림 요소 리듀싱하기

```go
package main

import (
	"fmt"

	"github.com/zeromicro/go-zero/core/fx"
)

func main() {
	items := []any{1, 2, 3, 4, 5}

	result, _ := fx.Just(items...).
		Reduce(func(pipe <-chan any) (any, error) {
			sum := 0
			for item := range pipe {
				sum += item.(int)
			}
			return sum, nil
		})

	fmt.Println(result) // 출력: 15
}
```

**설명:**

1. `Just` 메서드로 배열을 스트림으로 변환합니다.
2. `Reduce` 메서드로 스트림의 모든 요소 합계를 계산합니다.
3. 리듀싱 결과를 출력합니다.

### 예제 5: 스트림 요소 그룹화하기

```go
package main

import (
	"fmt"

	"github.com/zeromicro/go-zero/core/fx"
)

func main() {
	items := []any{"apple", "banana", "avocado", "blueberry"}

	stream := fx.Just(items...).
		Group(func(item any) any {
			return item.(string)[0] // 첫 글자로 그룹화합니다
		})

	for group := range stream.source {
		fmt.Println(group)
	}
}
```

**설명:**

1. `Just` 메서드로 배열을 스트림으로 변환합니다.
2. `Group` 메서드로 첫 글자를 기준으로 요소를 그룹화합니다.
3. 스트림을 순회하며 각 그룹을 출력합니다.

이 예제들은 `fx` 패키지가 스트림 연산으로 데이터 처리를 단순화하는 방법을 보여 줍니다. 실제 코드의 요구 사항에 맞게 여러 메서드를 조합해 적용할 수 있습니다.
