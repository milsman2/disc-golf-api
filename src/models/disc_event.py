"""
SQLAlchemy model definition for disc golf events.

This module defines the DiscEvent ORM class, representing
disc golf events in the database.
"""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.event_result import EventResult


class DiscEvent(Base):
    """
    SQLAlchemy model for disc golf events.

    Attributes:
        id (int): The primary key for the event.
        name (str): The name of the event.
        start_date (datetime): The start date and time of the event.
        end_date (datetime): The end date and time of the event.
        description (str | None): A brief description of the event.
        event_results (list[EventResult]): List of EventResult objects
        associated with this disc event.
    """

    __tablename__ = "disc_events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        nullable=False,
        doc="The primary key for the event.",
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False, doc="The name of the event."
    )
    start_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, doc="The start date and time of the event."
    )
    end_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, doc="The end date and time of the event."
    )
    description: Mapped[str | None] = mapped_column(
        String, nullable=True, doc="A brief description of the event."
    )

    event_results: Mapped[list["EventResult"]] = relationship(
        "EventResult",
        back_populates="disc_event",
        cascade="all, delete-orphan",
        doc="List of EventResult objects associated with this disc event.",
    )
