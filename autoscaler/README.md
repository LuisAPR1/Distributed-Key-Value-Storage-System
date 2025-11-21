# Autoscaler

This directory contains the service responsible for automatically scaling system components based on load.

## Structure

- `autoscaler.py`: Main autoscaler implementation
- `Dockerfile`: Containerization configuration
- `requirements.txt`: Service dependencies

## Features

- System load metrics monitoring via Prometheus
- Automatic scaling of API and consumer services
- Dynamic replica adjustment based on resource usage
- Oscillation prevention with cooldown periods
- Configurable maximum and minimum instance limits

## How It Works

The autoscaler operates in periodic cycles:

1. Queries Prometheus metrics (latency, CPU, memory, queue size)
2. Applies decision algorithms to determine optimal number of replicas
3. Interacts with Docker API to scale services up/down
4. Logs scaling decisions for later analysis

## Configuration

Autoscaler behavior can be adjusted via environment variables:

- `SCALE_INTERVAL`: Interval between scaling decisions (seconds)
- `MIN_REPLICAS`: Minimum number of replicas per service
- `MAX_REPLICAS`: Maximum number of replicas per service
- `SCALE_UP_THRESHOLD`: Threshold for scaling up decision
- `SCALE_DOWN_THRESHOLD`: Threshold for scaling down decision