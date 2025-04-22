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


@pytest.fixture(name="session")
def session_fixture():
    ic()
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


client = TestClient(app)


@pytest.fixture(name="sample_csv_path")
def get_sample():
    """
    Fixture to provide the path to the sample CSV file for testing.
    """
    return "./data/tc-jester-hfds-league-tc-jester-hfds-league-2025-03-19.csv"


def test_valid_event_result(sample_csv_path):
    """
    Test that valid rows from the CSV file fit the EventResultCreate schema.
    """
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
            "layout_id": 1,
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
        assert event_result.layout_id == data["layout_id"]
        response = client.post("/api/v1/event-results/", json=event_result.model_dump())
        response.raise_for_status()
        assert response.status_code == 200

        # Check if the response contains the expected data
        response_data = response.json()
        assert response_data["division"] == data["division"]
        assert response_data["position"] == data["position"]
        assert response_data["position_raw"] == data["position_raw"]
        assert response_data["name"] == data["name"]
        assert response_data["event_relative_score"] == data["event_relative_score"]
        assert response_data["event_total_score"] == data["event_total_score"]
        assert response_data["pdga_number"] == data["pdga_number"]
        assert response_data["username"] == data["username"]
        assert response_data["round_relative_score"] == data["round_relative_score"]
        assert response_data["round_total_score"] == data["round_total_score"]


def test_invalid_event_result():
    """
    Test that invalid rows raise validation errors.
    """
    invalid_data = {
        "division": "GOLD",
        "position": "1",
        "position_raw": "invalid",
        "name": "Andrew Zinck",
        "event_relative_score": -6,
        "event_total_score": 49,
        "pdga_number": "invalid",
        "username": "zinckles",
        "round_relative_score": -6,
        "round_total_score": 49,
        "course_id": 1,
        "layout_id": 2,
    }

    with pytest.raises(ValueError):
        EventResultCreate(**invalid_data)
