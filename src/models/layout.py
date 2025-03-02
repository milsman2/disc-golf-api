"""
Layout model
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Layout(Base):
    """
    SQL model for disc golf course layouts

    """

    __tablename__ = "layout"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("courses.id"), nullable=False
    )
    total_holes: Mapped[int] = mapped_column(Integer, nullable=False)
