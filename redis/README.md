# Redis

This directory contains configurations and scripts related to Redis, used as the caching system in the project.

## Configuration

Redis is implemented as a cluster with:
- 1 master node
- 2 slave nodes (read replicas)
- 3 sentinel nodes (monitoring and automatic failover)

## Features

- **Data Caching**: Temporary storage of frequently accessed values
- **High Availability**: Sentinel for failure detection and automatic failover
- **Replication**: Replicas for read load distribution
- **TTL**: Configurable time-to-live for keys
- **Metrics**: Usage and performance statistics

## Policies and Limits

- **Expiration Policy**: allkeys-lru (Least Recently Used)
- **Memory Limit**: 100MB per instance
- **Cache Time**: 5 minutes (configurable)

## How It Works

1. When a GET is requested, the system first checks the Redis cache
2. If found (cache hit), the value is returned immediately
3. If not found (cache miss), the value is fetched from the database and stored in cache
4. When a PUT/DELETE is processed, the cache is invalidated to maintain consistency

## Persistence

Redis in this project is configured without disk persistence, functioning purely as a cache.
The mapped Docker volumes serve only to ensure that configurations are preserved
between restarts.