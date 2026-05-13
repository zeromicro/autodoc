---
title: CI/CD 설정
description: go-zero 서비스 배포 파이프라인을 위해 GitLab, Jenkins, Harbor를 설정하는 방법입니다.
sidebar:
  order: 14
---


go-zero 서비스를 배포하기 전에 CI/CD 파이프라인이 필요합니다. 이 가이드는 Docker Compose를 사용해 GitLab(source control), Jenkins(build & deploy), Harbor(container registry)를 설정하는 과정을 설명합니다.

## 인프라 개요

| 서버 | 목적 |
|---|---|
| `deploy-server` | GitLab, Jenkins, Harbor(Docker와 Docker Compose 필요) |
| `srv-data` | MySQL, Redis, Elasticsearch 등 데이터 서비스 |
| `nginx-gateway` | 클러스터 외부의 API gateway |
| K8s cluster | Kubernetes node(K8s 배포용) |

:::tip
RDS, ElastiCache 같은 cloud-managed service를 사용한다면 `srv-data` 서버는 생략할 수 있습니다.
:::

## GitLab

### Docker Compose로 배포

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

기본 admin 계정은 `root`입니다. 처음 로그인할 때 비밀번호를 설정하세요.

### SSH key 설정

비밀번호를 입력하지 않고 code를 push할 수 있도록 **Settings → SSH Keys**에서 public SSH key를 추가합니다.

## Harbor(Container Registry)

### Harbor 배포

[Harbor releases](https://github.com/goharbor/harbor/releases)에서 offline installer를 다운로드합니다.

```bash
tar -xzf harbor-offline-installer-v2.x.0.tgz
cd harbor
cp harbor.yml.tmpl harbor.yml
```

`harbor.yml`을 수정합니다.

```yaml
hostname: 192.168.1.180

http:
  port: 8077

# local dev에서는 https section을 주석 처리합니다
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

기본 credential은 `admin` / `Harbor12345`입니다.

### Docker daemon 설정

Harbor가 HTTPS가 아니라 HTTP를 사용한다면 Docker에서 insecure registry를 허용하도록 설정합니다.

```json title="/etc/docker/daemon.json"
{
  "insecure-registries": ["192.168.1.180:8077"]
}
```

```bash
sudo systemctl restart docker
```

로그인해 설정을 확인합니다.

```bash
docker login 192.168.1.180:8077 -u admin -p Harbor12345
```

## Jenkins

### Docker Compose로 배포

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

### 초기 설정

1. `http://<your-server>:8989`에 접속합니다.
2. 초기 admin 비밀번호를 확인합니다. `cat jenkins_home/secrets/initialAdminPassword`
3. 권장 plugin을 설치합니다.
4. admin user를 생성합니다.

### Jenkins에 Go 설치

Jenkins container 안에서 Go를 사용할 수 있게 하는 방법은 세 가지입니다.

1. **Jenkins Go Plugin** — **Manage Jenkins → Plugin Manager**에서 “Go”를 검색해 설치한 뒤 **Global Tool Configuration**에서 설정합니다.
2. **Go binary를 container에 복사** — Go를 다운로드한 뒤 `docker cp`로 복사합니다.
   ```bash
   docker cp /usr/local/go jenkins:/usr/local/
   ```
3. **Bare-metal Jenkins** — Jenkins를 서버에 직접 설치하고 system Go 설치를 사용합니다.

### 추가 도구 마운트

Kubernetes 배포에는 `goctl`과 `kubectl`을 Jenkins container에 복사합니다.

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

### GitLab credential 추가

1. **Manage Jenkins → Manage Credentials**로 이동합니다.
2. **SSH Username with private key** 타입의 credential을 추가합니다.
3. Jenkins 서버의 public key를 GitLab에 복사합니다(Settings → SSH Keys).

## 다음 단계

- [베어메탈 배포](bare-metal.md) — 물리 서버에 직접 배포
- [Docker 배포](docker.md) — Docker로 build하고 실행
- [Kubernetes 배포](kubernetes.md) — K8s cluster에 배포
