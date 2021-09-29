# charm-loki-k8s

## Description

The [Loki](https://grafana.com/oss/loki/) operator provides a logging aggregation system.

## Usage

The Loki operator may be deployed using the Juju command line via:

```bash
    juju deploy loki-k8s --resource loki-image=grafana/loki:2.3.0
```

## Relations

```bash
    juju relate loki-k8s grafana-k8s
```

## OCI Images

This charm defaults to the latest version of the [grafana/loki](https://hub.docker.com/r/grafana/loki) image.

## Roadmap to completion

What is needed before this charm could be considered complete and production ready:

1. Add storage
2. Support Loki horizontally scalable with the microservice mode (querier, ingester, query-frontend, or distributor)
3. Create charms for agents that aggregates logs, e.g. promtail, grafana-agent
4. Support TLS termination