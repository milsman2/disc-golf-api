"""
This file contains the Pydantic models for the CourseLayout model.
"""

from pydantic import BaseModel, ConfigDict

from src.schemas.holes import HoleCreate, HolePublic


class CourseLayoutBase(BaseModel):
    name: str
    par: int | None = None
    length: float | None = None
    difficulty: str | None = None

    model_config = ConfigDict(extra="forbid")


class CourseLayoutCreate(CourseLayoutBase):
    holes: list[HoleCreate] = []


class CourseLayoutInDBBase(CourseLayoutBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int | None = None


class CourseLayoutPublic(CourseLayoutInDBBase):
    holes: list[HolePublic] = []


class CourseLayoutsPublic(BaseModel):
    course_layouts: list[CourseLayoutPublic] = []
    count: int
