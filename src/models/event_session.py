"""
This module defines the SQLAlchemy model for a disc golf league session.

A LeagueSession represents a session or season of a disc golf league, including
its name, start and end dates, and an optional description. Each LeagueSession
can have multiple associated EventResult records, establishing a one-to-many
relationship between LeagueSession and EventResult.
"""

import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class EventSession(Base):
    """
    SQLAlchemy model for a league session.

    Represents a session or season of a disc golf league, including its
    name, start and end dates, and an optional description. Each LeagueSession
    can have multiple associated EventResult records.
    """

    __tablename__ = "league_sessions"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, comment="Name of the league session"
    )
    start_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, comment="Start date of the league session"
    )
    end_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, comment="End date of the league session"
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Description of the league session",
    )

    event_results = relationship(
        "EventResult",
        back_populates="event_session",
        cascade="all, delete-orphan",
        doc="List of EventResult objects associated with this league session.",
    )
