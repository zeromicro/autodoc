---
title: goctl Kubernetes
description: go-zero의 goctl Kubernetes에 대해 설명합니다.
sidebar:
  order: 8

---

## 개요


- How should CPU과 메모리 requests/limits be set?
- How should 서비스 be exposed 로 other callers?


## goctl Kube directive

```bash
$ goctl kube --help
Generate kubernetes files

Usage:
  goctl kube [command]

Available 명령s:
  deploy      Generate deployment yaml file

Flags:
  -h, --help   help for kube


Use "goctl kube [command] --help" for more information about a command.
```

goctl kube currently 지원합니다 generating 배포 YAML 파일.

### goctl kube 배포 directive

```bash
$ goctl kube deploy --help
Generate deployment yaml file

Usage:
  goctl kube deploy [flags]

Flags:
      --branch string            The branch of the remote repo, it does work with --remote
  -h, --help                     help for deploy
      --home string              The goctl home path of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
      --image string             The docker image of deployment (required)
      --imagePullPolicy string   Image pull policy. One of Always, Never, IfNotPresent
      --limitCpu int             The limit cpu to deploy (default 1000)
      --limitMem int             The limit memory to deploy (default 1024)
      --maxReplicas int          The max replicas to deploy (default 10)
      --minReplicas int          The min replicas to deploy (default 3)
      --name string              The name of deployment (required)
      --namespace string         The namespace of deployment (required)
      --nodePort int             The nodePort of the deployment to expose
      --o string                 The output yaml file (required)
      --port int                 The port of the deployment to listen on pod (required)
      --remote string            The remote git repo of the template, --home and --remote cannot be set at the same time, if they are, --remote has higher priority
                                 The git repo directory must be consistent with the https://github.com/zeromicro/go-zero-template directory structure
      --replicas int             The number of replicas to deploy (default 3)
      --requestCpu int           The request cpu to deploy (default 500)
      --requestMem int           The request memory to deploy (default 512)
      --revisions int            The number of revision history to limit (default 5)
      --secret string            The secret to image pull from registry
      --serviceAccount string    The ServiceAccount for the deployment
      --targetPort int           The targetPort of the deployment, default to port
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명                                                        |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| branch                                               | string                                              | 없음                                             | Empty string                                       | 원격 템플릿 name is 사용됨 만 경우 `remote` has value                                                           |
| home                                                 | string                                              | 없음                                             | `${HOME}/.goctl`                                   | 로컬 템플릿 파일 디렉터리                                                                                     |
| image                                                | string                                              | YES                                            | Empty string                                       | Image name                                                                                                        |
| imagePullPolicy                                      | string                                              | YES                                            | Empty string                                       | Image Pull policy, Always: Always Pull, Never: Never Pull, IfNotPresent: Pull 때 it does 아님 exist              |
| limitCpu                                             | int                                                 | 없음                                             | `1000`                                             | cpu resource usage 제한                                                                                          |
| limitMem                                             | int                                                 | 없음                                             | `1024`                                             | Maximum 메모리 usage                                                                                              |
| maxReplicas                                          | int                                                 | 없음                                             | `10`                                               | Maximum number 의 replicas                                                                                        |
| minReplicas                                          | int                                                 | 없음                                             | `3`                                                | Minimum number 의 replicas                                                                                        |
| name                                                 | string                                              | YES                                            | Empty string                                       | Deployment name                                                                                                     |
| namespace                                            | string                                              | YES                                            | Empty string                                       | Kubernetes namespace                                                                                              |
| nodePort                                             | int                                                 | YES                                            | 0                                                  | Service 포트 로 be exposed                                                                                        |
| o                                                    | string                                              | YES                                            | Empty string                                       | yaml 파일 name                                                                                                    |
| 포트                                                 | int                                                 | YES                                            | 0                                                  | 포트 로 listen                                                                                                    |
| 원격                                               | string                                              | 없음                                             | Empty string                                       |해당 항목의 동작과 사용법을 설명합니다. |
| replicas                                             | int                                                 | 없음                                             | `3`                                                | Number 의 replicas                                                                                                |
| requestCpu                                           | int                                                 | 없음                                             | `500`                                              | cpu 제한                                                                                                         |
| requestMem                                           | int                                                 | 없음                                             | `512`                                              | 메모리 제한                                                                                                      |
| revisions                                            | int                                                 | 없음                                             | `1`                                                | Number 의 reserved 버전, easy 로 roll back                                                                    |
| secret                                               | string                                              | 없음                                             | Empty string                                       | 레지스트리 image Pull secret                                                                                        |
| serviceAccount                                       | string                                              | 없음                                             | Empty string                                       | Service account                                                                                                   |
| targetPort                                           | int                                                 | 없음                                             | 0                                                  | Target 포트                                                                                                       |

## 예제

사용하여 Redis image 로서 예제, here은 how 로 생성 배포 YAML 파일 사용하여 `goctl kube deploy`입니다.

```bash
$ goctl kube deploy -name redis -namespace adhoc -image redis:6-alpine -o redis.yaml -port 6379
Done.
```


```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: adhoc
  labels:
    app: redis
spec:
  replicas: 3
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:6-alpine
        ports:
        - containerPort: 6379
        readinessProbe:
          tcpSocket:
            port: 6379
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          tcpSocket:
            port: 6379
          initialDelaySeconds: 15
          periodSeconds: 20
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1024Mi
        volumeMounts:
        - name: timezone
          mountPath: /etc/localtime
      volumes:
        - name: timezone
          hostPath:
            path: /usr/share/zoneinfo/Asia/Shanghai

---

apiVersion: v1
kind: Service
metadata:
  name: redis-svc
  namespace: adhoc
spec:
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: redis

---

apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: redis-hpa-c
  namespace: adhoc
  labels:
    app: redis-hpa-c
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: redis
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      targetAverageUtilization: 80

---

apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: redis-hpa-m
  namespace: adhoc
  labels:
    app: redis-hpa-m
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: redis
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: memory
      targetAverageUtilization: 80
```
