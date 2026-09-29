# State Machine: Generator Instance Lifecycle

## Overview
This document describes the lifecycle states and transitions for a single Generator instance.

## State Diagram

```
                                    ┌─────────────────────────────────────────┐
                                    │                                         │
                                    ▼                                         │
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────────┐
│          │───▶│              │───▶│              │───▶│              │───▶│            │
│          │    │              │    │              │    │              │    │            │
│ STARTING │    │   HEALTHY    │    │   DEGRADED   │    │    FAILED    │    │  STOPPED   │
│          │◀───│              │◀───│              │◀───│              │◀───│            │
│          │    │              │    │              │    │              │    │            │
└──────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └────────────┘
     │               │                   │                  │
     │               │                   │                  │
     │               ▼                   ▼                  │
     │        ┌──────────────┐    ┌──────────────┐            │
     └───────▶│    FAILED    │───▶│   STOPPED    │◀───────────┘
              └──────────────┘    └──────────────┘
```

## States

### STARTING
**Description:** Initial state when the process is booting up.

| Property | Value |
|----------|-------|
| Accepts Requests | No |
| Health Check | Fail |
| Logging | INFO |

**Entry Actions:**
- Load configuration (datacenter_id, machine_id, epoch)
- Initialize clock service
- Initialize sequence counter to 0
- Open database connections (if persistence enabled)

**Exit Criteria:**
- All initialization complete
- Clock service responding
- Health check passes

---

### HEALTHY
**Description:** Normal operation. The instance is fully functional and accepting requests.

| Property | Value |
|----------|-------|
| Accepts Requests | Yes |
| Health Check | Pass |
| Logging | INFO (periodic heartbeat) |

**Entry Actions:**
- Start heartbeat logging
- Begin accepting /generate requests

**Exit Criteria:**
- Clock drift detected (transition to DEGRADED)
- Sequence overflow handled
- Fatal error occurred (transition to FAILED)
- SIGTERM received (transition to STOPPING)

**Invariants Maintained:**
- IDs are monotonically increasing within a millisecond
- Sequence number never exceeds 4095
- Timestamp never goes backwards

---

### DEGRADED
**Description:** The instance is functioning but with reduced capacity or potential issues.

| Property | Value |
|----------|-------|
| Accepts Requests | Yes (with warnings) |
| Health Check | Pass (with warnings) |
| Logging | WARN |

**Entry Conditions:**
- Clock drift detected (> 1ms but < 10ms)
- Database connection unstable
- High error rate (> 1% but < 10%)

**Exit Criteria:**
- Issue resolved → transition to HEALTHY
- Issue worsens → transition to FAILED
- Manual restart → transition to STOPPED

**Actions:**
- Log warning with details
- Continue generating IDs
- Alert monitoring system

---

### FAILED
**Description:** Unrecoverable error. The instance cannot continue.

| Property | Value |
|----------|-------|
| Accepts Requests | No |
| Health Check | Fail |
| Logging | ERROR |

**Entry Conditions:**
- Fatal exception (MemoryError, OSError)
- Clock went backwards by > 10ms
- Database corruption detected
- Unhandled exception in critical path

**Actions:**
- Log error with full stack trace
- Attempt graceful cleanup
- Close database connections
- Exit process

---

### STOPPED
**Description:** Terminal state. The process has exited.

| Property | Value |
|----------|-------|
| Accepts Requests | No |
| Health Check | N/A |
| Logging | None |

**Entry Conditions:**
- Graceful shutdown (SIGTERM)
- Failed state cleanup complete
- Manual kill (SIGKILL)

**Actions:**
- Final cleanup
- Close file handles
- Flush logs

---

## Transitions

| ID | From | To | Trigger | Guard Conditions | Actions |
|----|------|----|---------|-------------------|---------|
| T1 | - | STARTING | Process spawn | None | Load config, init services |
| T2 | STARTING | HEALTHY | Init complete | All services OK | Start heartbeat |
| T3 | STARTING | FAILED | Init failed | Exception thrown | Log error, cleanup |
| T4 | HEALTHY | DEGRADED | Clock drift detected | 1ms < drift < 10ms | Log warning |
| T5 | HEALTHY | FAILED | Fatal error | Exception in critical path | Log error, cleanup |
| T6 | HEALTHY | STOPPED | SIGTERM received | Graceful shutdown | Close connections |
| T7 | DEGRADED | HEALTHY | Issue resolved | Clock sync restored | Log info |
| T8 | DEGRADED | FAILED | Issue worsened | drift >= 10ms | Log error, cleanup |
| T9 | DEGRADED | STOPPED | SIGTERM received | Graceful shutdown | Close connections |
| T10 | FAILED | STOPPED | Cleanup complete | Process exit | None |

## Special Transitions

### Sequence Overflow
```
HEALTHY ──[sequence >= 4096]──▶ Wait for next ms ──▶ HEALTHY
```

### Clock Going Backwards
```
HEALTHY ──[timestamp < last_timestamp]──▶ ERROR: Clock went backwards
                                              │
                                              ▼
                                           FAILED
```

### All Generators Unavailable (External View)
```
System State: All generators in {DEGRADED, FAILED, STOPPED}
                                               │
                                               ▼
                                    Return 503 to client
```

## Health Check Response by State

| State | /health response | HTTP Status |
|-------|------------------|-------------|
| STARTING | { "status": "starting" } | 200 |
| HEALTHY | { "status": "ok", "instance": "dc-XX-machine-XX" } | 200 |
| DEGRADED | { "status": "degraded", "instance": "...", "warning": "..." } | 200 |
| FAILED | { "status": "down", "error": "..." } | 503 |
| STOPPED | No response (connection refused) | - |

## Metrics by State

| Metric | STARTING | HEALTHY | DEGRADED | FAILED | STOPPED |
|--------|----------|---------|----------|--------|---------|
| ids_generated | 0 | Incrementing | Incrementing | Frozen | Frozen |
| error_count | 0 | Low | Medium | High | N/A |
| uptime_seconds | 0 | Incrementing | Incrementing | Frozen | N/A |
| sequence_current | 0 | 0-4095 | 0-4095 | Frozen | N/A |
