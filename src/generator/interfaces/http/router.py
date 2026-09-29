"""HTTP Router - Transport Layer."""

from typing import Any

import structlog
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse, Response

from generator.domain.services.id_generator import ClockBackwardsError, IdGeneratorService

logger = structlog.get_logger()

router = APIRouter(prefix="", tags=["id"])


def create_id_generator(app: FastAPI) -> IdGeneratorService:
    """Factory function to create IdGeneratorService with app state."""
    return IdGeneratorService(
        clock=app.state.clock,
        datacenter_id=app.state.datacenter_id,
        machine_id=app.state.machine_id,
    )


@router.get("/generate")
async def generate_id(request: Request) -> Response:
    """Generate a unique Snowflake ID.

    Returns:
        JSON response with 64-bit unique ID

    Raises:
        500: If clock moved backwards or other error
    """
    try:
        generator = create_id_generator(request.app)
        snowflake_id = generator.generate_id()
        return JSONResponse(content={"id": snowflake_id.value})
    except ClockBackwardsError as e:
        logger.error(
            "clock_backwards",
            expected_ms=e.expected_ms,
            actual_ms=e.actual_ms,
        )
        return JSONResponse(
            status_code=500,
            content={"error": "Clock moved backwards", "code": "CLOCK_BACKWARDS"},
        )
    except Exception as e:
        logger.error("generate_id_error", error=str(e))
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "code": "INTERNAL_ERROR"},
        )
