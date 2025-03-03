"""
This file contains the Pydantic models for the Course model.
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from src.schemas.course_layouts import CourseLayout, CourseLayoutCreate


class CourseBase(BaseModel):
    name: str
    location: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    holes: Optional[int] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None


class CourseCreate(CourseBase):
    layouts: List[CourseLayoutCreate] = []


class CourseInDBBase(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Course(CourseInDBBase):
    layouts: List[CourseLayout] = []
