"""
Test response validation for all API endpoints to ensure they match their schemas.

This test suite validates that all GET endpoints return responses that conform
to their declared Pydantic response models, catching validation errors early.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.api.deps import get_db
from src.main import app
from src.models.base import Base


@pytest.fixture(scope="module", name="test_session")
def test_session_fixture():
    """
    Create a shared in-memory SQLite database session for the test suite.
    """
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as test_session:
        yield test_session


@pytest.fixture(name="test_client")
def client(test_session):
    """
    Provides a TestClient with the session dependency overridden.
    """

    def get_session_override():
        return test_session

    app.dependency_overrides[get_db] = get_session_override
    return TestClient(app)


def test_course_layouts_empty_response(test_client):
    """
    Test that GET /course-layouts returns correct schema structure even when empty.

    This test specifically validates the fix for the ResponseValidationError
    that occurred when returning an empty list instead of proper schema structure.
    """
    response = test_client.get("/api/v1/course-layouts/")
    assert response.status_code == 200

    data = response.json()
    assert "course_layouts" in data
    assert "count" in data
    assert isinstance(data["course_layouts"], list)
    assert isinstance(data["count"], int)
    assert data["count"] == len(data["course_layouts"])


def test_courses_empty_response(test_client):
    """
    Test that GET /courses returns correct schema structure when empty.
    """
    response = test_client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert "courses" in data
    assert isinstance(data["courses"], list)


def test_event_results_empty_response(test_client):
    """
    Test that GET /event-results handles empty data correctly.
    """
    response = test_client.get("/api/v1/event-results/")
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        assert "event_results" in data or "grouped" in data


def test_event_results_grouped_response(test_client):
    """
    Test that GET /event-results with grouping returns correct structure.
    """
    response = test_client.get("/api/v1/event-results/?group_by_division=true")
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        assert "grouped" in data
        assert isinstance(data["grouped"], list)


def test_disc_events_response(test_client):
    """
    Test that GET /disc-events returns correct list structure.
    """
    response = test_client.get("/api/v1/disc-events/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.parametrize(
    "endpoint",
    [
        "/api/v1/courses/",
        "/api/v1/course-layouts/",
        "/api/v1/disc-events/",
    ],
)
def test_pagination_parameters(test_client, endpoint):
    """
    Test that pagination parameters work correctly and don't break response validation.
    """
    response = test_client.get(f"{endpoint}?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data is not None


@pytest.mark.parametrize(
    "endpoint,expected_fields",
    [
        ("/api/v1/courses/", ["courses"]),
        ("/api/v1/course-layouts/", ["course_layouts", "count"]),
    ],
)
def test_response_schema_fields(test_client, endpoint, expected_fields):
    """
    Test that specific endpoints return responses with expected fields.
    """
    response = test_client.get(endpoint)
    assert response.status_code == 200
    data = response.json()
    for field in expected_fields:
        assert field in data, f"Field '{field}' missing from {endpoint} response"


def test_event_results_by_username_response(test_client):
    """
    Test that GET /event-results/username/{username} returns correct structure.
    """
    response = test_client.get("/api/v1/event-results/username/testuser")
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        assert "event_results" in data
        assert isinstance(data["event_results"], list)


def test_course_layouts_search_response(test_client):
    """
    Test that GET /course-layouts/search returns correct schema structure.

    This test specifically validates the fix for the search endpoint that was
    returning raw layout lists instead of proper schema structure.
    """
    response = test_client.get("/api/v1/course-layouts/search?name=test")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "course_layouts" in data
        assert "count" in data
        assert isinstance(data["course_layouts"], list)
        assert isinstance(data["count"], int)
        assert data["count"] == len(data["course_layouts"])


def test_search_endpoints_validation(test_client):
    """
    Test search endpoints return correct structure.
    """
    response = test_client.get("/api/v1/course-layouts/search?name=test")
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        assert "course_layouts" in data
        assert "count" in data


def test_invalid_ids_return_404(test_client):
    """
    Test that requesting non-existent resources returns 404, not validation errors.
    """
    endpoints_with_ids = [
        "/api/v1/courses/id/99999",
        "/api/v1/course-layouts/id/99999",
        "/api/v1/disc-events/id/99999",
        "/api/v1/event-results/id/99999",
    ]

    for endpoint in endpoints_with_ids:
        response = test_client.get(endpoint)
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data


def test_response_content_type(test_client):
    """
    Test that all endpoints return proper JSON content type.
    """
    endpoints = [
        "/api/v1/courses/",
        "/api/v1/course-layouts/",
        "/api/v1/disc-events/",
    ]

    for endpoint in endpoints:
        response = test_client.get(endpoint)
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")
