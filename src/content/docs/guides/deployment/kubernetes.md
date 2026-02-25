---
title: Kubernetes
description: Deploy go-zero microservices to Kubernetes.
sidebar:
  order: 2
---


go-zero services run well on Kubernetes with minimal configuration.

## Deployment

```yaml title="k8s/deployment.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-api
spec:
  replicas: 3
  selector:
    matchLabels: {app: order-api}
  template:
    metadata:
      labels: {app: order-api}
    spec:
      containers:
        - name: order-api
          image: myregistry/order-api:latest
          ports:
            - containerPort: 8888
          resources:
            requests: {cpu: 100m, memory: 128Mi}
            limits:   {cpu: 500m, memory: 256Mi}
          livenessProbe:
            httpGet: {path: /healthz, port: 8888}
            initialDelaySeconds: 10
          readinessProbe:
            httpGet: {path: /healthz, port: 8888}
            initialDelaySeconds: 5
```

## Service

```yaml title="k8s/service.yaml"
apiVersion: v1
kind: Service
metadata:
  name: order-api-svc
spec:
  selector: {app: order-api}
  ports: [{port: 8888, targetPort: 8888}]
```

## ConfigMap

```yaml title="k8s/configmap.yaml"
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-api-config
data:
  app.yaml: |
    Name: order-api
    Host: 0.0.0.0
    Port: 8888
```

## HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-api
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: {type: Utilization, averageUtilization: 60}
```

## Apply

```bash
kubectl apply -f k8s/
kubectl rollout status deployment/order-api
```
