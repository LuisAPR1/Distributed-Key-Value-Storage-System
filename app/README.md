# Main API (FastAPI)

This directory contains the REST API implementation that serves as the main entry point for the key-value storage system.

## Structure

- `main.py`: FastAPI application definition and API endpoints
- `cache.py`: Redis interface for caching
- `mq.py`: RabbitMQ client for messaging
- `metrics.py`: Prometheus metrics instrumentation
- `health_check.py`: Health checks implementation
- `storage/`: Adapters for different storage backends

## Features

- REST endpoints for PUT, GET, and DELETE operations
- Data caching using Redis
- Event publishing for asynchronous processing
- Monitoring via Prometheus metrics
- Health checks for orchestrator integration

## Dependencies

Dependencies are listed in the `requirements.txt` file and include:
- FastAPI: Web framework
- uvicorn: ASGI server
- Redis: Cache client
- pika: RabbitMQ client
- prometheus-client: Metrics client
- psycopg: CockroachDB client