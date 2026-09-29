"""Health Controller - Transport Layer."""

import time
from typing import Any

from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])

_start_time = time.time()


@router.get("/health")
async def health(request: Request) -> dict[str, Any]:
    """Health check endpoint.

    Returns:
        Health status with instance information
    """
    return {
        "status": "ok",
        "instance": f"dc-{request.app.state.datacenter_id}-machine-{request.app.state.machine_id}",
        "uptime_seconds": time.time() - _start_time,
    }
