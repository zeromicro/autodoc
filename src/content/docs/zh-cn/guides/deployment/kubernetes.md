---
title: Kubernetes 部署
description: 在 Kubernetes 集群中部署 go-zero 服务。
sidebar:
  order: 16
---

# Kubernetes 部署

![部署架构图](../../../../../assets/deployment.svg)

建议使用 Deployment + Service + Ingress，并结合 HPA 实现弹性扩容。
