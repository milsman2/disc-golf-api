"""
CRUD operations for EventResult resources.

This module provides functions to perform Create, Read, Update, and Delete (CRUD)
operations on EventResult resources in the database. These functions interact
with the SQLAlchemy ORM models and are used by the FastAPI routes to manage
EventResult data.

Functions:
- create_event_result: Create a new EventResult in the database.
- get_event_result: Retrieve a single EventResult by its ID.
- update_event_result: Update an existing EventResult by its ID.
- delete_event_result: Delete an EventResult by its ID.

Dependencies:
- SQLAlchemy Session: Used to interact with the database.
- EventResultModel: The SQLAlchemy model for EventResult.
- EventResultCreate: The Pydantic schema for creating or updating EventResults.

Modules Used:
- sqlalchemy.orm: Provides the Session class for database interactions.
- src.models.event_result: Defines the EventResult SQLAlchemy model.
- src.schemas.event_results: Defines the Pydantic schemas for EventResult.
"""

from sqlalchemy.orm import Session, joinedload

from src.models.event_result import EventResult as EventResultModel
from src.schemas.event_results import EventResultCreate


def create_event_result(
    db: Session, event_result: EventResultCreate
) -> EventResultModel:
    db_event_result = EventResultModel(**event_result.model_dump())
    db.add(db_event_result)
    db.commit()
    db.refresh(db_event_result)
    return db_event_result


def get_event_result(db: Session, event_result_id: int) -> EventResultModel | None:
    return (
        db.query(EventResultModel)
        .options(joinedload(EventResultModel.course_layout))
        .filter(EventResultModel.id == event_result_id)
        .first()
    )


def update_event_result(
    db: Session, event_result_id: int, updated_event_result: EventResultCreate
) -> EventResultModel | None:
    """
    Update an existing EventResult by its ID.

    Args:
        db (Session): The database session.
        event_result_id (int): The ID of the EventResult to update.
        updated_event_result (EventResultCreate): The updated data for the EventResult.

    Returns:
        EventResultModel | None: The updated EventResult if found, otherwise None.
    """
    db_event_result = (
        db.query(EventResultModel)
        .filter(EventResultModel.id == event_result_id)
        .first()
    )
    if not db_event_result:
        return None

    for key, value in updated_event_result.model_dump().items():
        setattr(db_event_result, key, value)

    db.commit()
    db.refresh(db_event_result)
    return db_event_result


def delete_event_result(db: Session, event_result_id: int) -> bool:
    """
    Delete an EventResult by its ID.

    Args:
        db (Session): The database session.
        event_result_id (int): The ID of the EventResult to delete.

    Returns:
        bool: True if the EventResult was deleted, False if not found.
    """
    db_event_result = (
        db.query(EventResultModel)
        .filter(EventResultModel.id == event_result_id)
        .first()
    )
    if not db_event_result:
        return False

    db.delete(db_event_result)
    db.commit()
    return True
