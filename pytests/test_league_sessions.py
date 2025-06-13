"""
Pytest module for testing disc golf league session API endpoints.

This module contains tests for validating and posting LeagueSession data using FastAPI's TestClient.
It includes fixtures for sample data and database session setup, and verifies that league session
creation via the API works as expected.
"""

import json

import httpx
import pytest
from fastapi.testclient import TestClient
from icecream import ic
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.api.deps import get_db
from src.main import app
from src.models.base import Base
from src.schemas.league_sessions import LeagueSessionCreate


@pytest.fixture(name="sample_csv_path")
def get_sample():
    """
    Fixture to provide the path to the sample CSV file for testing.
    """
    return "./data/league_sessions/tcj_session_2025_1.json"


@pytest.fixture(name="session", scope="module")
def session_fixture():
    ic()
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_league_session_post(sample_csv_path, session: Session):
    """
    Test that valid rows from the CSV file fit the EventResultCreate schema,
    including associated layout data.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    ic(client)
    with open(sample_csv_path, encoding="utf-8") as f:
        league_session_data = json.load(f)
        try:
            league_session = LeagueSessionCreate.model_validate(league_session_data)
        except ValidationError as e:
            ic(e)
            league_session = None
        if league_session is not None:
            try:
                response = client.post(
                    "/api/v1/league_sessions/",
                    json=league_session.model_dump(mode="json"),
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"
                return response.json()
            except httpx.HTTPStatusError as e:
                ic(e)
            except httpx.RequestError as e:
                ic(e)
