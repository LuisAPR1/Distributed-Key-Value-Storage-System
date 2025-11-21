# Consumer / Worker

This directory contains the consumer service that processes asynchronous operations in a distributed manner.

## Structure

- `worker.py`: RabbitMQ consumer implementation
- `metrics.py`: Metrics instrumentation
- `Dockerfile`: Containerization configuration
- `requirements.txt`: Service dependencies

## Features

- Consumption of PUT and DELETE operation messages from the queue
- Asynchronous processing to improve system performance
- Data persistence to backend storage
- Cache invalidation when necessary
- Failure resilience with message acknowledgment

## How It Works

The consumer listens to RabbitMQ queues for operations requiring persistence. When a message is received:

1. The message is deserialized
2. The operation is executed on the storage backend (CockroachDB)
3. The cache is invalidated if necessary
4. The message is acknowledged (ack) only after successful processing

In case of failure, messages are automatically re-queued by RabbitMQ.