---
title: 同时输出到文件和控制台
description: 在 go-zero 中同时将日志输出到文件和控制台。
---


## 如何在 go-zero 中输出日志到文件中的同时也打印到控制台？

为了在使用 go-zero 框架时实现日志既输出到文件又打印到控制台，可以按照以下步骤进行配置和编写代码。

**步骤如下：**

1. **创建配置文件 `config.yaml`**：
   首先，定义一个 YAML 文件来配置日志输出模式和编码方式。

```yaml
Mode: file
Encoding: json
```

2. **编写主程序 `main.go`**：
   使用以下 Go 代码加载配置文件，并设置日志输出到文件和控制台。

```go
package main

import (
	"os"
	"time"

	"github.com/zeromicro/go-zero/core/conf"
	"github.com/zeromicro/go-zero/core/logx"
	"github.com/zeromicro/go-zero/core/proc"
)

func main() {
	var c logx.LogConf
	conf.MustLoad("config.yaml", &c)   // 加载配置文件
	logx.MustSetup(c)                  // 设置日志配置
	logx.AddWriter(logx.NewWriter(os.Stdout))  // 添加控制台输出

	for {
		select {
		case <-proc.Done():  // 检查程序是否需要退出
			return
		default:
			time.Sleep(time.Second)
			logx.Info(time.Now())  // 打印当前时间到日志
		}
	}
}
```

**详细说明**：

- **配置文件 (`config.yaml`)**：
    - `Mode: file` 表示将日志输出到文件。
    - `Encoding: json` 指定日志的编码格式为 JSON。

- **主程序 (`main.go`)**：
    - 使用 `conf.MustLoad` 加载配置文件。
    - 调用 `logx.MustSetup` 配置日志系统。
    - 使用 `logx.AddWriter` 方法添加额外的日志输出目标，这里我们添加了标准输出（控制台）。
    - 在无限循环中，每秒记录一次当前时间，通过 `select` 语句配合 `proc.Done()` 实现平滑退出。

通过以上配置和代码，能够实现 go-zero 同时输出日志到文件和控制台。

> go-zero 版本：>= v1.7.0