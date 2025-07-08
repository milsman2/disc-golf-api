"""
CRUD operations for disc golf event sessions.

This module provides functions to create, retrieve, update, and
delete EventSession records in the database using SQLAlchemy ORM.
It supports operations for single event sessions as well as listing
multiple sessions with pagination.
"""

from sqlalchemy.orm import Session

from src.models import EventSession
from src.schemas import EventSessionCreate, EventSessionUpdate


def create_event_session(
    db: Session, event_session: EventSessionCreate
) -> EventSession:
    db_event_session = EventSession(**event_session.model_dump())
    db.add(db_event_session)
    db.commit()
    db.refresh(db_event_session)
    return db_event_session


def get_event_session(db: Session, event_session_id: int) -> EventSession | None:
    return db.query(EventSession).filter(EventSession.id == event_session_id).first()


def get_event_sessions(
    db: Session, skip: int = 0, limit: int = 100
) -> list[EventSession]:
    return db.query(EventSession).offset(skip).limit(limit).all()


def delete_event_session(db: Session, event_session_id: int) -> EventSession | None:
    db_event_session = (
        db.query(EventSession).filter(EventSession.id == event_session_id).first()
    )
    if db_event_session:
        db.delete(db_event_session)
        db.commit()
    return db_event_session


def update_event_session(
    db: Session, event_session_id: int, event_session_data: EventSessionUpdate
) -> EventSession | None:
    db_event_session = (
        db.query(EventSession).filter(EventSession.id == event_session_id).first()
    )
    if db_event_session:
        for key, value in event_session_data.model_dump().items():
            setattr(db_event_session, key, value)
        db.commit()
        db.refresh(db_event_session)
    return db_event_session
