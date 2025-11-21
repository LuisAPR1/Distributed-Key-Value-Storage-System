# Prometheus

This directory contains configurations for Prometheus, the monitoring and alerting system used in the project.

## Structure

- `prometheus.yml`: Main Prometheus configuration
- `alert_rules.yml`: Alert rules
- Other specific configuration files

## Features

- **Metrics Collection**: Time series storage of system metrics
- **Service Discovery**: Automatic location of targets for monitoring
- **PromQL Expressions**: Language for querying metrics
- **Alerts**: Detection of anomalous conditions in the system
- **Integration**: Data source for Grafana

## Collected Metrics

- **API**: Latency, request rate, errors
- **Cache**: Hits, misses, memory usage
- **Database**: Operations per second, latency, storage usage
- **Queues**: Size, processing rate
- **System Resources**: CPU, memory, network, disk
- **Custom Metrics**: Application-specific metrics

## Access

- URL: http://localhost:9091
- No authentication required by default

## Configuration

To modify Prometheus targets or add alert rules:

1. Edit the `prometheus.yml` or `alert_rules.yml` file
2. Rebuild the container: `docker compose up -d prometheus`

## Data Retention

By default, Prometheus stores data for 15 days. This configuration can be adjusted in
the `prometheus.yml` file by modifying the `storage.tsdb.retention.time` parameter.