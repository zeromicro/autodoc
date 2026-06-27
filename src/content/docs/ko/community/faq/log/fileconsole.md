---
title: 파일과 콘솔에 로그 출력
description: go-zero에서 로그를 파일과 콘솔에 동시에 출력하는 방법입니다.
sidebar:
  order: 2
---


go-zero 프레임워크를 사용하면서 로그를 파일과 콘솔에 동시에 출력하려면 다음 단계로 설정하고 코드를 작성합니다.

**단계:**

1. **설정 파일 `config.yaml` 생성**

   먼저 로깅 모드와 인코딩 형식을 설정하는 YAML 파일을 정의합니다.

```yaml
Mode: file
Encoding: json
```

2. **메인 프로그램 `main.go` 작성**

   다음 Go 코드는 설정 파일을 로드하고 로그를 파일과 콘솔 양쪽으로 출력하도록 설정합니다.

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
	conf.MustLoad("config.yaml", &c)   // 설정 파일을 로드합니다
	logx.MustSetup(c)                  // 로깅 설정을 초기화합니다
	logx.AddWriter(logx.NewWriter(os.Stdout))  // 콘솔 출력을 추가합니다

	for {
		select {
		case <-proc.Done():  // 프로그램 종료가 필요한지 확인합니다
			return
		default:
			time.Sleep(time.Second)
			logx.Info(time.Now())  // 현재 시간을 로그로 남깁니다
		}
	}
}
```

**자세한 설명:**

- **설정 파일(`config.yaml`)**
  - `Mode: file`은 로그를 파일로 출력한다는 뜻입니다.
  - `Encoding: json`은 로그 형식을 JSON으로 사용한다는 뜻입니다.

- **메인 프로그램(`main.go`)**
  - `conf.MustLoad`로 설정 파일을 로드합니다.
  - `logx.MustSetup`을 호출해 로깅 시스템을 설정합니다.
  - `logx.AddWriter`로 추가 출력 대상을 등록합니다. 여기서는 표준 출력(console)을 추가합니다.
  - 무한 루프에서 1초마다 현재 시간을 기록합니다. `select`와 `proc.Done()`을 함께 사용하면 프로그램을 부드럽게 종료할 수 있습니다.

위 설정과 코드를 사용하면 go-zero에서 로그를 파일과 콘솔에 동시에 출력할 수 있습니다.
