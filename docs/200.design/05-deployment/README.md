# Phase 205 — Deployment Specifications

## Overview
Design the Docker containerization and deployment strategy.

## Objectives
- Define Dockerfiles for each service
- Design docker-compose for local dev
- Specify resource requirements
- Define environment variables

## Deliverables

### Core Documents
- `docker-compose.yml` — Local development setup
- `docker/Dockerfile-generator` — Generator Dockerfile
- `docker/Dockerfile-dashboard` — Dashboard Dockerfile
- `resource-sizing.md` — CPU/memory specifications
- `environment-variables.md` — Required env vars

## Resource Requirements

| Service | CPU | Memory | Disk |
|---------|-----|--------|------|
| nginx | 0.1 core | 64MB | 100MB |
| Generator (×3) | 0.5 core each | 128MB each | 100MB |
| PostgreSQL | 1 core | 512MB | 10GB |
| Dashboard | 0.5 core | 256MB | 200MB |

## Status
- [ ] Initiated
- [ ] In progress
- [ ] Complete
