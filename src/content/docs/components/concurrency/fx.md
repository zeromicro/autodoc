---
title: FX Pipeline
description: Build data pipelines with go-zero's FX streaming utility.
sidebar:
  order: 2

---



The `fx` package provides a powerful and flexible API for stream processing. It allows users to perform various operations on streams, including filtering, mapping, reducing, grouping, and more.

### Function Types
#### `FilterFunc`
Defines the method to filter a Stream.
```go
type FilterFunc func(item any) bool
```

#### `ForAllFunc`
Defines the method to handle all elements in a Stream.
```go
type ForAllFunc func(pipe <-chan any)
```

#### `ForEachFunc`
Defines the method to handle each element in a Stream.
```go
type ForEachFunc func(item any)
```

#### `GenerateFunc`
Defines the method to send elements into a Stream.
```go
type GenerateFunc func(source chan<- any)
```

#### `KeyFunc`
Defines the method to generate keys for the elements in a Stream.
```go
type KeyFunc func(item any) any
```

#### `LessFunc`
Defines the method to compare the elements in a Stream.
```go
type LessFunc func(a, b any) bool
```

#### `MapFunc`
Defines the method to map each element to another object in a Stream.
```go
type MapFunc func(item any) any
```

#### `Option`
Defines the method to customize a Stream.
```go
type Option func(opts *rxOptions)
```

#### `ParallelFunc`
Defines the method to handle elements parallelly.
```go
type ParallelFunc func(item any)
```

#### `ReduceFunc`
Defines the method to reduce all the elements in a Stream.
```go
type ReduceFunc func(pipe <-chan any) (any, error)
```

#### `WalkFunc`
Defines the method to walk through all the elements in a Stream.
```go
type WalkFunc func(item any, pipe chan<- any)
```

### `Stream`
A Stream is a stream that can be used to do stream processing.
```go
type Stream struct {
    source <-chan any
}
```

## Functions

### `Concat`
Returns a concatenated Stream.
```go
func Concat(s Stream, others ...Stream) Stream
```

### `From`
Constructs a Stream from the given `GenerateFunc`.
```go
func From(generate GenerateFunc) Stream
```

### `Just`
Converts the given arbitrary items to a Stream.
```go
func Just(items ...any) Stream
```

### `Range`
Converts the given channel to a Stream.
```go
func Range(source <-chan any) Stream
```

### Stream Methods

#### `AllMatch`
Returns whether all elements of this stream match the provided predicate.
```go
func (s Stream) AllMatch(predicate func(item any) bool) bool
```

#### `AnyMatch`
Returns whether any elements of this stream match the provided predicate.
```go
func (s Stream) AnyMatch(predicate func(item any) bool) bool
```

#### `Buffer`
Buffers the items into a queue with size `n`.
```go
func (s Stream) Buffer(n int) Stream
```

#### `Concat`
Returns a Stream that concatenated other streams.
```go
func (s Stream) Concat(others ...Stream) Stream
```

#### `Count`
Counts the number of elements in the result.
```go
func (s Stream) Count() (count int)
```

#### `Distinct`
Removes the duplicated items based on the given `KeyFunc`.
```go
func (s Stream) Distinct(fn KeyFunc) Stream
```

#### `Done`
Waits all upstreaming operations to be done.
```go
func (s Stream) Done()
```

#### `Filter`
Filters the items by the given `FilterFunc`.
```go
func (s Stream) Filter(fn FilterFunc, opts ...Option) Stream
```

#### `First`
Returns the first item, nil if no items.
```go
func (s Stream) First() any
```

#### `ForAll`
Handles the streaming elements from the source and no later streams.
```go
func (s Stream) ForAll(fn ForAllFunc)
```

#### `ForEach`
Seals the Stream with the `ForEachFunc` on each item, no successive operations.
```go
func (s Stream) ForEach(fn ForEachFunc)
```

#### `Group`
Groups the elements into different groups based on their keys.
```go
func (s Stream) Group(fn KeyFunc) Stream
```

#### `Head`
Returns the first `n` elements in p.
```go
func (s Stream) Head(n int64) Stream
```

#### `Last`
Returns the last item, or nil if no items.
```go
func (s Stream) Last() (item any)
```

#### `Map`
Converts each item to another corresponding item, which means it's a 1:1 model.
```go
func (s Stream) Map(fn MapFunc, opts ...Option) Stream
```

#### `Max`
Returns the maximum item from the underlying source.
```go
func (s Stream) Max(less LessFunc) any
```

#### `Merge`
Merges all the items into a slice and generates a new stream.
```go
func (s Stream) Merge() Stream
```

#### `Min`
Returns the minimum item from the underlying source.
```go
func (s Stream) Min(less LessFunc) any
```

#### `NoneMatch`
Returns whether all elements of this stream don't match the provided predicate.
```go
func (s Stream) NoneMatch(predicate func(item any) bool) bool
```

#### `Parallel`
Applies the given `ParallelFunc` to each item concurrently with given number of workers.
```go
func (s Stream) Parallel(fn ParallelFunc, opts ...Option)
```

#### `Reduce`
Is a utility method to let the caller deal with the underlying channel.
```go
func (s Stream) Reduce(fn ReduceFunc) (any, error)
```

#### `Reverse`
Reverses the elements in the stream.
```go
func (s Stream) Reverse() Stream
```

#### `Skip`
Returns a Stream that skips `n` elements.
```go
func (s Stream) Skip(n int64) Stream
```

#### `Sort`
Sorts the items from the underlying source.
```go
func (s Stream) Sort(less LessFunc) Stream
```

#### `Split`
Splits the elements into chunks with size up to `n`.
```go
func (s Stream) Split(n int) Stream
```

#### `Tail`
Returns the last `n` elements in p.
```go
func (s Stream) Tail(n int64) Stream
```

#### `Walk`
Lets the callers handle each item. The caller may write zero, one, or more items based on the given item.
```go
func (s Stream) Walk(fn WalkFunc, opts ...Option) Stream
```

## Options

### `UnlimitedWorkers`
Lets the caller use as many workers as the tasks.
```go
func UnlimitedWorkers() Option
```

### `WithWorkers`
Lets the caller customize the concurrent workers.
```go
func WithWorkers(workers int) Option
```

## Examples

Here are some examples demonstrating how to use the `fx` package for stream processing operations.

### Example 1: Creating a Stream from an Array and Filtering Elements

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

**Explanation:**

1. Use the `Just` method to convert an array to a stream.
2. Use the `Filter` method to filter out even numbers.
3. Iterate over the stream and print the results.

### Example 2: Processing Stream Elements in Parallel

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

**Explanation:**

1. Use the `Just` method to convert an array to a stream.
2. Use the `Parallel` method to process each element in parallel, specifying 3 workers.
3. Print each element being processed.

### Example 3: Sorting Elements in a Stream

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

**Explanation:**

1. Use the `Just` method to convert an array to a stream.
2. Use the `Sort` method to sort the elements.
3. Iterate over the stream and print the sorted results.

### Example 4: Reducing Elements in a Stream

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

	fmt.Println(result) // Output: 15
}
```

**Explanation:**

1. Use the `Just` method to convert an array to a stream.
2. Use the `Reduce` method to calculate the sum of all elements in the stream.
3. Print the reduction result.

### Example 5: Grouping Elements in a Stream

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
			return item.(string)[0] // Group by the first letter
		})

	for group := range stream.source {
		fmt.Println(group)
	}
}
```

**Explanation:**

1. Use the `Just` method to convert an array to a stream.
2. Use the `Group` method to group elements by their first letter.
3. Iterate over the stream and print each group.

These examples demonstrate how the `fx` package can simplify data processing through stream operations. You can combine and apply these methods according to your specific requirements in your code.