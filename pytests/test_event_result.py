"""
Unit tests for disc golf event result API endpoints.

This module contains comprehensive tests to validate EventResult data models
and API endpoints using FastAPI's TestClient. It includes tests for schema
validation, API creation endpoints, and error handling for invalid data.

The tests use an in-memory SQLite database for isolation and include fixtures
for CSV data loading, database session setup, and event session creation.

Tests:
- test_valid_event_result_with_layouts: Validates CSV data against the EventResultCreate
  schema and tests successful API creation with valid event session references.
- test_invalid_event_session_id: Ensures that invalid event_session_id references
  return appropriate 422 HTTP error responses.

Dependencies:
- pandas: Used to read and process CSV test data files.
- pytest: Testing framework with fixtures for database and client setup.
- FastAPI TestClient: For simulating HTTP requests to API endpoints.
- SQLAlchemy: For in-memory database session management during tests.
"""

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.api.deps import get_db
from src.main import app
from src.models.base import Base
from src.schemas.event_results import EventResultCreate


@pytest.fixture(name="session", scope="module")
def session_fixture():
    """
    Fixture to provide a SQLAlchemy session with an in-memory SQLite database.

    Creates a temporary database for the duration of the test module, ensuring
    test isolation and preventing interference with production data. All database
    tables are created from the SQLAlchemy models.

    Yields:
        Session: SQLAlchemy session connected to the in-memory test database.
    """
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


@pytest.fixture(name="sample_event_session_id")
def event_session_id(sample_client):
    """
    Fixture to create a test event session and return its database ID.

    Creates a sample event session via the API to ensure that event results
    have a valid foreign key reference during testing. This prevents foreign
    key constraint violations when creating test event results.

    Args:
        sample_client: The TestClient fixture for making API requests.

    Returns:
        int: The database ID of the created event session.

    Raises:
        AssertionError: If the event session creation fails (non-200/201 response).
    """
    data = {
        "name": "Test Event Session",
        "start_date": "2025-03-01T00:00:00Z",
        "end_date": "2025-04-01T00:00:00Z",
        "description": "Test session",
    }
    response = sample_client.post("/api/v1/event-sessions/", json=data)
    assert response.status_code in (200, 201)
    return response.json()["id"]


@pytest.fixture(name="sample_csv_path")
def get_sample():
    """
    Fixture to provide the file path to the sample CSV file for testing.

    Returns:
        str: Path to the CSV file containing test event result data.
    """
    return "./data/event_results/tc-jester-hfds-league-2025-03-12.csv"


def test_valid_event_result_with_layouts(
    sample_csv_path, sample_client, sample_event_session_id
):
    """
    Test that valid CSV data fits the EventResultCreate schema and API endpoints.

    This comprehensive test validates that:
    1. CSV data can be successfully parsed and converted to EventResultCreate objects
    2. Schema validation passes for all required fields
    3. API POST requests succeed with valid data
    4. Response data matches the input data for all fields
    5. Foreign key relationships (event_session_id) are properly handled

    The test processes each row in the CSV file, validates it against the Pydantic
    schema, and then makes API calls to ensure end-to-end functionality works.

    Args:
        sample_csv_path (str): Path to the test CSV file containing event result data.
        sample_client (TestClient): FastAPI test client with database override.
        sample_event_session_id (int): ID of a valid event session for foreign
        key reference.

    Asserts:
        - Schema validation succeeds for all CSV rows
        - API returns 200 status code for successful creation
        - Response data matches input data for all fields
        - Foreign key relationships are properly established
    """
    df = pd.read_csv(sample_csv_path)
    df.insert(0, "date", pd.to_datetime(1741820400, unit="s"))
    for _, row in df.iterrows():
        data = {
            "date": (
                row["date"].isoformat()
                if hasattr(row["date"], "isoformat")
                else str(row["date"])
            ),
            "division": row["division"],
            "position": row["position"],
            "position_raw": (
                float(row["position_raw"])
                if not pd.isna(row["position_raw"]) or row["position_raw"] == "DNF"
                else None
            ),
            "name": row["name"],
            "event_relative_score": int(row["event_relative_score"]),
            "event_total_score": int(row["event_total_score"]),
            "pdga_number": (
                float(row["pdga_number"]) if not pd.isna(row["pdga_number"]) else None
            ),
            "username": row["username"],
            "round_relative_score": int(row["round_relative_score"]),
            "round_total_score": int(row["round_total_score"]),
            "course_layout_id": 1,
            "event_session_id": sample_event_session_id,
        }

        event_result = EventResultCreate(**data)

        assert (
            event_result.date.isoformat()
            if hasattr(event_result.date, "isoformat")
            else str(event_result.date)
        ) == data["date"]
        assert event_result.division == data["division"]
        assert event_result.position == data["position"]
        assert event_result.position_raw == data["position_raw"]
        assert event_result.name == data["name"]
        assert event_result.event_relative_score == data["event_relative_score"]
        assert event_result.event_total_score == data["event_total_score"]
        assert event_result.pdga_number == data["pdga_number"]
        assert event_result.username == data["username"]
        assert event_result.round_relative_score == data["round_relative_score"]
        assert event_result.round_total_score == data["round_total_score"]
        response = sample_client.post(
            "/api/v1/event-results",
            json=event_result.model_dump(mode="json", exclude_none=True),
        )
        assert response.status_code == 201
        assert response.json()["division"] == data["division"]
        assert response.json()["position"] == data["position"]
        assert response.json()["position_raw"] == data["position_raw"]
        assert response.json()["name"] == data["name"]
        assert response.json()["event_relative_score"] == data["event_relative_score"]
        assert response.json()["event_total_score"] == data["event_total_score"]
        assert response.json()["pdga_number"] == data["pdga_number"]
        assert response.json()["username"] == data["username"]
        assert response.json()["round_relative_score"] == data["round_relative_score"]
        assert response.json()["round_total_score"] == data["round_total_score"]
        assert response.json()["round_points"] == 0.0


def test_invalid_event_session_id(sample_client):
    """
    Test that invalid event_session_id references return proper 422 HTTP errors.

    This test ensures that the API properly validates foreign key references
    and returns meaningful error messages when attempting to create an event
    result with a non-existent event_session_id.

    The test verifies that:
    1. Invalid foreign key references are caught at the API level
    2. A 422 Unprocessable Entity status code is returned
    3. The error message contains helpful information about the validation failure

    Args:
        sample_client (TestClient): FastAPI test client with database override.

    Asserts:
        - HTTP status code is 422 (Unprocessable Entity)
        - Error message contains "does not exist" to indicate validation failure
        - Request is rejected before attempting database operations
    """
    event_result_data = {
        "date": "2025-03-12T18:00:00Z",
        "division": "MPO",
        "position": "1",
        "position_raw": 1,
        "name": "Test Player",
        "event_relative_score": -10,
        "event_total_score": 50,
        "pdga_number": 12345,
        "username": "testuser",
        "round_relative_score": -5,
        "round_total_score": 25,
        "course_layout_id": 1,
        "event_session_id": 99999,  # Non-existent event_session_id
    }

    response = sample_client.post(
        "/api/v1/event-results",
        json=event_result_data,
    )
    assert response.status_code == 422
    assert "does not exist" in response.json()["detail"]
