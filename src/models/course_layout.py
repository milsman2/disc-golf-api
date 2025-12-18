"""
CourseLayout model for disc golf course layouts
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.course import Course
    from src.models.event_result import EventResult
    from src.models.hole import Hole


class CourseLayout(Base):
    """
    SQL model for disc golf course layouts
    """

    __tablename__ = "course_layouts"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    par: Mapped[int | None] = mapped_column(Integer, nullable=True)
    length: Mapped[float | None] = mapped_column(Float, nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String, nullable=True)

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    course: Mapped["Course"] = relationship("Course", back_populates="layouts")
    holes: Mapped[list["Hole"]] = relationship(
        "Hole", back_populates="layout", cascade="all, delete-orphan"
    )
    event_results: Mapped[list["EventResult"]] = relationship(
        "EventResult", back_populates="course_layout"
    )
