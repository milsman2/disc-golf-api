"""
This module contains tests for the courses endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
import json
from src.api.deps import get_db
from src.main import app
from src.models.base import Base


@pytest.fixture(name="session")
def session_fixture():
    ic()
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_course_from_file(session: Session):
    ic()

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)

    with open("data/t-c-jester-park-zVh6.json", encoding="utf-8") as f:
        course_data = json.load(f)

    course_data.pop("id", None)
    for layout in course_data["layouts"]:
        layout.pop("id", None)
        layout.pop("course_id", None)
        for hole in layout["holes"]:
            hole.pop("id", None)
            hole.pop("layout_id", None)

    response = client.post("/api/v1/courses/", json=course_data)
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
