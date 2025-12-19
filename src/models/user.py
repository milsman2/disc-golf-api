"""
SQL Model for TPL users
"""

from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class User(Base):
    """
    TPL user model as SQL data types
    """

    __tablename__ = "users"

    id: Mapped[int | None] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    hashed_password: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    full_name: Mapped[str | None] = mapped_column(nullable=True)
