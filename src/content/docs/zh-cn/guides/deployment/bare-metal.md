---
title: 物理机部署
description: 使用 Jenkins CI/CD 将 go-zero 服务部署到物理服务器。
sidebar:
  order: 17
---

本指南介绍如何将 go-zero 服务直接部署到物理服务器上，使用 `nohup` 作为后台守护进程，由 Jenkins 负责构建和部署流水线。

:::tip
其他守护进程方案包括 `systemd` 和 `supervisor`，只需配置一个配置文件即可，部署流水线不变。
:::

## 前置条件

- 已安装 Go 的 Jenkins 服务器（参见 [CI/CD 环境搭建](ci-cd.md)）
- GitLab 中已有项目仓库
- 目标部署服务器可通过 SSH 从 Jenkins 访问

## 第一步：创建示例服务

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

生成并构建项目：

```bash
cd apicode && goctl api go -api *.api -dir ./
go mod tidy
```

在 `hellologic.go` 中添加逻辑：

```go
func (l *HelloLogic) Hello(req *types.HelloReq) (resp *types.HelloResp, err error) {
    return &types.HelloResp{
        Msg: "hello->" + req.Msg,
    }, nil
}
```

本地验证：

```bash
go run apicode.go
# 访问 http://127.0.0.1:8888/hello?msg=world
```

将代码推送到 GitLab。

## 第二步：配置 SSH 密钥

Jenkins 需要通过 SSH 访问 GitLab（拉取代码）和目标服务器（部署）：

```bash
# 在 Jenkins 服务器上查看公钥
cat /root/.ssh/id_rsa.pub
```

将此公钥添加到：

1. **GitLab** — 设置 → SSH Keys（用于代码检出）
2. **目标服务器** — 追加到 `/root/.ssh/authorized_keys`（用于 `scp` 部署）

## 第三步：创建 Jenkins Pipeline

1. 在 Jenkins 中点击 **新建 Item** → 输入名称 `apicode` → 选择 **流水线** → 确定
2. 在 **General** 中勾选 **参数化构建过程** → **添加参数** → **Git Parameter**
   - 名称：`branch`
   - 参数类型：Branch
   - 默认值：`master`

3. 在 **流水线** 部分输入脚本：

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
        description: '选择需要构建的分支'
    }

    stages {
        stage('服务信息') {
            steps {
                sh 'echo 分支: $branch'
            }
        }

        stage('拉取代码') {
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

        stage('构建') {
            steps {
                sh '/usr/local/go/bin/go build -o apicode apicode.go'
                sh 'mkdir -p deploy && cp -r ./etc ./apicode deploy'
                sh 'tar -zcvf deploy.tar.gz deploy'
            }
        }

        stage('部署') {
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
请将 `your-gitlab` 和 `your-target-server` 替换为你实际的主机名或 IP 地址。
:::

## 第四步：构建与部署

1. 在 Jenkins 中打开 `apicode` 流水线
2. 点击 **Build with Parameters**
3. 选择分支并点击 **Build**

流水线完成后验证部署：

```bash
curl "http://your-target-server:8888/hello?msg=world"
# {"msg":"hello->world"}
```

## 进程管理替代方案

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

## 下一步

- [Docker 部署](docker.md) — 容器化部署
- [Kubernetes 部署](kubernetes.md) — 集群化大规模部署
