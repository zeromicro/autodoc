---
title: Redis Metrics
description: Monitor Redis connection metrics in go-zero.
sidebar:
  order: 3

---

## Overview

This section highlights the relevance of monitoring through redis.

## Description

Redis has two internal metrics to monitor related metric.<a href="/docs/tutorials/monitor/index" target="_blank">More component monitoring messages</a>

1. <a href="https://github.com/zeromicro/go-zero/blob/master/core/stores/redis/metrics.go#L8" target="_blank">RedisConf</a> related introduction.

    ```go
        metricReqDur = metric.NewHistogramVec(&metric.HistogramVecOpts{
            Namespace: namespace,
            Subsystem: "requests",
            Name:      "duration_ms",
            Help:      "redis client requests duration(ms).",
            Labels:    []string{"command"},
            Buckets:   []float64{5, 10, 25, 50, 100, 250, 500, 1000, 2500},
        })
    ```

2. <a href="https://github.com/zeromicro/go-zero/blob/master/core/stores/redis/metrics.go#L16" target="_blank">metricReqErr</a>: Useful monitoring of redis commands.

    ```go
        metricReqErr = metric.NewCounterVec(&metric.CounterVecOpts{
            Namespace: namespace,
            Subsystem: "requests",
            Name:      "error_total",
            Help:      "redis client requests error count.",
            Labels:    []string{"command", "error"},
        })
    ```
