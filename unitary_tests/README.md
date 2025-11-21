# Unit Tests

This directory contains unit tests to verify correct functioning of the key-value storage system.

## Structure

- `tests.py`: Main test suite
- `run_tests.py`: Alternative test runner script
- `README-tests.md`: Detailed test documentation (deprecated - see main TESTING.md)

## Tested Features

- Health checks and system state verification
- PUT, GET, and DELETE API operations
- Cache statistics
- Error behavior (non-existent keys, invalid formats)

## How to Execute

Tests can be run in two ways:

1. **Automatically during startup**:
   ```bash
   ./start.sh
   ```
   
2. **Manually**:
   ```bash
   python3 -m unitary_tests.tests
   ```

## Requirements

- Python 3.8+
- requests module
- System running (all containers active)

## Extending Tests

Tests are designed to be easily extended. To add new test cases:

1. Open the `tests.py` file
2. Add a new method to the test class (starting with `test_`)
3. Implement necessary checks using assertion methods

See the main [TESTING.md](../TESTING.md) for more details on test implementation.