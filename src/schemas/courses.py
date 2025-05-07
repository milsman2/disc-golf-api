"""
This file contains the Pydantic models for the Course model.
"""

from pydantic import BaseModel, ConfigDict

from src.schemas.course_layouts import CourseLayoutCreate, CourseLayoutPublic


class CourseBase(BaseModel):
    """
    Course base schema
    """

    name: str
    location: str | None = None
    description: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    holes: int | None = None
    rating: float | None = None
    reviews_count: int | None = None
    link: str | None = None
    conditions: str | None = None
    conditions_updated: str | None = None

    model_config = ConfigDict(extra="forbid")


class CourseCreate(CourseBase):
    layouts: list[CourseLayoutCreate] = []


class CourseInDBBase(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CoursePublic(CourseInDBBase):
    layouts: list[CourseLayoutPublic] = []


class CoursesPublic(BaseModel):
    courses: list[CoursePublic] = []
