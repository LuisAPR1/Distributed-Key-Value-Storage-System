# Setup Guide

This guide provides detailed instructions for installing, configuring, and running the Distributed Key-Value Storage System.

## Requirements

- **Docker** and **Docker Compose**
- **Operating System**: Linux, macOS, or Windows with WSL
- **Python 3.8+** (for running tests manually)

## Quick Installation

The system is designed for instant setup using a single command:

```bash
# Clone the repository
git clone https://github.com/LuisAPR1/Distributed-Key-Value-Storage-System.git
cd Distributed-Key-Value-Storage-System

# Run the startup script
./start.sh
```

The `start.sh` script will:
1. Start all necessary containers
2. Configure the database and cache
3. Run unit tests to verify installation
4. Start the system and display access information

## Manual Installation

If you prefer to start the system manually or need more control:

### Step 1: Start Services

```bash
docker compose up --build -d
```

### Step 2: Wait for Services

Wait 10-15 seconds for all services to initialize properly.

### Step 3: Verify Installation

Run the unit tests:

```bash
python3 -m unitary_tests.tests
```

## API Endpoints

The system exposes the following REST API endpoints:

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET    | /kv      | Retrieve value | key (query param) |
| PUT    | /kv      | Store key-value | JSON body: `{"data": {"key":"foo", "value":"bar"}}` |
| DELETE | /kv      | Remove key | key (query param) |
| GET    | /health  | Health check | - |
| GET    | /metrics | Prometheus metrics | - |

### Example API Calls

**Store a key-value pair:**
```bash
curl -X PUT http://localhost/kv \
  -H "Content-Type: application/json" \
  -d '{"data": {"key":"test", "value":"hello world"}}'
```

**Retrieve a value:**
```bash
curl http://localhost/kv?key=test
```

**Delete a key:**
```bash
curl -X DELETE http://localhost/kv?key=test
```

## Web Interface

A simple web interface is available at http://localhost/ to interact with the API through your browser.

## Administrative Interfaces

The system provides several administrative interfaces for monitoring and management:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Grafana** | http://localhost:3000 | admin/admin |
| **Prometheus** | http://localhost:9091 | - |
| **RabbitMQ Management** | http://localhost:25673 | admin/admin |
| **CockroachDB Admin** | http://localhost:8080 | - |
| **API Documentation (Swagger)** | http://localhost/docs | - |
| **Health Check** | http://localhost/health | - |

## Configuration

The system can be configured through environment variables in the `docker-compose.yml` file. Key configuration options include:

- **API replicas**: Number of API server instances
- **Cache size**: Redis memory limits
- **Database connections**: CockroachDB connection pool settings
- **Message queue**: RabbitMQ cluster configuration

## System Limits and Capabilities

- **Storage**: Limited by disk space allocated to CockroachDB volumes
- **Cache**: Configured for maximum 100MB per Redis instance
- **Maximum key size**: 1KB
- **Maximum value size**: 1MB
- **Throughput**: Approximately 2000 requests/second for reads and 500 requests/second for writes on recommended hardware

## Stopping the System

To stop all services:

```bash
docker compose down
```

To stop and remove all data (volumes):

```bash
docker compose down -v
```

## Troubleshooting

### Services not starting

Check service status:
```bash
docker compose ps
```

View logs:
```bash
docker compose logs api consumer
```

### Tests failing

1. Ensure all services are running: `docker compose ps`
2. Check API logs: `docker compose logs api`
3. Verify Nginx is routing correctly: `docker compose logs nginx`
4. Increase wait time in `start.sh` if services need more time to initialize

### Connection refused errors

Wait a few more seconds for services to fully initialize. The system has multiple components that need to start in sequence.

## Next Steps

- See [TESTING.md](TESTING.md) for information on running unit tests and load tests
- See [CLOUD/README.md](CLOUD/README.md) for cloud migration planning
- Check the main [README.md](README.md) for architecture and distributed systems features
