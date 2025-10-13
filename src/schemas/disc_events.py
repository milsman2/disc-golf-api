"""
Pydantic schemas for disc golf events.

This module defines data validation and serialization schemas for
DiscEvent objects, including base, creation, update, database,
and public response models. These schemas are used for request validation,
response formatting, and ORM integration in the API.
"""

import datetime

from pydantic import BaseModel, ConfigDict, Field


class DiscEventBase(BaseModel):
    """
    Base schema for DiscEvent, shared attributes used in
    creation and response schemas.
    """

    name: str = Field(..., description="Name of the disc event")
    start_date: datetime.datetime = Field(
        ..., description="Start date of the disc event in ISO format"
    )
    end_date: datetime.datetime = Field(
        ..., description="End date of the disc event in ISO format"
    )
    description: str | None = Field(None, description="Description of the disc event")

    model_config = ConfigDict(extra="forbid")


class DiscEventCreate(DiscEventBase):
    """
    Schema for validating data when creating a new DiscEvent.
    Used for POST requests to create disc events.
    """

    pass


class DiscEventUpdate(DiscEventBase):
    """
    Schema for validating data when updating an existing DiscEvent.
    All fields are optional to allow partial updates via PUT/PATCH requests.
    """

    pass


class DiscEventInDBBase(DiscEventBase):
    """
    Schema representing a DiscEvent as stored in the database.
    Includes the database-generated ID and enables ORM attribute mapping.
    """

    id: int = Field(..., description="Unique identifier for the disc event")

    model_config = ConfigDict(from_attributes=True)


class DiscEventPublic(DiscEventInDBBase):
    """
    Schema for API responses, representing a DiscEvent with its ID.
    Used for GET requests and public-facing API responses.
    """

    pass
