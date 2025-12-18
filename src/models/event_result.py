"""
EventResult model for disc golf events.

This module defines the SQLAlchemy model for storing event results in a disc golf
application. Each event result is tied to a specific course and course layout, and
contains information about a player's performance in the event.
"""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.course_layout import CourseLayout
    from src.models.disc_event import DiscEvent


class EventResult(Base):
    """
    SQLAlchemy model for disc golf event results.

    Attributes:
        id (int): The primary key for the event result.
        division (str): The division in which the player competed (e.g., GOLD, BLUE).
        position (str): The player's position in the event (e.g., 1, T2).
        position_raw (int): The raw position value for sorting purposes.
        name (str): The name of the player.
        event_relative_score (int): The player's score relative to par for the event.
        event_total_score (int): The player's total score for the event.
        pdga_number (float | None): The player's PDGA number, if available.
        username (str): The player's username in the system.
        round_relative_score (int): The player's score relative to par for the round.
        round_total_score (int): The player's total score for the round.
        course_layout_id (int): The foreign key referencing the CourseLayout model.
        course_layout (CourseLayout): The CourseLayout associated with the event
        round_points (float): The points earned by the player for the round.
    """

    __tablename__ = "event_results"
    __table_args__ = (
        UniqueConstraint("date", "username", name="uq_eventresult_date_username"),
    )
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    division: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[str] = mapped_column(String, nullable=False)
    position_raw: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    event_relative_score: Mapped[int] = mapped_column(Integer, nullable=False)
    event_total_score: Mapped[int] = mapped_column(Integer, nullable=False)
    pdga_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    round_relative_score: Mapped[int] = mapped_column(Integer, nullable=False)
    round_total_score: Mapped[int] = mapped_column(Integer, nullable=False)
    round_points: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    course_layout_id: Mapped[int] = mapped_column(
        ForeignKey("course_layouts.id"), nullable=False
    )
    disc_event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("disc_events.id"), nullable=False
    )

    disc_event: Mapped["DiscEvent"] = relationship(
        "DiscEvent", back_populates="event_results"
    )
    course_layout: Mapped["CourseLayout"] = relationship(
        "CourseLayout", back_populates="event_results"
    )
