"""
This module contains tests for the courses endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import json
from src.api.deps import get_db
from src.main import app
from src.models.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    ic()
    db = TestingSessionLocal()
    yield db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db_setup():
    ic()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_course_from_file(test_db_setup):
    ic(test_db_setup)
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
        data["description"]
        == "Dual tees, short White tees have concrete pads, long Blue tees are on the grass. Mostly flat, lightly wooded. Good shade. New trees planted in early 2020."
    )
    assert data["city"] == "Houston"
    assert data["state"] == "Texas"
    assert data["country"] == "USA"
    assert data["holes"] == 21
    assert data["rating"] == 4.3
    assert data["reviews_count"] == 3834
    assert len(data["layouts"]) == 1
    assert data["layouts"][0]["name"] == "Full 21 - White Tees"
