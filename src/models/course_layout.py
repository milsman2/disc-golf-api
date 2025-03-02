"""
CourseLayout model for disc golf course layouts
"""

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
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
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("courses.id"), nullable=False
    )
    par: Mapped[int | None] = mapped_column(Integer, nullable=True)
    length: Mapped[float | None] = mapped_column(Float, nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String, nullable=True)
    course: Mapped["CourseLayout"] = relationship("Course", back_populates="layouts")
    holes: Mapped[list["Hole"]] = relationship("Hole", back_populates="layout")
