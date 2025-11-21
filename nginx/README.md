# Nginx

This directory contains Nginx configurations used as a load balancer and reverse proxy in the system.

## Structure

- Configuration files for different services
- Templates for dynamic configuration generation

## Features

- **Load Balancing**: Load distribution among multiple API instances
- **Reverse Proxy**: Exposure of internal services to the external world
- **TLS Termination**: HTTPS connection management (when configured)
- **Rate Limiting**: Protection against request overload
- **Health Checking**: Automatic detection and removal of unhealthy instances

## Main Configurations

- Configuration for the main API (request distribution)
- Configuration for CockroachDB (connection balancing)
- Configuration for administration services (Prometheus, Grafana, etc.)

## How It Works

Nginx receives all external requests and distributes them to the appropriate services:

1. Requests to `/kv` are forwarded to API instances
2. Requests to `/metrics` are forwarded to Prometheus
3. Requests to administration pages are protected and forwarded
4. Periodic health checks verify service availability

## Customization

To modify Nginx configuration:

1. Edit configuration files in this directory
2. Rebuild containers using `docker compose up --build -d`