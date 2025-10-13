"""
Pydantic schemas for disc golf event results.

This module defines data validation and serialization schemas for
EventResult objects, including base, creation, update, database,
and public response models. These schemas are used for request validation,
response formatting, and ORM integration in the disc golf API.
"""

import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventResultBase(BaseModel):
    """
    Base schema for EventResult containing shared attributes used across
    creation and response schemas for disc golf event results.
    """

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
    """
    Schema for validating data when creating a new EventResult.
    Used for POST requests to create event results with required foreign key references.
    """

    course_layout_id: int = Field(
        ..., description="ID of the course layout where the event took place"
    )
    disc_event_id: int = Field(
        ..., description="ID of the disc event this result belongs to"
    )


class EventResultInDBBase(EventResultBase):
    """
    Schema representing an EventResult as stored in the database.
    Includes the database-generated ID and enables ORM attribute mapping.
    """

    id: int = Field(..., description="Unique identifier for the event result")

    model_config = ConfigDict(from_attributes=True)


class EventResultPublic(EventResultBase):
    """
    Schema for API responses, representing an EventResult with its ID
    and foreign key references. Used for GET requests and public-facing API responses.
    """

    id: int = Field(..., description="Unique identifier for the event result")
    course_layout_id: int = Field(
        ..., description="ID of the course layout where the event took place"
    )
    disc_event_id: int = Field(
        ..., description="ID of the disc event this result belongs to"
    )


class EventResultsPublic(BaseModel):
    """
    Schema for API responses returning a collection of EventResults.
    Used for GET requests that return multiple event results.
    """

    event_results: list[EventResultPublic] = Field(
        default=[], description="List of event results"
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
