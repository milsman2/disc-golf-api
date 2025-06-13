"""
Pydantic schemas for disc golf league sessions.

This module defines data validation and serialization schemas for
LeagueSession objects, including base, creation, update, database,
and public response models. These schemas are used for request validation,
response formatting, and ORM integration in the API.
"""

import datetime

from pydantic import BaseModel, ConfigDict, Field


class LeagueSessionBase(BaseModel):
    """
    Base schema for LeagueSession, shared attributes used in
    creation and response schemas.
    """

    name: str | None = Field(..., description="Name of the league session")
    start_date: datetime.datetime | None = Field(
        None, description="Start date of the league session in ISO format"
    )
    end_date: datetime.datetime | None = Field(
        None, description="End date of the league session in ISO format"
    )
    description: str | None = Field(
        None, description="Description of the league session"
    )

    model_config = ConfigDict(extra="forbid")


class LeagueSessionCreate(LeagueSessionBase):
    """
    Schema for validating data when creating a new LeagueSession.
    """

    pass


class LeagueSessionUpdate(LeagueSessionBase):
    """
    Schema for validating data when updating an existing LeagueSession.
    All fields are optional to allow partial updates.
    """

    pass


class LeagueSessionInDBBase(LeagueSessionBase):
    """
    Schema representing a LeagueSession as stored in the database.
    Includes the database-generated ID.
    """

    id: int = Field(..., description="Unique identifier for the league session")

    model_config = ConfigDict(from_attributes=True)


class LeagueSessionPublic(LeagueSessionInDBBase):
    """
    Schema for API responses, representing a LeagueSession with its ID.
    """

    pass
