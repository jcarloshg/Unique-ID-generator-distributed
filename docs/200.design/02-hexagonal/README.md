# Phase 202 — Hexagonal Architecture

## Overview
Design the hexagonal (ports & adapters) architecture for the Generator service.

## Objectives
- Define domain layer (pure business logic)
- Define port interfaces
- Design adapter implementations
- Ensure dependency direction

## Deliverables

### Core Documents
- `domain-model.md` — Domain entities and services
- `ports.md` — Port interfaces (IClock, IIdPersistence)
- `adapters.md` — Adapter implementations
- `dependency-rule.md` — Dependency direction validation

## Domain Model

### Entities
- `SnowflakeId` — Value object for 64-bit ID
- `GeneratorConfig` — Datacenter/machine ID configuration

### Services
- `IdGeneratorService` — Core Snowflake algorithm
- `SequenceManager` — Sequence counter management

### Ports
- `IClock` — Time provider interface
- `IIdPersistence` — Persistence interface

## Status
- [ ] Initiated
- [ ] In progress
- [ ] Complete
