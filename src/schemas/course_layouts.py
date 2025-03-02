"""
Schema for Course Layouts
"""

from pydantic import BaseModel
from typing import Optional, List
from src.schemas.holes import Hole


class CourseLayoutBase(BaseModel):
    name: str
    par: Optional[int] = None
    length: Optional[float] = None
    difficulty: Optional[str] = None


class CourseLayoutCreate(CourseLayoutBase):
    course_id: int


class CourseLayoutUpdate(CourseLayoutBase):
    pass


class CourseLayoutInDBBase(CourseLayoutBase):
    id: int
    course_id: int

    class Config:
        orm_mode = True


class CourseLayout(CourseLayoutInDBBase):
    holes: List[Hole] = []


class CourseLayoutInDB(CourseLayoutInDBBase):
    pass
