"""
Unit tests for disc event endpoints.

This module tests the creation, retrieval, and deletion of disc events via the API.
"""

from datetime import datetime as _dt
from datetime import timezone as _tz

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
def test_client_fixture(test_session):
    """
    Provides a TestClient with the session dependency overridden.
    Automatically commits the session after each request to ensure data is visible.
    """

    def get_session_override():
        return test_session

    app.dependency_overrides[get_db] = get_session_override
    test_client = TestClient(app)

    # Patch the request method to commit after each request
    orig_request = test_client.request

    def request_with_commit(*args, **kwargs):
        response = orig_request(*args, **kwargs)
        test_session.commit()
        return response

    test_client.request = request_with_commit

    return test_client


def test_create_disc_event(test_client):
    """
    Test creating a disc event.
    """
    event_data = {
        "name": "Test Disc Event",
        "start_date": "2025-10-11T00:00:00Z",
        "end_date": "2025-10-12T00:00:00Z",
        "description": "A test event for disc golf.",
    }
    response = test_client.post("/api/v1/disc-events/", json=event_data)
    if response.status_code == 422:
        print("Create Disc Event 422 Response:", response.json())
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["name"] == event_data["name"]
    assert data["description"] == event_data["description"]


def test_get_disc_event(test_client):
    """
    Test retrieving a disc event by ID.
    """
    event_data = {
        "name": "Get Disc Event",
        "start_date": "2025-10-12T00:00:00Z",
        "end_date": "2025-10-13T00:00:00Z",
        "description": "Another test event.",
    }
    create_response = test_client.post("/api/v1/disc-events/", json=event_data)
    print("POST create_response:", create_response.status_code, create_response.json())
    if create_response.status_code == 422:
        print("Get Disc Event 422 Response:", create_response.json())
    assert create_response.status_code in (200, 201)
    event_id = create_response.json()["id"]
    print("Event ID used for GET:", event_id)
    get_response = test_client.get(f"/api/v1/disc-events/id/{event_id}")
    if get_response.status_code == 404:
        print("Get Disc Event 404 Response:", get_response.json())
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == event_id
    assert data["name"] == event_data["name"]


def test_delete_disc_event(test_client):
    """
    Test deleting a disc event.
    """
    event_data = {
        "name": "Delete Disc Event",
        "start_date": "2025-10-13T00:00:00Z",
        "end_date": "2025-10-14T00:00:00Z",
        "description": "Event to be deleted.",
    }
    create_response = test_client.post("/api/v1/disc-events/", json=event_data)
    print("POST create_response:", create_response.status_code, create_response.json())
    if create_response.status_code == 422:
        print("Delete Disc Event 422 Response:", create_response.json())
    assert create_response.status_code in (200, 201)
    event_id = create_response.json()["id"]
    print("Event ID used for DELETE:", event_id)
    delete_response = test_client.delete(f"/api/v1/disc-events/id/{event_id}")
    if delete_response.status_code == 404:
        print("Delete Disc Event 404 Response:", delete_response.json())
    assert delete_response.status_code in (200, 204)
    get_response = test_client.get(f"/api/v1/disc-events/id/{event_id}")
    if get_response.status_code == 404:
        print("Get After Delete 404 Response:", get_response.json())
    assert get_response.status_code == 404


def test_partial_update_disc_event(test_client):
    """
    Test that updating a single field on a DiscEvent works
    and other fields remain unchanged.
    """
    event_data = {
        "name": "Partial Update Event",
        "start_date": "2025-10-20T00:00:00Z",
        "end_date": "2025-10-21T00:00:00Z",
        "description": "Original description",
    }
    create_response = test_client.post("/api/v1/disc-events/", json=event_data)
    assert create_response.status_code in (200, 201)
    event_id = create_response.json()["id"]

    # Partial update: only change description
    patch_data = {"description": "Updated description only"}
    update_response = test_client.put(
        f"/api/v1/disc-events/id/{event_id}", json=patch_data
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["description"] == "Updated description only"
    # Ensure other fields remain unchanged
    assert updated["name"] == event_data["name"]
    # Normalize ISO timestamps (server may strip trailing Z / timezone representation)

    def _norm(iso_str: str) -> _dt:
        dt = _dt.fromisoformat(iso_str.replace("Z", "+00:00"))
        # ensure aware UTC for comparison
        if dt.tzinfo is None:
            return dt.replace(tzinfo=_tz.utc)
        return dt.astimezone(_tz.utc)

    assert _norm(updated["start_date"]) == _norm(event_data["start_date"])
    assert _norm(updated["end_date"]) == _norm(event_data["end_date"])
