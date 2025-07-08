"""
This module defines the SQLAlchemy model for a disc golf event session.

A EventSession represents a session or season of a disc golf event, including
its name, start and end dates, and an optional description. Each EventSession
can have multiple associated EventResult records, establishing a one-to-many
relationship between EventSession and EventResult.
"""

import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class EventSession(Base):
    """
    SQLAlchemy model for a event session.

    Represents a session or season of a disc golf event, including its
    name, start and end dates, and an optional description. Each EventSession
    can have multiple associated EventResult records.
    """

    __tablename__ = "event_sessions"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, comment="Name of the event session"
    )
    start_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, comment="Start date of the event session"
    )
    end_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, comment="End date of the event session"
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Description of the event session",
    )

    event_results = relationship(
        "EventResult",
        back_populates="event_session",
        cascade="all, delete-orphan",
        doc="List of EventResult objects associated with this event session.",
    )
