---
title: Bare Metal Deployment
description: Deploy go-zero services to physical servers using Jenkins CI/CD.
sidebar:
  order: 17
---

This guide shows how to deploy a go-zero service directly on a physical server using `nohup` as a process daemon, with Jenkins handling the build and deployment pipeline.

:::tip
Other daemon options include `systemd` and `supervisor`. They only require a configuration file — the deployment pipeline remains the same.
:::

## Prerequisites

- A Jenkins server with Go installed (see [CI/CD Setup](ci-cd.md))
- GitLab with your project repository
- A target deployment server accessible via SSH from Jenkins

## Step 1: Create a Demo Service

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

Generate and build the project:

```bash
cd apicode && goctl api go -api *.api -dir ./
go mod tidy
```

Add the logic in `hellologic.go`:

```go
func (l *HelloLogic) Hello(req *types.HelloReq) (resp *types.HelloResp, err error) {
    return &types.HelloResp{
        Msg: "hello->" + req.Msg,
    }, nil
}
```

Verify locally:

```bash
go run apicode.go
# Visit http://127.0.0.1:8888/hello?msg=world
```

Push the code to GitLab.

## Step 2: Configure SSH Keys

Jenkins needs SSH access to both GitLab (to pull code) and the target server (to deploy):

```bash
# On the Jenkins server — copy its public key
cat /root/.ssh/id_rsa.pub
```

Add this key to:

1. **GitLab** — Settings → SSH Keys (for code checkout)
2. **Target server** — Append to `/root/.ssh/authorized_keys` (for deployment via `scp`)

## Step 3: Create Jenkins Pipeline

1. In Jenkins, click **New Item** → name it `apicode` → select **Pipeline** → OK
2. Under **General**, check **This project is parameterized** → **Add Parameter** → **Git Parameter**
   - Name: `branch`
   - Parameter Type: Branch
   - Default: `master`

3. In the **Pipeline** section, enter the script:

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
Replace `your-gitlab` and `your-target-server` with your actual hostnames or IP addresses.
:::

## Step 4: Build & Deploy

1. Open the `apicode` pipeline in Jenkins
2. Click **Build with Parameters**
3. Select the branch and click **Build**

Once the pipeline completes, verify the deployment:

```bash
curl "http://your-target-server:8888/hello?msg=world"
# {"msg":"hello->world"}
```

## Process Management Alternatives

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

## What's Next

- [Docker Deployment](docker.md) — Containerized deployment
- [Kubernetes Deployment](kubernetes.md) — Orchestrated deployment at scale
