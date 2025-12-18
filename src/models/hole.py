"""
Hole model for disc golf course holes
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.course_layout import CourseLayout


class Hole(Base):
    """
    SQL model for disc golf course holes
    """

    __tablename__ = "holes"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, nullable=False, autoincrement=True
    )
    hole_name: Mapped[str] = mapped_column(String, nullable=False)
    par: Mapped[int | None] = mapped_column(Integer, nullable=False)
    distance: Mapped[int | None] = mapped_column(Integer, nullable=True)

    layout_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("course_layouts.id"), nullable=False
    )

    layout: Mapped["CourseLayout"] = relationship(
        "CourseLayout", back_populates="holes"
    )
