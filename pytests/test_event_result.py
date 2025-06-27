"""
Unit tests for the EventResultCreate schema.

This module contains tests to validate that data from a CSV file fits the
EventResultCreate schema. It ensures that valid data passes schema validation
and invalid data raises appropriate errors.

Tests:
- test_valid_event_result_with_layouts: Validates rows from the CSV file
against the schema and API.
- test_invalid_league_session_id: Ensures invalid league_session_id returns
a 422 error.

Dependencies:
- pandas: Used to read and process the CSV file.
- pytest: Used as the testing framework.
"""

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from icecream import ic
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
    Fixture to create a TestClient with a session override for testing.
    This allows the tests to use the in-memory SQLite database.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    return TestClient(app)


@pytest.fixture(name="sample_league_session_id")
def league_session_id(sample_client):
    """
    Fixture to create a league session and return its ID.
    """
    data = {
        "name": "Test League Session",
        "start_date": "2025-03-01T00:00:00Z",
        "end_date": "2025-04-01T00:00:00Z",
        "description": "Test session",
    }
    response = sample_client.post("/api/v1/league_sessions/", json=data)
    assert response.status_code in (200, 201)
    return response.json()["id"]


@pytest.fixture(name="sample_csv_path")
def get_sample():
    """
    Fixture to provide the path to the sample CSV file for testing.
    """
    return "./data/event_results/tc-jester-hfds-league-2025-03-12.csv"


def test_valid_event_result_with_layouts(
    sample_csv_path, sample_client, sample_league_session_id
):
    """
    Test that valid rows from the CSV file fit the EventResultCreate schema,
    including associated layout data and a valid league_session_id.
    """
    ic(sample_client)
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
            "league_session_id": sample_league_session_id,
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
            "/api/v1/event-results/",
            json=event_result.model_dump(mode="json", exclude_none=True),
        )
        assert response.status_code == 200
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


def test_invalid_league_session_id(sample_client):
    """
    Test that creating an EventResult with a non-existent league_session_id returns 422.
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
        "league_session_id": 99999,  # Non-existent league_session_id
    }

    response = sample_client.post(
        "/api/v1/event-results/",
        json=event_result_data,
    )
    assert response.status_code == 422
    assert "does not exist" in response.json()["detail"]
