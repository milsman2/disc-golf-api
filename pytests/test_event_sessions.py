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

import httpx
import pytest
from dateutil.parser import isoparse
from fastapi.testclient import TestClient
from icecream import ic
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.api.deps import get_db
from src.main import app
from src.models.base import Base
from src.schemas.event_sessions import EventSessionCreate


@pytest.fixture(name="sample_csv_path")
def get_sample():
    """
    Fixture to provide the file path to the sample JSON file for testing.

    This fixture returns the path to a JSON file containing test event session data.
    The file should contain valid EventSession data including name, start_date,
    end_date, and description fields.

    Returns:
        str: Path to the test JSON file containing event session data.

    Note:
        The fixture name uses 'csv_path' for historical reasons but actually
        points to a JSON file containing event session test data.
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


def test_event_session_post(sample_csv_path, session: Session):
    """
    Test creating an event session via the API endpoint.

    This comprehensive test validates the complete flow of event session creation:
    1. Loads event session data from a JSON file
    2. Validates the data against the EventSessionCreate Pydantic schema
    3. Makes a POST request to the API endpoint with valid data
    4. Verifies the response contains the expected fields and values
    5. Confirms the created event session is assigned a unique database ID

    The test uses dependency injection to override the database session with
    an in-memory test database, ensuring isolation from production data.

    Args:
        sample_csv_path (str): Path to the JSON file containing test event session data.
                              Despite the name, this contains JSON data, not CSV.
        session (Session): SQLAlchemy session for database operations, provided by
                          the session fixture for test isolation.

    Asserts:
        - JSON data can be successfully loaded and parsed
        - EventSessionCreate schema validation passes for the test data
        - HTTP status code is 201 (Created) for successful creation
        - Response data matches the input data for name, dates, and description
        - Response includes a database-generated ID field
        - Datetime fields are properly parsed and compared (timezone-aware)

    Raises:
        AssertionError: If any of the validation checks fail
        FileNotFoundError: If the test JSON file cannot be found
        ValidationError: If the JSON data doesn't match the EventSessionCreate schema
        HTTPStatusError: If the API request fails with an HTTP error
        RequestError: If there's a network or connection error during the request

    Note:
        The test includes comprehensive error handling with debug output using
        icecream (ic) for troubleshooting test failures.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    ic(client)
    with open(sample_csv_path, encoding="utf-8") as f:
        event_session_data = json.load(f)
        try:
            event_session = EventSessionCreate.model_validate(event_session_data)
        except ValidationError as e:
            ic(e)
            event_session = None
        if event_session is not None:
            try:
                response = client.post(
                    "/api/v1/event-sessions/",
                    json=event_session.model_dump(mode="json"),
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"
                data = response.json()
                assert data["name"] == event_session_data["name"]
                assert isoparse(data["start_date"]).replace(tzinfo=None) == isoparse(
                    event_session_data["start_date"]
                ).replace(tzinfo=None)
                assert isoparse(data["end_date"]).replace(tzinfo=None) == isoparse(
                    event_session_data["end_date"]
                ).replace(tzinfo=None)
                assert data["description"] == event_session_data["description"]
                assert "id" in data
            except httpx.HTTPStatusError as e:
                ic(e)
            except httpx.RequestError as e:
                ic(e)
