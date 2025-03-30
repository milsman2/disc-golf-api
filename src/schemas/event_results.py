"""
Schemas for EventResult.

This module defines the Pydantic schemas for the EventResult model, which represent
the results of a disc golf event. These schemas are used for data validation and
serialization in the FastAPI application.

Schemas:
- EventResultBase: Shared attributes for EventResult.
- EventResultCreate: Schema for creating a new EventResult.
- EventResult: Schema for returning an EventResult, including relationships to
  Course and CourseLayout.
"""

from pydantic import BaseModel, ConfigDict
from src.schemas.courses import CoursePublic
from src.schemas.course_layouts import CourseLayoutPublic


class EventResultBase(BaseModel):
    """
    Base schema for EventResult, used for shared attributes.
    """

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
    course_id: int
    layout_id: int


class EventResultCreate(EventResultBase):
    """
    Schema for creating a new EventResult.
    """

    pass


class EventResult(EventResultBase):
    """
    Schema for returning an EventResult, including relationships.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    course: CoursePublic
    layout: CourseLayoutPublic
