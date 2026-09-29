# ADR-002: Python as Generator Language

## Status
Accepted

## Context
We need a generator service that produces unique IDs at 10,000+ RPS. The service implements the Snowflake algorithm and exposes an HTTP API.

## Decision
We will use **Python** as the primary language for the generator service.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| Python | Team expertise, fast development, rich ecosystem | GIL concerns for threading, slower than Go/Rust |
| Go | High performance, built-in concurrency, simple deployment | Learning curve, additional complexity |
| Rust | Maximum performance, memory safety | Steep learning curve, slower development |
| Node.js | Non-blocking I/O, JSON-native | Less suitable for CPU-bound ID generation |
| Java | Mature, fast JIT | Verbose, heavy resource usage |

## Decision Rationale
1. **Team expertise** — Strong Python proficiency across the team
2. **Development speed** — Fast iteration for initial implementation
3. **Performance adequacy** — Single generator can handle 4M+ RPS; Python can easily hit 10K RPS
4. **Simplicity** — Python's arithmetic operations are fast enough for Snowflake ID generation

## Performance Validation
```
Target: 10,000 RPS
Single Python instance: ~50,000-100,000 RPS (simple endpoint)
Single Python instance with Snowflake: ~20,000-50,000 RPS
Required generators: 1 (with redundancy of 3)
```

## Consequences

### Positive
- Rapid development and prototyping
- Easy integration with PostgreSQL (asyncpg, SQLAlchemy)
- Good testing ecosystem (pytest)
- Simple deployment with Docker

### Negative
- GIL prevents true multi-threaded parallelism (mitigated: async or multiprocessing)
- Slower than Go/Rust for CPU-bound tasks (not a bottleneck for this use case)

## Implementation Notes
- Use **FastAPI** or **Flask** for HTTP server
- Use **asyncio** for concurrent request handling
- Use `time.time_ns()` or `datetime` for high-resolution timestamps
- Consider **multiprocessing** if single-threaded performance is insufficient
