"""
Hole model for disc golf course holes
"""

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.models.base import Base
from src.models.course_layout import CourseLayout


class Hole(Base):
    """
    SQL model for disc golf course holes
    """

    __tablename__ = "holes"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, nullable=False, autoincrement=True
    )
    layout_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("course_layouts.id"), nullable=False
    )
    hole_number: Mapped[int] = mapped_column(Integer, nullable=False)
    par: Mapped[int] = mapped_column(Integer, nullable=False)
    distance: Mapped[int | None] = mapped_column(Integer, nullable=True)

    layout: Mapped["CourseLayout"] = relationship(
        "CourseLayout", back_populates="holes"
    )
