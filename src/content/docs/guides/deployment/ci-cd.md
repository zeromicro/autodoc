---
title: CI/CD Setup
description: Set up GitLab, Jenkins, and Harbor for go-zero service deployment pipelines.
sidebar:
  order: 14
---

Before deploying go-zero services, you need a CI/CD pipeline. This guide walks through setting up GitLab (source control), Jenkins (build & deploy), and Harbor (container registry) using Docker Compose.

## Infrastructure Overview

| Server | Purpose |
|---|---|
| `deploy-server` | GitLab, Jenkins, Harbor (requires Docker & Docker Compose) |
| `srv-data` | MySQL, Redis, Elasticsearch, etc. (data services) |
| `nginx-gateway` | API gateway, external to the cluster |
| K8s cluster | Kubernetes nodes (for K8s deployments) |

:::tip
If you use cloud-managed services (RDS, ElastiCache, etc.), you can skip the `srv-data` server.
:::

## GitLab

### Deploy with Docker Compose

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

The default admin account is `root`. Set a password on first login.

### Configure SSH Key

Add your public SSH key in **Settings → SSH Keys** so you can push code without entering a password.

## Harbor (Container Registry)

### Deploy Harbor

Download the offline installer from [Harbor releases](https://github.com/goharbor/harbor/releases):

```bash
tar -xzf harbor-offline-installer-v2.x.0.tgz
cd harbor
cp harbor.yml.tmpl harbor.yml
```

Edit `harbor.yml`:

```yaml
hostname: 192.168.1.180

http:
  port: 8077

# Comment out https section for local dev
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

Default credentials: `admin` / `Harbor12345`.

### Configure Docker Daemon

If Harbor uses HTTP (not HTTPS), configure Docker to allow insecure registries:

```json title="/etc/docker/daemon.json"
{
  "insecure-registries": ["192.168.1.180:8077"]
}
```

```bash
sudo systemctl restart docker
```

Login to verify:

```bash
docker login 192.168.1.180:8077 -u admin -p Harbor12345
```

## Jenkins

### Deploy with Docker Compose

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

### Initial Setup

1. Visit `http://<your-server>:8989`
2. Get the initial admin password: `cat jenkins_home/secrets/initialAdminPassword`
3. Install the recommended plugins
4. Create an admin user

### Install Go in Jenkins

Three options to make Go available inside the Jenkins container:

1. **Jenkins Go Plugin** — Install via **Manage Jenkins → Plugin Manager**, search for "Go", then configure under **Global Tool Configuration**
2. **Copy Go binary into container** — Download Go and `docker cp` it in:
   ```bash
   docker cp /usr/local/go jenkins:/usr/local/
   ```
3. **Bare-metal Jenkins** — Install Jenkins directly on the server and use the system Go installation

### Mount Additional Tools

For Kubernetes deployments, copy `goctl` and `kubectl` into the Jenkins container:

```bash
# goctl
docker cp $GOPATH/bin/goctl jenkins:/usr/local/bin

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
docker cp kubectl jenkins:/usr/local/bin

# K8s config
docker cp ~/.kube jenkins:/root/
```

### Add GitLab Credentials

1. **Manage Jenkins → Manage Credentials**
2. Add a credential of type **SSH Username with private key**
3. Copy the Jenkins server's public key to GitLab (Settings → SSH Keys)

## What's Next

- [Bare Metal Deployment](bare-metal.md) — Deploy directly to physical servers
- [Docker Deployment](docker.md) — Build and run with Docker
- [Kubernetes Deployment](kubernetes.md) — Deploy to a K8s cluster
