"""
Define relationships between models
"""

from sqlalchemy.orm import relationship

from src.models.course import Course
from src.models.course_layout import CourseLayout
from src.models.hole import Hole

course_layout_relationship = Course.layouts = relationship(
    "CourseLayout", back_populates="course"
)
course_hole_relationship = CourseLayout.course = relationship(
    "Course", back_populates="layouts"
)
layout_hole_relationship = CourseLayout.holes = relationship(
    "Hole", back_populates="layout"
)
Hole.layout = relationship("CourseLayout", back_populates="holes")
