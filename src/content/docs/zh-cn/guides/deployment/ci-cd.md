---
title: CI/CD 环境搭建
description: 搭建 GitLab、Jenkins 和 Harbor，为 go-zero 服务部署构建流水线。
sidebar:
  order: 14
---

在部署 go-zero 服务之前，需要搭建 CI/CD 流水线。本指南介绍如何使用 Docker Compose 搭建 GitLab（代码管理）、Jenkins（构建与部署）和 Harbor（容器镜像仓库）。

## 基础设施概览

| 服务器 | 用途 |
|---|---|
| `deploy-server` | 部署 GitLab、Jenkins、Harbor（需预装 Docker 和 Docker Compose） |
| `srv-data` | 部署 MySQL、Redis、Elasticsearch 等数据服务 |
| `nginx-gateway` | API 网关，独立于集群外部 |
| K8s 集群 | Kubernetes 节点（用于 K8s 部署） |

:::tip
如果使用云托管服务（RDS、ElastiCache 等），可以跳过 `srv-data` 服务器。
:::

## GitLab

### 使用 Docker Compose 部署

```bash
mkdir gitlab && cd gitlab
```

```yaml title="docker-compose.yml"
version: "3"

services:
  gitlab:
    image: "gitlab/gitlab-ce:latest"
    container_name: "gitlab"
    restart: always
    hostname: "192.168.1.180"
    environment:
      TZ: "Asia/Shanghai"
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://192.168.1.180'
        gitlab_rails['gitlab_shell_ssh_port'] = 2222
        unicorn['port'] = 8888
    ports:
      - "80:80"
      - "2222:22"
    volumes:
      - ./etc:/etc/gitlab
      - ./data:/var/opt/gitlab
      - ./logs:/var/log/gitlab
```

```bash
docker-compose up -d
```

默认管理员账号为 `root`，首次登录时设置密码。

### 配置 SSH 公钥

在 **设置 → SSH Keys** 中添加你的 SSH 公钥，以便免密推送代码。

## Harbor（容器镜像仓库）

### 部署 Harbor

从 [Harbor releases](https://github.com/goharbor/harbor/releases) 下载离线安装包：

```bash
tar -xzf harbor-offline-installer-v2.x.0.tgz
cd harbor
cp harbor.yml.tmpl harbor.yml
```

编辑 `harbor.yml`：

```yaml
hostname: 192.168.1.180

http:
  port: 8077

# 本地开发暂时注释掉 https
#https:
#  port: 443
#  certificate: /your/certificate/path
#  private_key: /your/private/key/path

data_volume: /root/harbor/data

log:
  level: info
  local:
    rotate_count: 50
    rotate_size: 200M
    location: /root/harbor/log
```

```bash
sudo ./install.sh
```

默认账号：`admin` / `Harbor12345`。

### 配置 Docker Daemon

如果 Harbor 使用 HTTP（非 HTTPS），需要配置 Docker 允许不安全的镜像仓库：

```json title="/etc/docker/daemon.json"
{
  "insecure-registries": ["192.168.1.180:8077"]
}
```

```bash
sudo systemctl restart docker
```

验证登录：

```bash
docker login 192.168.1.180:8077 -u admin -p Harbor12345
```

## Jenkins

### 使用 Docker Compose 部署

```bash
mkdir jenkins && cd jenkins
```

```yaml title="docker-compose.yml"
version: "3"
services:
  jenkins:
    image: "jenkins/jenkins:lts"
    container_name: jenkins
    restart: always
    environment:
      - TZ=Asia/Shanghai
    user: root
    ports:
      - "8989:8080"
      - "50000:50000"
    volumes:
      - "./jenkins_home:/var/jenkins_home"
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "/usr/bin/docker:/usr/bin/docker"
```

```bash
docker-compose up -d
```

### 初始设置

1. 访问 `http://<your-server>:8989`
2. 获取初始管理员密码：`cat jenkins_home/secrets/initialAdminPassword`
3. 安装推荐插件
4. 创建管理员用户

### 在 Jenkins 中安装 Go

有三种方式让 Go 在 Jenkins 容器中可用：

1. **Jenkins Go 插件** — 通过 **系统管理 → 插件管理** 搜索 "Go" 安装，然后在 **全局工具配置** 中配置
2. **复制 Go 到容器** — 下载 Go 后使用 `docker cp` 复制：
   ```bash
   docker cp /usr/local/go jenkins:/usr/local/
   ```
3. **裸机安装 Jenkins** — 直接在服务器上安装 Jenkins，使用系统已有的 Go 环境

### 挂载其他工具

对于 Kubernetes 部署，将 `goctl` 和 `kubectl` 复制到 Jenkins 容器中：

```bash
# goctl
docker cp $GOPATH/bin/goctl jenkins:/usr/local/bin

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
docker cp kubectl jenkins:/usr/local/bin

# K8s 配置
docker cp ~/.kube jenkins:/root/
```

### 添加 GitLab 凭据

1. **系统管理 → 凭据管理**
2. 添加类型为 **SSH Username with private key** 的凭据
3. 将 Jenkins 服务器的公钥添加到 GitLab（设置 → SSH Keys）

## 下一步

- [物理机部署](bare-metal.md) — 直接部署到物理服务器
- [Docker 部署](docker.md) — 使用 Docker 构建和运行
- [Kubernetes 部署](kubernetes.md) — 部署到 K8s 集群
