# Storage Adapters

This directory contains storage adapters for different persistence backends.

## Structure

- `__init__.py`: Dynamic backend selector based on configuration
- `base.py`: Base interface (abstract class) for all backends
- `cockroach_backend.py`: Implementation for CockroachDB
- `sqlite_backend.py`: Implementation for SQLite (development/testing)
- `memory.py`: In-memory implementation (development/testing)

## Design

The system was designed with an adapter pattern, allowing:

- Backend changes without modifying application code
- Isolation of complexities specific to each storage system
- Unit testing with simulated or in-memory backends
- Easy addition of new backends in the future

## Available Backends

### CockroachDB (Production)
- Persistent and distributed
- High availability and fault tolerance
- ACID transactions across nodes
- Horizontal scalability

### SQLite (Development)
- Persistent but not distributed
- Easy to configure for development
- No external dependencies
- Low resource overhead

### Memory (Testing)
- Not persistent
- Extremely fast
- Useful for unit tests
- No configuration required

## Usage

Backend selection is done via environment variable:

```bash
STORAGE_BACKEND=cockroach  # Use CockroachDB
STORAGE_BACKEND=sqlite     # Use SQLite
STORAGE_BACKEND=memory     # Use in-memory storage
```

By default, the system uses CockroachDB in production environment.