from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.schemas import holes

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
