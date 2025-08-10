"""
Pydantic schemas for disc golf event sessions.

This module defines data validation and serialization schemas for
EventSession objects, including base, creation, update, database,
and public response models. These schemas are used for request validation,
response formatting, and ORM integration in the API.
"""

import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventSessionBase(BaseModel):
    """
    Base schema for EventSession, shared attributes used in
    creation and response schemas.
    """

    name: str = Field(..., description="Name of the event session")
    start_date: datetime.datetime = Field(
        ..., description="Start date of the event session in ISO format"
    )
    end_date: datetime.datetime = Field(
        ..., description="End date of the event session in ISO format"
    )
    description: str | None = Field(
        None, description="Description of the event session"
    )

    model_config = ConfigDict(extra="forbid")


class EventSessionCreate(EventSessionBase):
    """
    Schema for validating data when creating a new EventSession.
    Used for POST requests to create event sessions.
    """

    pass


class EventSessionUpdate(EventSessionBase):
    """
    Schema for validating data when updating an existing EventSession.
    All fields are optional to allow partial updates via PUT/PATCH requests.
    """

    pass


class EventSessionInDBBase(EventSessionBase):
    """
    Schema representing an EventSession as stored in the database.
    Includes the database-generated ID and enables ORM attribute mapping.
    """

    id: int = Field(..., description="Unique identifier for the event session")

    model_config = ConfigDict(from_attributes=True)


class EventSessionPublic(EventSessionInDBBase):
    """
    Schema for API responses, representing an EventSession with its ID.
    Used for GET requests and public-facing API responses.
    """

    pass
