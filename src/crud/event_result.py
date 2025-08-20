"""
CRUD operations for EventResult resources.

This module provides functions to perform Create, Read, Update, and Delete (CRUD)
operations on EventResult resources in the database. These functions interact
with the SQLAlchemy ORM models and are used by the FastAPI routes to manage
EventResult data.

Functions:
- create_event_result: Create a new EventResult in the database.
- get_event_result: Retrieve a single EventResult by its ID.
- get_event_results: Get a list of EventResults with optional pagination.
- get_event_results_by_username: Get all event results for a specific username.
- get_event_results_by_session: Get all event results for a specific event session.
- get_median_round_score: Calculate the median round score for an event session.
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
from sqlalchemy.sql import functions

from src.models.event_result import EventResult as EventResultModel
from src.schemas.event_results import EventResultCreate, EventResultStats


def get_event_result(db: Session, event_result_id: int) -> EventResultModel | None:
    return (
        db.query(EventResultModel)
        .options(joinedload(EventResultModel.course_layout))
        .filter(EventResultModel.id == event_result_id)
        .first()
    )


def get_event_results(
    db: Session, skip: int = 0, limit: int = 100
) -> list[EventResultModel]:
    """
    Get a list of EventResults with optional pagination.

    Args:
        db (Session): The database session.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.

    Returns:
        list[EventResultModel]: A list of EventResult models.
    """
    return (
        db.query(EventResultModel)
        .options(joinedload(EventResultModel.course_layout))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_event_results_by_username(db: Session, username: str):
    db_event_results = (
        db.query(EventResultModel).filter(EventResultModel.username == username).all()
    )
    return db_event_results


def get_event_results_by_session(
    db: Session, event_session_id: int, skip: int = 0, limit: int = 100
) -> list[EventResultModel]:
    """
    Retrieve all event results for a specific event session with pagination.

    Args:
        db: Database session
        event_session_id: Event session ID to filter by
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return

    Returns:
        List of EventResult objects for the session
    """
    return (
        db.query(EventResultModel)
        .filter(EventResultModel.event_session_id == event_session_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_median_round_score(
    db: Session, event_session_id: int | None = None, division: str | None = None
):
    base_query = db.query(EventResultModel.round_total_score).filter(
        EventResultModel.round_total_score.isnot(None)
    )
    if event_session_id is not None:
        base_query = base_query.filter(
            EventResultModel.event_session_id == event_session_id
        )
    if division is not None:
        base_query = base_query.filter(EventResultModel.division == division)

    median = base_query.with_entities(
        functions.percentile_cont(0.5).within_group(
            EventResultModel.round_total_score.asc()
        )
    ).scalar()
    mode = base_query.with_entities(
        functions.mode().within_group(EventResultModel.round_total_score.asc())
    ).scalar()
    min_score = base_query.with_entities(
        functions.min(EventResultModel.round_total_score)
    ).scalar()
    max_score = base_query.with_entities(
        functions.max(EventResultModel.round_total_score)
    ).scalar()
    count = base_query.with_entities(
        functions.count(EventResultModel.round_total_score)
    ).scalar()

    return EventResultStats(
        event_session_id=event_session_id,
        division=division,
        median=float(median) if median is not None else None,
        mode=float(mode) if mode is not None else None,
        minimum=float(min_score) if min_score is not None else None,
        maximum=float(max_score) if max_score is not None else None,
        count=int(count) if count is not None else 0,
    )


def create_event_result(
    db: Session, event_result: EventResultCreate
) -> EventResultModel:
    db_event_result = EventResultModel(**event_result.model_dump())
    db.add(db_event_result)
    db.commit()
    db.refresh(db_event_result)
    return db_event_result


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
