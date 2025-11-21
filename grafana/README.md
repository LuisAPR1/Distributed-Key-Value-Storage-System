# Grafana

This directory contains configurations and dashboards for Grafana, the system's visualization and monitoring tool.

## Structure

- Pre-configured dashboards for monitoring
- Datasource configuration (Prometheus)
- Alerts and notifications

## Available Dashboards

1. **System Overview**: General metrics and service status
2. **API Performance**: Latency, throughput, and error rate
3. **Redis Cache**: Hit/miss rate, memory usage
4. **CockroachDB**: Database metrics, operations per second
5. **RabbitMQ**: Queue size, message processing rate
6. **System Resources**: CPU, memory, network per service

## Access

- URL: http://localhost:3000
- Default credentials: admin/admin

## Configuration

Dashboards are automatically provisioned during system initialization.
To add new dashboards:

1. Create the dashboard via Grafana interface
2. Export the dashboard JSON
3. Add the file to the `dashboards/` directory
4. Update the `dashboards.yaml` file to include the new dashboard
5. Rebuild containers: `docker compose up -d grafana`

## Alerts

The system includes alerts configured for critical conditions:

- High API latency
- API errors above threshold
- Processing queue too large
- Resource usage (CPU/memory) above limit

Alerts can be configured to send notifications via email or other communication channels.