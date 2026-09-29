# Phase 101 — Business Context

## Overview
This phase establishes the Ubiquitous Language, maps Domain Events, and defines Bounded Contexts for the Unique ID Generator Distributed service.

## Objectives
- Establish shared domain vocabulary
- Map core business workflows as domain events
- Define bounded contexts and their responsibilities
- Document business invariants

## Deliverables

### Core Document
- `01.business-context.md` — Complete Business Context analysis

### Supporting Documents
- `02.ubiquitous-language.md` — Domain glossary ✅
- `03.event-storming.md` — Domain events mapping ✅
- `04.bounded-contexts.md` — Context map ✅
- `05.invariants.md` — Business rules ✅

## Phase Steps

| Step | Description |
|------|-------------|
| 1 | Gather Raw Business Inputs |
| 2 | Establish Ubiquitous Language |
| 3 | Run Event Storming |
| 4 | Define Bounded Contexts |
| 5 | Define Business Rules |
| 6 | Produce Business Context Summary |
| 7 | Verification Checklist |
| 8 | Handoff to Next Steps |

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Snowflake Algorithm adopted | Industry-proven, meets requirements |
| 4 Bounded Contexts | ID Generation, Persistence, Load Balancing, Monitoring |
| CP Consistency chosen | Zero collision tolerance |
| Single datacenter in v1 | No multi-region complexity needed |

## Status
- [x] Phase document created
- [x] Supporting documents created
- [x] Verified against 00.defining.md
- [ ] Signed off by Tech Lead

## Next Phase
→ Phase 102 — Technical Requirements
