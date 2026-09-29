# ADR-001: nginx as Load Balancer

## Status
Accepted

## Context
We need a load balancer to distribute HTTP requests across 3 generator instances. The load balancer is the single entry point for all client services requesting unique IDs.

## Decision
We will use **nginx** as the HTTP load balancer.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| nginx | Battle-tested, simple config, low resource usage, well-understood | No built-in auto-recovery, single instance SPOF |
| HAProxy | High performance, health checks, ACLs | More complex config |
| AWS ALB | Managed, highly available | Cloud-specific, overkill for internal service |
| Traefik | Dynamic, Docker integration | Additional complexity for internal tool |

## Decision Rationale
1. **Simplicity** — nginx configuration is straightforward for round-robin load balancing
2. **Team expertise** — Team is familiar with nginx configuration
3. **Resource efficiency** — nginx has minimal memory/CPU footprint
4. **Maturity** — Production-proven at massive scale

## Consequences

### Positive
- Simple, predictable load distribution (round-robin)
- Minimal operational overhead
- Low latency overhead (~0.5ms)

### Negative
- nginx is a single point of failure (mitigation: internal service, low availability requirement)
- No built-in health check auto-removal of failed generators
- Manual intervention required if nginx goes down

## Implementation Notes
- Use `ip_hash` or `round_robin` for distribution
- Configure `/health` endpoint for upstream checks
- Set appropriate timeouts (connect: 5s, read: 10s)
