"""
Course model for disc golf courses
"""

from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.models.course_layout import CourseLayout
from src.models.base import Base


class Course(Base):
    """
    SQL model for disc golf courses
    """

    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    location: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str | None] = mapped_column(String, nullable=True)
    state: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    holes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    reviews_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    layouts: Mapped[list["CourseLayout"]] = relationship(
        "Layout", back_populates="course"
    )
