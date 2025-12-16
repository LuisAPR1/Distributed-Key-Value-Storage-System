# Distributed Key-Value Storage System

> **Quick Start**: See [SETUP.md](SETUP.md) for installation and usage instructions.

A distributed key-value storage system capable of storing, retrieving, and managing key-value pairs across multiple nodes in a distributed environment. The system is designed to handle fundamental distributed systems challenges such as fault tolerance, consistency, availability, and scalability.  
**This project was developed as part of a university course assignment (Parallel and Distributed Systems).**

## Contents

- [Architecture](#architecture-diagram)  
- [Features](#features)  
- [Technology Stack](#technology-stack)  
- [Documentation](#documentation)  
- [Distributed Systems Features](#distributed-systems-features)  
- [Cloud Implementation](#cloud-implementation)  
- [Contributing](#contributing)  
- [References](#references)

---

## Architecture Diagram

```
                           ┌─────────────┐                          
                           │   Client    │                          
                           └──────┬──────┘                          
                                  │                                 
                                  ▼                                 
             ┌───────────────────────────────────────┐             
             │         Nginx Load Balancer           │             
             └─────────────┬───────────────┬─────────┘             
                           │               │                        
           ┌───────────────▼┐           ┌─▼───────────────┐        
           │     API Node 1 │           │    API Node 2   │        
           └───────┬────────┘           └────────┬────────┘        
                   │                             │                  
┌──────────────────┼─────────────────────────────┼──────────────┐  
│                  │                             │              │  
│    ┌─────────────▼─────────────┐  ┌────────────▼────────────┐ │  
│    │     Redis Cluster         │  │      RabbitMQ Cluster   │ │  
│    │  (Cache + Sentinel)       │  │     (Message Queue)     │ │  
│    └─────────────┬─────────────┘  └────────────┬────────────┘ │  
│                  │                             │              │  
│    ┌─────────────▼─────────────┐  ┌────────────▼────────────┐ │  
│    │    CockroachDB Cluster    │  │   Consumer Workers      │ │  
│    │   (Persistent Storage)    │  │  (Async Processing)     │ │  
│    └───────────────────────────┘  └─────────────────────────┘ │  
│                                                               │  
└───────────────────────────────────────────────────────────────┘  
   
     ┌────────────────────┐  ┌─────────────────┐  ┌───────────┐   
     │  Prometheus/Grafana│  │   Autoscaler    │  │ Health    │  
     │  (Monitoring)      │  │ (Scalability)   │  │ Checks    │ 
     └────────────────────┘  └─────────────────┘  └───────────┘   
```

---

## Features

The system implements the following basic operations:

| Operation | Description |
|-----------|-------------|
| PUT (key, value) | Store a value associated with a key |
| GET (key) | Retrieve the value associated with a key |
| DELETE (key) | Remove a key-value pair |

---

## Technology Stack

### API and Services

| Component | Technology |
|-----------|------------|
| REST API | FastAPI |
| Containerization | Docker & Docker Compose |
| Load Balancer | Nginx |

### Storage

| Component | Technology |
|-----------|------------|
| Persistent Storage | CockroachDB (distributed and resilient) |
| Cache | Redis with Sentinel for high availability |

### Messaging

| Component | Technology |
|-----------|------------|
| Message Queue | RabbitMQ for asynchronous operations |

### Monitoring

| Component | Technology |
|-----------|------------|
| Metrics Collection | Prometheus |
| Visualization | Grafana dashboards |

### Automation

| Component | Purpose |
|-----------|---------|
| Autoscaler | Automatically scales services based on load |
| Health Checks | Continuous operational status verification |

---

## Documentation

| Document | Description |
|----------|-------------|
| [SETUP.md](SETUP.md) | Installation, configuration, and usage instructions |
| [TESTING.md](TESTING.md) | Unit testing and load testing guide |
| [CLOUD/README.md](CLOUD/README.md) | Cloud migration planning and strategy |

---

## Distributed Systems Features

### Concurrency

The system manages concurrency through:

- Atomic operations in CockroachDB  
- Message queues in RabbitMQ for asynchronous operations  
- Distributed cache with Redis to reduce contention

### Scalability

Scalability is ensured by:

- Loosely coupled microservices architecture  
- Load balancer for request distribution  
- Autoscaler for dynamic resource adjustment  
- Distributed database cluster

### Fault Tolerance

The system implements fault tolerance mechanisms:

- Data replication in CockroachDB  
- Redis Sentinel for failure detection and automatic failover  
- RabbitMQ cluster to ensure message processing  
- Continuous health checks for proactive problem detection

### Consistency

Data consistency is guaranteed by:

- ACID transactions in CockroachDB  
- Distributed coordination mechanism for updates  
- Cache with expiration policy to reduce inconsistencies

### Resource Coordination

Resource coordination is managed through:

- Load balancing between API nodes  
- Balanced data distribution in the cluster  
- Message queues to coordinate asynchronous operations

---

## Cloud Implementation

A detailed plan for migrating and implementing this system in the cloud is available in the `/CLOUD` directory. The plan includes:

- Proposed architecture in cloud providers (AWS, Azure, GCP)  
- Phased migration strategy  
- Security and compliance considerations  
- Cost estimation  
- Benefits of cloud migration

For more details, see [CLOUD/README.md](CLOUD/README.md).

---

## Contributing

1. Fork the repository  
2. Create a branch for your feature (`git checkout -b feature/amazing-feature`)  
3. Commit your changes (`git commit -m 'Add some amazing feature'`)  
4. Push to the branch (`git push origin feature/amazing-feature`)  
5. Open a Pull Request

---

## References

### Academic References

- Tanenbaum, A. S., & Van Steen, M. (2017). *Distributed systems: principles and paradigms.*  
- Kleppmann, M. (2017). *Designing data-intensive applications: The big ideas behind reliable, scalable, and maintainable systems.* O'Reilly Media, Inc.

### Technologies Used

| Technology | Documentation |
|------------|---------------|
| FastAPI | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| CockroachDB | [cockroachlabs.com/docs](https://www.cockroachlabs.com/docs/) |
| Redis | [redis.io/documentation](https://redis.io/documentation) |
| RabbitMQ | [rabbitmq.com/documentation](https://www.rabbitmq.com/documentation.html) |
| Docker | [docs.docker.com](https://docs.docker.com/) |

---

## License & Acknowledgments

- This project was created for educational purposes as part of a university course.  
- Tanenbaum, A. S., & Van Steen, M. (2017). *Distributed systems: principles and paradigms.*  
- Kleppmann, M. (2017). *Designing data-intensive applications.* O'Reilly Media, Inc.

---

## Author

**[LuisAPR1](https://github.com/LuisAPR1)**

---

*This README was auto-generated with the assistance of Claude Opus 4.5 Thinking.*
