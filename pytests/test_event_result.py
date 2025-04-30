"""
Unit tests for the EventResultCreate schema.

This module contains tests to validate that data from a CSV file fits the
EventResultCreate schema. It ensures that valid data passes schema validation
and invalid data raises appropriate errors.

Tests:
- test_valid_event_result: Validates rows from the CSV file against the schema.
- test_invalid_event_result: Ensures invalid data raises validation errors.

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

from src.main import app
from src.models.base import Base
from src.schemas.event_results import EventResultCreate
from src.api.deps import get_db


@pytest.fixture(name="session", scope="module")
def session_fixture():
    ic()
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="sample_csv_path")
def get_sample():
    """
    Fixture to provide the path to the sample CSV file for testing.
    """
    return "./data/tc-jester-hfds-league-tc-jester-hfds-league-2025-03-19.csv"


def test_valid_event_result_with_layouts(sample_csv_path, session: Session):
    """
    Test that valid rows from the CSV file fit the EventResultCreate schema,
    including associated layout data.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    ic(client)
    df = pd.read_csv(sample_csv_path)

    for _, row in df.iterrows():
        data = {
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
        }

        event_result = EventResultCreate(**data)

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
        response = client.post(
            "/api/v1/event-results/",
            json=event_result.model_dump(),
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
