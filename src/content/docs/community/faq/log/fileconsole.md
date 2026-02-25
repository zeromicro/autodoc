---
title: Log to File and Console
description: Output logs to both file and console in go-zero.
---

# How to Output Logs to Both File and Console in go-zero?

To output logs to both a file and the console while using the go-zero framework, follow these steps to configure and write your code.

**Steps:**

1. **Create the configuration file `config.yaml`**:
   First, define a YAML file to configure the logging mode and encoding format.

```yaml
Mode: file
Encoding: json
```

2. **Write the main program `main.go`**:
   Use the following Go code to load the configuration file and set up logging to both a file and the console.

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
	conf.MustLoad("config.yaml", &c)   // Load the configuration file
	logx.MustSetup(c)                  // Set up the logging configuration
	logx.AddWriter(logx.NewWriter(os.Stdout))  // Add console output

	for {
		select {
		case <-proc.Done():  // Check if the program needs to exit
			return
		default:
			time.Sleep(time.Second)
			logx.Info(time.Now())  // Log the current time
		}
	}
}
```

**Detailed Explanation**:

- **Configuration File (`config.yaml`)**:
    - `Mode: file` specifies that logs should be output to a file.
    - `Encoding: json` specifies that the log format will be JSON.

- **Main Program (`main.go`)**:
    - Use `conf.MustLoad` to load the configuration file.
    - Call `logx.MustSetup` to configure the logging system.
    - Use `logx.AddWriter` to add an additional logging target. Here, we add standard output (console).
    - In an infinite loop, record the current time every second. The `select` statement combined with `proc.Done()` allows for smooth program termination.

By following the above configuration and code, you can achieve log output to both a file and the console in go-zero.