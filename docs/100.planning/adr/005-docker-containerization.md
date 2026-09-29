# ADR-005: Docker for Containerization

## Status
Accepted

## Context
We need to containerize all services (nginx, Python generators, PostgreSQL, Vite dashboard) for consistent deployment across environments.

## Decision
We will use **Docker** with **docker-compose** for local development and container orchestration.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| Docker + docker-compose | Standard, well-understood, easy local dev | No auto-scaling, single-node |
| Kubernetes | Auto-scaling, orchestration, production-grade | Overkill for initial deployment, complexity |
| Podman | Docker-compatible, rootless | Less ecosystem, less tooling |
| Bare-metal | No container overhead | Poor portability, environment inconsistency |

## Decision Rationale
1. **Standardization** — Docker is the industry standard for containers
2. **Simplicity** — docker-compose provides simple local orchestration
3. **Portability** — Consistent behavior across dev/staging/prod
4. **Team expertise** — Familiar to the team
5. **Future migration** — Docker images can run on Kubernetes later

## Consequences

### Positive
- Consistent environments across dev/staging/prod
- Easy local development setup
- Simple service orchestration with docker-compose
- Standard CI/CD integration

### Negative
- Additional layer of abstraction
- Docker daemon running on host required
- Single-node limitation (mitigation: easy to migrate to K8s later)

## Docker Images

| Service | Base Image | Multi-stage |
|---------|------------|-------------|
| Generator | python:3.11-slim | Yes |
| nginx | nginx:alpine | No |
| Dashboard | node:20-alpine | Yes |
| PostgreSQL | postgres:15-alpine | No |

## Implementation Notes
- Use **multi-stage builds** for Python and Node services
- Pin base images by digest for reproducibility
- Use `.dockerignore` to minimize image size
- Expose ports: 80 (nginx), 5001-5003 (generators), 5432 (postgres), 3000 (dashboard)
