---
title: 베어메탈 배포
description: Jenkins CI/CD를 사용해 go-zero 서비스를 물리 서버에 배포하는 방법입니다.
sidebar:
  order: 17
---

이 가이드는 `nohup`을 process daemon으로 사용해 go-zero 서비스를 물리 서버에 직접 배포하는 방법을 설명합니다. Jenkins는 build와 deployment pipeline을 처리합니다.

:::tip
다른 daemon 옵션으로는 `systemd`와 `supervisor`가 있습니다. 이들은 설정 파일만 다를 뿐, 배포 파이프라인은 동일하게 유지됩니다.
:::

## 사전 준비

- Go가 설치된 Jenkins 서버([CI/CD 설정](ci-cd.md) 참고)
- 프로젝트 repository가 있는 GitLab
- Jenkins에서 SSH로 접근할 수 있는 target 배포 서버

## 1단계: demo 서비스 만들기

```text title="apicode.api"
syntax = "v1"

info(
    title: "deploy demo"
    desc: "deployment example"
    author: "go-zero"
)

type (
    HelloReq {
        Msg string `form:"msg"`
    }
    HelloResp {
        Msg string `json:"msg"`
    }
)

service apicode {
    @doc "hello"
    @handler hello
    get /hello(HelloReq) returns(HelloResp)
}
```

프로젝트 코드를 생성하고 build 준비를 합니다.

```bash
cd apicode && goctl api go -api *.api -dir ./
go mod tidy
```

`hellologic.go`에 로직을 추가합니다.

```go
func (l *HelloLogic) Hello(req *types.HelloReq) (resp *types.HelloResp, err error) {
    return &types.HelloResp{
        Msg: "hello->" + req.Msg,
    }, nil
}
```

로컬에서 확인합니다.

```bash
go run apicode.go
# http://127.0.0.1:8888/hello?msg=world 에 접속합니다
```

코드를 GitLab에 push합니다.

## 2단계: SSH key 설정

Jenkins는 GitLab에서 code를 pull하고 target server에 배포해야 하므로 두 곳 모두에 SSH 접근 권한이 필요합니다.

```bash
# Jenkins 서버에서 public key를 복사합니다
cat /root/.ssh/id_rsa.pub
```

이 key를 다음 위치에 추가합니다.

1. **GitLab** — Settings → SSH Keys(code checkout용)
2. **Target server** — `/root/.ssh/authorized_keys`에 추가(`scp` 배포용)

## 3단계: Jenkins pipeline 만들기

1. Jenkins에서 **New Item**을 클릭하고 이름을 `apicode`로 지정한 뒤 **Pipeline**을 선택하고 OK를 클릭합니다.
2. **일반** 섹션에서 **이 프로젝트는 매개변수를 사용함**을 체크하고 **매개변수 추가** → **Git 매개변수**를 선택합니다.
   - Name: `branch`
   - Parameter Type: Branch
   - Default: `master`

3. **Pipeline** section에 다음 script를 입력합니다.

```groovy
pipeline {
    agent any

    parameters {
        gitParameter name: 'branch',
        type: 'PT_BRANCH',
        branchFilter: 'origin/(.*)',
        defaultValue: 'master',
        selectedValue: 'DEFAULT',
        sortMode: 'ASCENDING_SMART',
        description: 'Select branch to build'
    }

    stages {
        stage('Info') {
            steps {
                sh 'echo Branch: $branch'
            }
        }

        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '$branch']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    submoduleCfg: [],
                    userRemoteConfigs: [[
                        credentialsId: 'gitlab-cert',
                        url: 'ssh://git@your-gitlab:2222/root/apicode.git'
                    ]]
                ])
            }
        }

        stage('Build') {
            steps {
                sh '/usr/local/go/bin/go build -o apicode apicode.go'
                sh 'mkdir -p deploy && cp -r ./etc ./apicode deploy'
                sh 'tar -zcvf deploy.tar.gz deploy'
            }
        }

        stage('Deploy') {
            steps {
                sh 'scp ./deploy.tar.gz root@your-target-server:/root/'
                sh 'ssh root@your-target-server "tar -xvf /root/deploy.tar.gz -C /root/"'
                sh 'ssh root@your-target-server "nohup /root/deploy/apicode -f /root/deploy/etc/apicode.yaml > /root/deploy/stdout.log 2> /root/deploy/stderr.log &"'
            }
        }
    }
}
```

:::caution
`your-gitlab`과 `your-target-server`를 실제 hostname 또는 IP 주소로 바꾸세요.
:::

## 4단계: build 및 배포

1. Jenkins에서 `apicode` pipeline을 엽니다.
2. **Build with Parameters**를 클릭합니다.
3. branch를 선택하고 **Build**를 클릭합니다.

pipeline이 완료되면 배포를 확인합니다.

```bash
curl "http://your-target-server:8888/hello?msg=world"
# {"msg":"hello->world"}
```

## process 관리 대안

### systemd

```ini title="/etc/systemd/system/apicode.service"
[Unit]
Description=apicode service
After=network.target

[Service]
Type=simple
ExecStart=/root/deploy/apicode -f /root/deploy/etc/apicode.yaml
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable apicode
sudo systemctl start apicode
```

### supervisor

```ini title="/etc/supervisor/conf.d/apicode.conf"
[program:apicode]
command=/root/deploy/apicode -f /root/deploy/etc/apicode.yaml
autostart=true
autorestart=true
stdout_logfile=/var/log/apicode.stdout.log
stderr_logfile=/var/log/apicode.stderr.log
```

```bash
sudo supervisorctl update
sudo supervisorctl start apicode
```

## 다음 단계

- [Docker 배포](docker.md) — container 기반 배포
- [Kubernetes 배포](kubernetes.md) — 대규모 orchestrated 배포
