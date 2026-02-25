---
title: FX Pipeline
description: 使用 go-zero FX 流式工具构建数据管道。
sidebar:
  order: 2

---


# fx

## 概述

`fx` 包提供了一系列用于流处理的函数和类型。流（Stream）是一个可以使用这些方法进行处理的数据集合。

### 函数类型

- `FilterFunc`: 定义了过滤流元素的方法。
- `ForAllFunc`: 定义了处理所有流元素的方法。
- `ForEachFunc`: 定义了处理每个流元素的方法。
- `GenerateFunc`: 定义了向流中发送元素的方法。
- `KeyFunc`: 定义了生成流元素键值的方法。
- `LessFunc`: 定义了比较流元素的方法。
- `MapFunc`: 定义了将每个流元素映射到另一个对象的方法。
- `Option`: 定义了自定义流的方法。
- `ParallelFunc`: 定义了并行处理元素的方法。
- `ReduceFunc`: 定义了归约流元素的方法。
- `WalkFunc`: 定义了遍历所有流元素的方法。

### Stream

```go
type Stream struct {
    source <-chan any // 流数据源
}
```

## 功能函数

### 创建流

- `Concat(s Stream, others ...Stream) Stream`: 返回连接其他流的流。
- `From(generate GenerateFunc) Stream`: 从给定的生成函数构造一个流。
- `Just(items ...any) Stream`: 将给定的任意项目转换为流。
- `Range(source <-chan any) Stream`: 将给定的通道转换为流。

### 流操作

- `AllMatch(predicate func(item any) bool) bool`: 返回流的所有元素是否满足提供的判断函数。
- `AnyMatch(predicate func(item any) bool) bool`: 返回流的任何元素是否满足提供的判断函数。
- `Buffer(n int) Stream`: 将项目缓冲到大小为n的队列中。
- `Count() (count int)`: 计算结果中的元素数量。
- `Distinct(fn KeyFunc) Stream`: 根据给定的 `KeyFunc` 删除重复项。
- `Done()`: 等待所有上游操作完成。
- `Filter(fn FilterFunc, opts ...Option) Stream`: 根据给定的 `FilterFunc` 过滤项目。
- `First() any`: 返回第一个项目，如果没有项目则返回 nil。
- `ForAll(fn ForAllFunc)`: 处理源中的流元素，并且没有后续的流操作。
- `ForEach(fn ForEachFunc)`: 使用 `ForEachFunc` 处理每个项目，没有后续操作。
- `Group(fn KeyFunc) Stream`: 根据键将元素分组。
- `Head(n int64) Stream`: 返回前 n 个元素。
- `Last() (item any)`: 返回最后一个项目，如果没有项目则返回 nil。
- `Map(fn MapFunc, opts ...Option) Stream`: 将每个项目映射到另一个相应的项目。
- `Max(less LessFunc) any`: 返回源中的最大项目。
- `Merge() Stream`: 将所有项目合并到一个切片中并生成一个新的流。
- `Min(less LessFunc) any`: 返回源中的最小项目。
- `NoneMatch(predicate func(item any) bool) bool`: 返回流的所有元素不满足提供的谓词。
- `Parallel(fn ParallelFunc, opts ...Option)`: 并行应用给定的 `ParallelFunc` 到每个项目。
- `Reduce(fn ReduceFunc) (any, error)`: 一个实用方法，用于处理底层通道。
- `Reverse() Stream`: 反转流中的元素。
- `Skip(n int64) Stream`: 返回跳过前 n 个元素后的流。
- `Sort(less LessFunc) Stream`: 对底层源中的项目进行排序。
- `Split(n int) Stream`: 将元素拆分为大小最多为 n 的块。
- `Tail(n int64) Stream`: 返回最后 n 个元素。
- `Walk(fn WalkFunc, opts ...Option) Stream`: 让调用者处理每个项目，调用者可以根据给定的项目写入零个、一个或多个项目。

### 配置选项

- `UnlimitedWorkers() Option`: 允许调用者使用与任务一样多的工作线程。
- `WithWorkers(workers int) Option`: 允许调用者自定义并发工作线程数。

## 使用示例

以下是一些使用 `fx` 包的示例，展示了如何进行流处理操作。

### 示例 1: 从数组创建流并过滤元素

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

**解释：**

1. 使用 `Just` 方法将数组转换为流。
2. 使用 `Filter` 过滤出偶数元素。
3. 遍历流并打印结果。

### 示例 2: 并行处理流中的元素

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

**解释：**

1. 使用 `Just` 方法将数组转换为流。
2. 使用 `Parallel` 方法并行处理每个元素，指定使用 3 个工作线程。
3. 打印正在处理的每个元素。

### 示例 3: 对流中的元素进行排序

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

**解释：**

1. 使用 `Just` 方法将数组转换为流。
2. 使用 `Sort` 方法对元素进行排序。
3. 遍历流并打印排序后的结果。

### 示例 4: 归约流中的元素

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

	fmt.Println(result) // 输出：15
}
```

**解释：**

1. 使用 `Just` 方法将数组转换为流。
2. 使用 `Reduce` 方法计算流中所有元素的总和。
3. 打印归约结果。

### 示例 5: 分组流中的元素

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
			return item.(string)[0] // 按首字母分组
		})

	for group := range stream.source {
		fmt.Println(group)
	}
}
```

**解释：**

1. 使用 `Just` 方法将数组转换为流。
2. 使用 `Group` 方法按首字母对元素进行分组。
3. 遍历流并打印每个分组。

这些示例展示了 `fx` 包如何通过流操作简化数据处理。可以根据实际需求在代码中组合和应用这些方法。