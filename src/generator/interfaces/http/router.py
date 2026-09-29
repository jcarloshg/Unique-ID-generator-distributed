"""HTTP Router - Transport Layer."""

import structlog
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response

from generator.domain.services.id_generator import ClockBackwardsError

logger = structlog.get_logger()

router = APIRouter(prefix="", tags=["id"])


@router.get("/generate")
async def generate_id(request: Request) -> Response:
    """Generate a unique Snowflake ID.

    Returns:
        JSON response with 64-bit unique ID

    Raises:
        500: If clock moved backwards or other error
    """
    try:
        snowflake_id = request.app.state.id_generator.generate_id()

        if request.app.state.write_queue:
            request.app.state.write_queue.enqueue(snowflake_id)

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
