"""
Pydantic schemas for EventResult resources.

Defines data validation and serialization models for EventResult objects,
including creation, database, and public response schemas. These are used
throughout the FastAPI application for request and response handling.
"""

import datetime

from pydantic import BaseModel, ConfigDict


class EventResultBase(BaseModel):
    """
    Shared attributes for EventResult used in creation and response schemas.
    """

    date: datetime.datetime
    division: str
    position: str
    position_raw: int | None = None
    name: str
    event_relative_score: int
    event_total_score: int
    pdga_number: int | None = None
    username: str
    round_relative_score: int
    round_total_score: int
    round_points: float = 0.0

    model_config = ConfigDict(extra="forbid")


class EventResultCreate(EventResultBase):
    """
    Schema for validating data when creating a new EventResult.
    """

    course_layout_id: int


class EventResultInDBBase(EventResultBase):
    """
    Schema representing an EventResult as stored in the database.
    Includes the database-generated ID.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int


class EventResultPublic(EventResultBase):
    """
    Schema for API responses, representing an EventResult with its ID
    and layout reference.
    """

    id: int
    course_layout_id: int


class EventResultsPublic(BaseModel):
    """
    Schema for API responses returning a list of EventResults.
    """

    event_results: list[EventResultPublic] = []
