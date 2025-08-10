"""
Unit tests for disc golf event session API endpoints.

This module contains comprehensive tests for validating EventSession data models
and testing the event session API endpoints using FastAPI's TestClient. It includes
fixtures for test data loading, database session setup, and verifies that event
session creation, validation, and API responses work as expected.

The tests use an in-memory SQLite database for isolation and include fixtures
for JSON data loading and database session management.

Tests:
- test_event_session_post: Validates JSON data against the EventSessionCreate
  schema and tests successful API creation with proper field validation.

Dependencies:
- json: For loading test data from JSON files.
- httpx: For HTTP client functionality and error handling.
- pytest: Testing framework with fixtures for database and client setup.
- dateutil: For parsing and comparing ISO datetime strings.
- FastAPI TestClient: For simulating HTTP requests to API endpoints.
- SQLAlchemy: For in-memory database session management during tests.
"""

import json

import pytest
from dateutil.parser import isoparse
from fastapi.testclient import TestClient
from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.api.deps import get_db
from src.main import app
from src.models.base import Base
from src.schemas.event_sessions import EventSessionCreate


@pytest.fixture(name="sample_json_path")
def get_sample():
    """
    Fixture to provide the file path to the sample JSON file for testing.

    This fixture returns the path to a JSON file containing test event session data.
    The file should contain valid EventSession data including name, start_date,
    end_date, and description fields.

    Returns:
        str: Path to the test JSON file containing event session data.
    """
    return "./data/event_sessions/tcj_session_2025_1.json"


@pytest.fixture(name="session", scope="module")
def session_fixture():
    """
    Fixture to provide a SQLAlchemy session with an in-memory SQLite database.

    Creates a temporary database for the duration of the test module, ensuring
    test isolation and preventing interference with production data. All database
    tables are created from the SQLAlchemy models defined in the application.

    The fixture uses module scope to share the same database session across all
    tests in this module, which improves performance and allows for test data
    to persist between individual test functions if needed.

    Yields:
        Session: SQLAlchemy session connected to the in-memory test database.

    Note:
        The in-memory database is automatically destroyed when the test module
        completes, ensuring no persistent state between test runs.
    """
    ic()
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="sample_client")
def client(session):
    """
    Fixture to create a TestClient with database session dependency override.

    This fixture sets up a FastAPI TestClient that uses the in-memory test database
    instead of the production database. It overrides the get_db dependency to ensure
    all API calls during testing use the same test database session.

    Args:
        session: The SQLAlchemy session fixture for the test database.

    Returns:
        TestClient: Configured FastAPI test client with database override.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    return TestClient(app)


def test_event_session_post(sample_json_path, sample_client: TestClient):
    """
    Test creating event sessions from JSON data with validation and duplicate checking.

    This test validates that:
    1. JSON data can be successfully parsed and converted to EventSessionCreate objects
    2. Schema validation passes for all required fields
    3. API POST requests succeed with valid data
    4. Response data matches the input data for all fields
    5. Duplicate event session names are properly rejected with 409 status
    6. Date parsing and comparison work correctly

    Args:
        sample_json_path (str): Path to the JSON file containing event session data
        session (Session): SQLAlchemy session for database operations
        sample_client (TestClient): FastAPI test client with database override

    Asserts:
        - Schema validation succeeds for JSON data
        - API returns 201 status code for successful creation
        - Response data matches input data for all fields
        - Date fields are properly parsed and formatted
        - Duplicate names return 409 Conflict status
    """
    # Load and validate the event session data
    with open(sample_json_path, encoding="utf-8") as f:
        event_session_data = json.load(f)

    event_session = EventSessionCreate.model_validate(event_session_data)

    assert event_session.name == event_session_data["name"]
    assert event_session.description == event_session_data["description"]

    expected_start = isoparse(event_session_data["start_date"])
    expected_end = isoparse(event_session_data["end_date"])
    assert event_session.start_date == expected_start
    assert event_session.end_date == expected_end

    # Test successful creation
    response = sample_client.post(
        "/api/v1/event-sessions/",
        json=event_session.model_dump(mode="json"),
    )
    assert response.status_code == 201

    # Verify response data matches input
    response_data = response.json()
    assert response_data["name"] == event_session_data["name"]
    assert response_data["description"] == event_session_data["description"]

    # Compare dates by converting both to the same timezone-aware format
    response_start = isoparse(response_data["start_date"])
    response_end = isoparse(response_data["end_date"])

    # Convert to UTC for comparison if needed
    if expected_start.tzinfo and not response_start.tzinfo:
        response_start = response_start.replace(tzinfo=expected_start.tzinfo)
    if expected_end.tzinfo and not response_end.tzinfo:
        response_end = response_end.replace(tzinfo=expected_end.tzinfo)

    assert response_start == expected_start
    assert response_end == expected_end
    assert "id" in response_data

    # Test duplicate name rejection
    duplicate_response = sample_client.post(
        "/api/v1/event-sessions/",
        json=event_session.model_dump(mode="json"),
    )
    assert duplicate_response.status_code == 409
    assert "already exists" in duplicate_response.json()["detail"]
    assert event_session.name in duplicate_response.json()["detail"]
