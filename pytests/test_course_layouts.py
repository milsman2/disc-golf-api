"""
This module contains tests for the courses endpoints.
"""

import json

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
from src.schemas.courses import CourseCreate


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


def load_course_layout_data():
    """
    Loads and normalizes course data from the test JSON file.
    """
    with open("data/courses/t-c-jester-park-zVh6.json", encoding="utf-8") as f:
        course_data = json.load(f)
        try:
            course_data["layouts"] = [
                {
                    "name": layout["name"],
                    "par": layout["par"],
                    "length": layout["length"],
                    "holes": [
                        {
                            "hole_name": hole["hole_name"],
                            "par": hole["par"],
                            "distance": hole["distance"],
                        }
                        for hole in layout["holes"]
                    ],
                }
                for layout in course_data["layouts"]
            ]
        except KeyError as e:
            ic(f"KeyError: {e}")
            raise
        try:
            course_data = CourseCreate.model_validate(course_data)
            return course_data
        except ValidationError as e:
            ic(f"ValidationError: {e}")
            raise


def test_create_course(test_client):
    """
    Test creating a course.
    """
    course_data = load_course_layout_data()
    response = test_client.post("/api/v1/courses", json=course_data.model_dump())
    assert response.status_code == 201
