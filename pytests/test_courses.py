"""
This module contains tests for the courses endpoints.
"""

import json

from pydantic import ValidationError
import pytest
from fastapi.testclient import TestClient
from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.api.deps import get_db
from src.main import app
from src.models.base import Base
from src.schemas.courses import CourseCreate
from pydantic import ValidationError


@pytest.fixture(scope="module", name="session")
def session_fixture():
    """
    Create a shared in-memory SQLite database session for the test suite.
    """
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_course(session: Session):
    """
    Test creating a course.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    ic(client)

    with open("data/t-c-jester-park-zVh6.json", encoding="utf-8") as f:
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
            course_test = CourseCreate.model_validate(course_data)
        except ValidationError as e:
            ic(f"ValidationError: {e}")
            raise

        response = client.post("/api/v1/courses/", json=course_test.model_dump())
        assert response.status_code == 200


def test_get_course(session: Session):
    """
    Test retrieving a course.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)

    response = client.get("/api/v1/courses/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "T.C. Jester Park"
    assert data["location"] == "Houston, TX"
    assert (
        data["description"] == "Dual tees, short White tees have concrete pads, "
        "long Blue tees are on the grass. "
        "Mostly flat, lightly wooded. Good shade. New trees planted in early 2020."
    )
    assert data["city"] == "Houston"
    assert data["state"] == "Texas"
    assert data["country"] == "USA"
    assert data["holes"] == 21
    assert data["rating"] == 4.3
    assert data["reviews_count"] == 3834
    assert len(data["layouts"]) == 2
    assert data["layouts"][0]["name"] == "Full 21 - White Tees"
    assert data["layouts"][0]["par"] == 64
    assert data["layouts"][0]["length"] == 6619
    assert data["layouts"][1]["name"] == "North 13 - White Tees"
    assert data["layouts"][1]["par"] == 40
    assert data["layouts"][1]["length"] == 4204
