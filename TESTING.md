# Testing Guide

This guide covers all aspects of testing the Distributed Key-Value Storage System, including unit tests and load tests.

## Overview

The system includes two types of tests:
- **Unit Tests**: Verify core functionality of the API
- **Load Tests**: Measure performance under various load conditions

## Unit Tests

### What Gets Tested

The unit test suite verifies:

1. **Health Checks**:
   - General health check
   - Liveness probe (Kubernetes compatibility)
   - Readiness probe (Kubernetes compatibility)

2. **Cache Statistics**:
   - Endpoint availability
   - Correct statistics format

3. **Key-Value Operations**:
   - PUT: Add/update values
   - GET: Retrieve values
   - DELETE: Remove values

4. **Error Validation**:
   - Behavior for non-existent keys
   - Invalid request validation

### How Unit Tests Work

1. **Initialization**: The `start.sh` script starts all services using Docker Compose
2. **Wait**: The system waits 10 seconds to ensure all services are ready
3. **Health Check**: The test script verifies the API is available
4. **Execution**: All unit tests are executed
5. **Report**: Results show the number of successful and failed tests
6. **Continuation**: If all tests pass, the script continues with normal initialization

### Running Unit Tests Manually

You can run unit tests at any time:

```bash
python3 -m unitary_tests.tests
```

### Adding New Tests

To add new unit tests:

1. Open `unitary_tests/tests.py`
2. Add a new test method to the `KVStoreAPITests` class (must start with `test_`)
3. Implement your test cases using `unittest` assertion methods

Example:

```python
def test_new_feature(self):
    """Description of new test"""
    response = requests.get(urljoin(BASE_URL, "/new-route"))
    self.assertEqual(response.status_code, 200)
```

### Troubleshooting Unit Tests

If tests fail:

1. Check if all services are running: `docker compose ps`
2. View service logs: `docker compose logs api consumer`
3. Verify Nginx is routing requests correctly
4. Increase initial wait time in `start.sh` if services need more startup time

## Load Tests

### What is Siege?

Siege is a load testing and benchmarking HTTP tool designed to measure web server performance under pressure. It allows developers to simulate multiple concurrent users and observe application behavior under different load conditions.

### Key Features of Siege

- Simulates multiple concurrent users
- Supports HTTP and HTTPS
- Generates detailed performance reports
- Allows configuring different load levels
- Uses a URL file to test different endpoints

### Installing Siege

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install siege
```

#### CentOS/RedHat
```bash
sudo yum install siege
```

#### macOS
```bash
brew install siege
```

#### Windows
On Windows, use WSL (Windows Subsystem for Linux) and follow Ubuntu/Debian instructions.

### Running Load Tests

The project includes a shell script to facilitate load test execution. The script supports testing PUT, GET, and DELETE operations.

#### Basic Usage

```bash
# Make script executable (first time only)
chmod +x load-tests/load-tests-siege.sh

# Run default test (PUT)
./load-tests/load-tests-siege.sh

# Specify test type (put, get, delete, or all)
./load-tests/load-tests-siege.sh put    # Test only PUT operation
./load-tests/load-tests-siege.sh get    # Test only GET operation
./load-tests/load-tests-siege.sh delete # Test only DELETE operation
./load-tests/load-tests-siege.sh all    # Test all operations in sequence
```

### Configuration

You can configure tests by modifying these variables at the beginning of the script:

- `NUM_KEYS`: Number of keys to test (default: 100)
- `USERS`: Number of concurrent users (default: 25)
- `DURATION`: Test duration (default: 1M, i.e., 1 minute)

### Interpreting Results

Siege provides a detailed report after test completion. Key metrics to observe:

1. **Transactions**: Total number of processed requests
2. **Availability**: Percentage of successful requests (ideally 100%)
3. **Response time**: Average response time per request (lower is better)
4. **Transaction rate**: Number of transactions processed per second (higher is better)
5. **Concurrency**: Average simultaneous connections maintained during the test
6. **Failed transactions**: Number of failed transactions (ideally zero)

### Example Siege Commands

If you prefer using Siege directly:

```bash
# Simulate 25 concurrent users for 1 minute
siege -c 25 -t 1M https://example.com/api

# Use a URL file for testing
siege -f urls.txt -c 25 -t 1M

# Add detailed information during test
siege -f urls.txt -c 25 -t 1M -v

# Simulation with random delay (more realistic)
siege -f urls.txt -c 25 -t 1M -d 10

# Set Content-Type header
siege --content-type="application/json" -f urls.txt -c 25 -t 1M
```

### Testing Different Scenarios

When testing your API, consider these scenarios:

1. **Normal Load**: Test with a typical number of users from your production environment
2. **Peak Load**: Test with high number of users to simulate traffic spikes
3. **Stress Test**: Gradually increase number of users until finding application limits
4. **Endurance Test**: Run tests for extended periods to identify memory/resource issues

## Common Issues

### Messages Not Appearing in RabbitMQ

If Siege is generating traffic (with high availability and transaction rate) but no messages appear in RabbitMQ, verify:

1. **Request body format**: Siege has a peculiarity in how it sends POST data. Instead of putting JSON directly in the URL file:

   ```
   # Incorrect format - doesn't send JSON correctly
   http://localhost/kv POST {"data":{"key":"test_key","value":"test_value"}}
   ```

   Use external files for JSON data:

   ```
   # Correct format - references a file with JSON content
   http://localhost/kv POST <data_file.json>
   ```

   The `load-tests-siege.sh` script already implements this approach by creating temporary JSON files for each request.

2. **HTTP Headers**: Verify that the `Content-Type: application/json` header is being sent correctly.

3. **Response code verification**: Siege may show low numbers in "successful_transactions" even when the API responds correctly with code 202, as it primarily considers 200 codes as success. Check API logs to confirm.

### Authorization Errors

If you encounter authorization errors, verify that the API security settings allow test requests. For APIs requiring authentication, you may need to include authentication headers:

```bash
# Add authentication header
siege --header="Authorization: Bearer your_token_here" -f urls.txt -c 25 -t 1M
```

## Limitations and Considerations

- Siege is a command-line tool and doesn't offer a graphical interface
- Very aggressive configurations can cause problems on the system running Siege
- Results may vary depending on the machine's capacity running the tests
- Consider the impact on server resources when running tests in shared environments

## Recommendations for Load Testing

1. **Start small**: Begin with small loads and gradually increase
2. **Monitor resources**: Watch CPU, memory, and network during tests
3. **Test in isolated environment**: Avoid impacting real users or other services
4. **Test regularly**: Perform load tests as part of your development cycle

## References

- [Official Siege Documentation](https://www.joedog.org/siege-manual/)
- [Siege GitHub Project](https://github.com/JoeDog/siege)
