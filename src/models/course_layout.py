"""
SQLAlchemy model for course layouts.

This module defines the `CourseLayout` model, which represents different layouts
of a disc golf course. Each layout belongs to a specific course and can have
multiple holes and event results associated with it.

Classes:
- CourseLayout: Represents a layout of a disc golf course.

Relationships:
- `course`: Links the layout to its parent course.
- `event_results`: Links the layout to the event results played on it.
- `holes`: Links the layout to the holes it contains.

Dependencies:
- SQLAlchemy ORM: Used for defining the model and relationships.
- src.models.base: Base class for all SQLAlchemy models.
- src.models.course: Defines the `Course` model.
- src.models.event_result: Defines the `EventResult` model.
- src.models.hole: Defines the `Hole` model.
"""

from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.event_result import EventResult
    from src.models.course import Course
    from src.models.hole import Hole


class CourseLayout(Base):
    """
    SQLAlchemy model for course layouts.
    """

    __tablename__ = "course_layouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("courses.id"), nullable=False
    )

    course: Mapped["Course"] = relationship("Course", back_populates="layouts")

    event_results: Mapped[list["EventResult"]] = relationship(
        "EventResult", back_populates="layout", cascade="all, delete-orphan"
    )
    holes: Mapped[list["Hole"]] = relationship(
        "Hole", back_populates="layout", cascade="all, delete-orphan"
    )
