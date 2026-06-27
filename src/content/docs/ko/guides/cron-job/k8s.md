---
title: Cron 작업 에서 Kubernetes
description: go-zero의 Cron 작업 에서 Kubernetes에 대해 설명합니다.
sidebar:
  order: 2
---

## 개요


## 2. 프로젝트 address

프로젝트 address：https://github.com/Mikaelemmm/zerok8scron


## 3. Key code analysis

```go title="main.go"
package main

import (
    "zerok8scron/internal/cmd"
)

func main() {
    cmd.Execute()
}
```

```go title="internal/cmd/root.go"
package cmd

import (
    "github.com/spf13/cobra"
    "github.com/zeromicro/go-zero/core/conf"
    "os"
    "zerok8scron/internal/config"
    "zerok8scron/internal/logic"
    "zerok8scron/internal/svc"
)

const (
    codeFailure = 1
)

var (
    confPath string

    rootCmd = &cobra.명령{
        Use:   "cron",
        Short: "exec cron job",
        Long:  "exec cron job",
    }

// all job ...
    helloJob = &cobra.명령{
        Use:   "hello",
        Short: "print 'hello SvcName' once per minute",
        RunE:  logic.Hello,
    }

    // 추가합니다
)

// Execute는 주어진 명령을 실행합니다
func Execute() {
    if err := rootCmd.Execute(); err != nil {
        os.Exit(codeFailure)
    }
}

func init() {

    // 예시입니다
    cobra.OnInitialize(initConfig)
    rootCmd.PersistentFlags().StringVar(&confPath, "config", "etc/cron.yaml", "config file (default is $HOME/.cobra.yaml)")

    // add subcommand
    rootCmd.Add명령(helloJob)
}

func initConfig() {
    var c config.Config
    conf.MustLoad(confPath, &c)
    svc.InitSvcCtx(c)
}

```

```go title="internal/logic/hello.go"
package logic

import (
    "fmt"
    "github.com/spf13/cobra"
    "zerok8scron/internal/svc"
)

// Hello는 1분마다 "hello SvcName"을 출력합니다
func Hello(_ *cobra.명령, _ []string) error {

    fmt.Printf("srvName : %s , hello \n", svc.GetSvcCtx().Config.Name)

    return nil
}
```

### 3.1 Implementation schedule


이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

### 3.2 어떻게 initialize 설정


다음 패키지를 사용합니다: 기본값 profile 로서 etc/cron.yaml

## 4. Operational schedule

### 4.1 로컬 execution once

```sh
$ go run main.go hello
```

### 4.2 Executed once 에서 Docker

```sh
$ goctl docker -go main.go #创建dockerfile，如果你用上面的项目，项目中已经创建好可以省略
$ docker build -t zerok8scron:v1 . # 构建镜像，如果你用上面的项目，项目中已经创建好可以省略
$ docker run zerok8scron:v1 hello #运行即可
```

### 4.3 k8s 사용하여 cronjob scheduling once minute

```yaml title="cronjob.yaml"
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: hello
              image: zerok8scron:v1
              args:
                - hello
          restartPolicy: OnFailure
```

실행

```shell
$ kubectl apply -f cronjob.yaml
```

Then you can view cronjob 상태과 출력

![deploy-server-deploy](/resource/tasks/timer-task/k8scronjob.png)
