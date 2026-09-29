"""Integration tests for HTTP endpoints."""

import time

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from generator.domain.ports.clock import IClock
from generator.domain.services.id_generator import IdGeneratorService
from generator.interfaces.http.router import router as http_router
from generator.interfaces.health.controller import router as health_router
from generator.interfaces.metrics.controller import router as metrics_router


class MockClock(IClock):
    """Mock clock for integration tests."""

    def __init__(self, time_ms: int | None = None) -> None:
        self._time_ms = time_ms or int(time.time() * 1000)

    def now_ms(self) -> int:
        current = self._time_ms
        self._time_ms += 1
        return current


@pytest.fixture
def app() -> FastAPI:
    """Create test FastAPI application."""
    test_app = FastAPI()
    test_app.state.datacenter_id = 1
    test_app.state.machine_id = 1
    test_app.state.id_generator = IdGeneratorService(
        clock=MockClock(),
        datacenter_id=1,
        machine_id=1,
    )
    test_app.include_router(http_router)
    test_app.include_router(health_router)
    test_app.include_router(metrics_router)
    return test_app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create test client."""
    return TestClient(app)


class TestGenerateEndpoint:
    """Tests for GET /generate endpoint."""

    def test_generate_returns_200(self, client: TestClient) -> None:
        """Test that /generate returns 200 OK."""
        response = client.get("/generate")
        assert response.status_code == 200

    def test_generate_returns_valid_json(self, client: TestClient) -> None:
        """Test that /generate returns valid JSON with 'id' field."""
        response = client.get("/generate")
        data = response.json()
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_generate_returns_64bit_integer(self, client: TestClient) -> None:
        """Test that generated ID is a valid 64-bit integer."""
        response = client.get("/generate")
        data = response.json()
        id_value = data["id"]
        assert 0 <= id_value < (1 << 64)

    def test_generate_ids_are_unique(self, client: TestClient) -> None:
        """Test that multiple calls return unique IDs."""
        ids = set()
        for _ in range(100):
            response = client.get("/generate")
            ids.add(response.json()["id"])
        assert len(ids) == 100

    def test_generate_contains_correct_components(self, client: TestClient) -> None:
        """Test that generated ID has correct datacenter and machine IDs."""
        response = client.get("/generate")
        data = response.json()
        id_value = data["id"]

        datacenter_id = (id_value >> 17) & 0x1F
        machine_id = (id_value >> 12) & 0x1F

        assert datacenter_id == 1
        assert machine_id == 1


class TestHealthEndpoint:
    """Tests for GET /health endpoint."""

    def test_health_returns_200(self, client: TestClient) -> None:
        """Test that /health returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_status_ok(self, client: TestClient) -> None:
        """Test that /health returns status: ok."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "ok"

    def test_health_returns_instance_info(self, client: TestClient) -> None:
        """Test that /health returns instance information."""
        response = client.get("/health")
        data = response.json()
        assert "instance" in data
        assert data["instance"] == "dc-1-machine-1"

    def test_health_returns_uptime(self, client: TestClient) -> None:
        """Test that /health returns uptime in seconds."""
        response = client.get("/health")
        data = response.json()
        assert "uptime_seconds" in data
        assert data["uptime_seconds"] >= 0


class TestMetricsEndpoint:
    """Tests for GET /metrics endpoint."""

    def test_metrics_returns_200(self, client: TestClient) -> None:
        """Test that /metrics returns 200 OK."""
        response = client.get("/metrics")
        assert response.status_code == 200

    def test_metrics_returns_prometheus_format(self, client: TestClient) -> None:
        """Test that /metrics returns Prometheus text format."""
        response = client.get("/metrics")
        assert "text/plain" in response.headers["content-type"] or "text/plain" in str(response.headers.get("content-type", ""))

    def test_metrics_contains_ids_generated_total(self, client: TestClient) -> None:
        """Test that /metrics contains ids_generated_total counter."""
        response = client.get("/metrics")
        content = response.text
        assert "ids_generated_total" in content

    def test_metrics_contains_request_duration(self, client: TestClient) -> None:
        """Test that /metrics contains request_duration_seconds."""
        response = client.get("/metrics")
        content = response.text
        assert "request_duration_seconds" in content


class TestEndToEnd:
    """End-to-end tests for the complete flow."""

    def test_full_generation_flow(self, client: TestClient) -> None:
        """Test the complete ID generation flow."""
        health_response = client.get("/health")
        assert health_response.status_code == 200

        generate_response = client.get("/generate")
        assert generate_response.status_code == 200
        generated_id = generate_response.json()["id"]

        metrics_response = client.get("/metrics")
        assert metrics_response.status_code == 200

        assert 0 <= generated_id < (1 << 64)
