"""
This file contains the Pydantic models for the CourseLayout model.
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from src.schemas.holes import Hole, HoleCreate


class CourseLayoutBase(BaseModel):
    name: str
    par: Optional[int] = None
    length: Optional[float] = None
    difficulty: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class CourseLayoutCreate(CourseLayoutBase):
    holes: List[HoleCreate] = []


class CourseLayoutInDBBase(CourseLayoutBase):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    course_id: Optional[int] = None


class CourseLayoutPublic(CourseLayoutInDBBase):
    holes: List[Hole] = []


class CourseLayoutsPublic(BaseModel):
    course_layouts: List[CourseLayoutPublic] = []
    count: int
