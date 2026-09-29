"""Metrics Controller - Transport Layer."""

from prometheus_client import CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response

router = APIRouter(tags=["metrics"])

ids_generated_total = 0
request_duration_seconds_sum = 0.0
request_duration_seconds_count = 0


@router.get("/metrics")
async def metrics() -> Response:
    """Prometheus metrics endpoint.

    Returns:
        Prometheus-formatted metrics
    """
    global ids_generated_total, request_duration_seconds_sum, request_duration_seconds_count

    output = [
        "# HELP ids_generated_total Total number of IDs generated",
        "# TYPE ids_generated_total counter",
        f"ids_generated_total {ids_generated_total}",
        "# HELP request_duration_seconds Time spent processing requests",
        "# TYPE request_duration_seconds summary",
        f"request_duration_seconds_sum {request_duration_seconds_sum}",
        f"request_duration_seconds_count {request_duration_seconds_count}",
    ]

    return Response(
        content="\n".join(output),
        media_type=CONTENT_TYPE_LATEST,
    )


def increment_ids_generated() -> None:
    """Increment the IDs generated counter."""
    global ids_generated_total
    ids_generated_total += 1


def observe_request_duration(duration: float) -> None:
    """Record a request duration observation."""
    global request_duration_seconds_sum, request_duration_seconds_count
    request_duration_seconds_sum += duration
    request_duration_seconds_count += 1
