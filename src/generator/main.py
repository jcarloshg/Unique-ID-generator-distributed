"""Unique ID Generator - Main Entry Point."""

import os
import structlog
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import uvicorn
from fastapi import FastAPI

from generator.domain.services.id_generator import IdGeneratorService
from generator.interfaces.http.router import router as http_router
from generator.interfaces.health.controller import router as health_router
from generator.interfaces.metrics.controller import router as metrics_router
from generator.infrastructure.adapters.system_clock import SystemClock

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

dc_id = int(os.getenv("DATACENTER_ID", "1"))
machine_id = int(os.getenv("MACHINE_ID", "1"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger = structlog.get_logger()
    logger.info(
        "generator_starting",
        datacenter_id=dc_id,
        machine_id=machine_id,
    )
    app.state.id_generator = IdGeneratorService(
        clock=SystemClock(),
        datacenter_id=dc_id,
        machine_id=machine_id,
    )
    yield
    logger.info("generator_stopping")


app = FastAPI(
    title="Unique ID Generator",
    version="0.1.0",
    lifespan=lifespan,
)
app.state.datacenter_id = dc_id
app.state.machine_id = machine_id

app.include_router(http_router)
app.include_router(health_router)
app.include_router(metrics_router)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    uvicorn.run("generator.main:app", host="0.0.0.0", port=port, reload=False)
