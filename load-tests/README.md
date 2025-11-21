# Load Tests

This directory contains scripts and tools for performing load tests on the distributed key-value storage system.

## Structure

- `load-tests-siege.sh`: Script to run tests with the Siege tool
- `README-load-tests.md`: Detailed documentation about load tests (deprecated - see main TESTING.md)

## Features

- Load tests for PUT, GET, and DELETE operations
- Simulation of multiple concurrent users
- Performance and availability metrics
- Configurable tests (number of users, duration, etc.)

## How to Execute

```bash
# Run all load tests
./load-tests-siege.sh all

# Test only a specific operation
./load-tests-siege.sh put    # Test only PUT
./load-tests-siege.sh get    # Test only GET
./load-tests-siege.sh delete # Test only DELETE
```

## Configuration

Test parameters can be adjusted by editing the `load-tests-siege.sh` script:

- `NUM_KEYS`: Number of keys to test
- `USERS`: Number of concurrent users
- `DURATION`: Test duration

## Requirements

- Siege: HTTP benchmarking tool
- System running (all containers active)

## Interpreting Results

The script generates reports containing the following metrics:

- Throughput (transactions per second)
- Average response time
- Availability rate
- Average concurrency
- Number of successful and failed transactions

See the main [TESTING.md](../TESTING.md) for more details on result interpretation and troubleshooting common issues.