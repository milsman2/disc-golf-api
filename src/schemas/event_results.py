"""Pydantic schemas for disc golf event results."""

import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventResultBase(BaseModel):
    """Base schema for EventResult containing shared attributes."""

    date: datetime.datetime = Field(..., description="Date when the event occurred")
    division: str = Field(..., description="Division category (e.g., MPO, FPO, MA1)")
    position: str = Field(..., description="Final position in the event")
    position_raw: int | None = Field(
        None, description="Raw numeric position, None if DNF or other special case"
    )
    name: str = Field(..., description="Player's full name")
    event_relative_score: int = Field(
        ..., description="Score relative to par for the entire event"
    )
    event_total_score: int = Field(..., description="Total strokes for the event")
    pdga_number: int | None = Field(None, description="Player's PDGA membership number")
    username: str = Field(..., description="Player's username or identifier")
    round_relative_score: int = Field(
        ..., description="Score relative to par for this round"
    )
    round_total_score: int = Field(..., description="Total strokes for this round")
    round_points: float = Field(
        default=0.0, description="Points awarded for this round"
    )

    model_config = ConfigDict(extra="forbid")


class EventResultCreate(EventResultBase):
    """Schema for creating a new EventResult."""

    course_layout_id: int = Field(
        ..., description="ID of the course layout where the event took place"
    )
    disc_event_id: int = Field(
        ..., description="ID of the disc event this result belongs to"
    )


class EventResultInDBBase(EventResultBase):
    """Schema for EventResult as stored in the database."""

    id: int = Field(..., description="Unique identifier for the event result")

    model_config = ConfigDict(from_attributes=True)


class EventResultPublic(EventResultBase):
    """Schema for public API responses with EventResult data."""

    id: int = Field(..., description="Unique identifier for the event result")
    course_layout_id: int = Field(
        ..., description="ID of the course layout where the event took place"
    )
    disc_event_id: int = Field(
        ..., description="ID of the disc event this result belongs to"
    )


class EventResultsPublic(BaseModel):
    """Schema for collections of EventResults."""

    event_results: list[EventResultPublic] = Field(
        default=[], description="List of event results"
    )


class DivisionResults(BaseModel):
    """Event results grouped for a single division, sorted by position_raw."""

    division: str
    # Use the DB-aware schema so ORM objects are serialized correctly
    results: list[EventResultInDBBase] = Field(
        default=[], description="Results for the division"
    )


class DivisionStats(BaseModel):
    """Statistics for a single division within an event."""

    division: str = Field(..., description="Division name (e.g., MPO, FPO, MA1)")
    count: int = Field(..., description="Number of players in this division")
    average_round_score: float | None = Field(
        None, description="Average round score for this division"
    )
    median_round_score: float | None = Field(
        None, description="Median round score for this division"
    )
    average_event_score: float | None = Field(
        None, description="Average total event score for this division"
    )
    median_event_score: float | None = Field(
        None, description="Median total event score for this division"
    )
    best_round_score: int | None = Field(
        None, description="Best (lowest) round score in this division"
    )
    worst_round_score: int | None = Field(
        None, description="Worst (highest) round score in this division"
    )
    best_event_score: int | None = Field(
        None, description="Best (lowest) total event score in this division"
    )
    worst_event_score: int | None = Field(
        None, description="Worst (highest) total event score in this division"
    )


class DivisionResultsWithStats(BaseModel):
    """Event results grouped for a single division with statistics."""

    division: str
    stats: DivisionStats
    results: list[EventResultInDBBase] = Field(
        default=[], description="Results for the division"
    )


class EventResultsGroupedPublic(BaseModel):
    """Top-level schema for grouped event results by division."""

    grouped: list[DivisionResults] = Field(
        default=[], description="Event results grouped by division"
    )


class EventResultsGroupedWithStatsPublic(BaseModel):
    """Top-level schema for grouped event results by division with statistics."""

    disc_event_id: int | None = Field(None, description="Disc event ID if filtered")
    grouped: list[DivisionResultsWithStats] = Field(
        default=[], description="Event results grouped by division with statistics"
    )


class DiscEventSummary(BaseModel):
    """Summary of a disc event with division statistics for frontend tables."""

    disc_event_id: int = Field(..., description="Disc event ID")
    event_name: str | None = Field(None, description="Event name")
    event_date: datetime.datetime | None = Field(None, description="Event date")
    total_players: int = Field(..., description="Total number of players")
    division_stats: list[DivisionStats] = Field(
        default=[], description="Statistics broken down by division"
    )


class MultiEventSummaryPublic(BaseModel):
    """Summary of multiple disc events for frontend dashboard/tables."""

    events: list[DiscEventSummary] = Field(
        default=[], description="List of disc event summaries"
    )


class EventResultStats(BaseModel):
    disc_event_id: int | None = Field(
        None, description="ID of the disc event if filtered"
    )
    division: str | None = Field(None, description="Division filter applied, if any")
    median: float | None
    mode: float | None
    minimum: float | None
    maximum: float | None
    count: int
