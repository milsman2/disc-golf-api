"""
CRUD operations for disc golf event sessions.

This module provides functions to create, retrieve, update, and
delete EventSession records in the database using SQLAlchemy ORM.
It supports operations for single event sessions as well as listing
multiple sessions with pagination.
"""

from sqlalchemy.orm import Session

from src.models import DiscEvent
from src.schemas import DiscEventCreate, DiscEventUpdate


def create_disc_event(db: Session, disc_event: DiscEventCreate) -> DiscEvent:
    db_disc_event = DiscEvent(**disc_event.model_dump())
    db.add(db_disc_event)
    db.commit()
    db.refresh(db_disc_event)
    return db_disc_event


def get_disc_event(db: Session, disc_event_id: int) -> DiscEvent | None:
    return db.query(DiscEvent).filter(DiscEvent.id == disc_event_id).first()


def get_disc_event_by_name(db: Session, name: str) -> DiscEvent | None:
    return db.query(DiscEvent).filter(DiscEvent.name == name).first()


def get_disc_events(db: Session, skip: int = 0, limit: int = 100) -> list[DiscEvent]:
    return db.query(DiscEvent).offset(skip).limit(limit).all()


def delete_disc_event(db: Session, disc_event_id: int) -> DiscEvent | None:
    db_disc_event = db.query(DiscEvent).filter(DiscEvent.id == disc_event_id).first()
    if db_disc_event:
        db.delete(db_disc_event)
        db.commit()
    return db_disc_event


def update_disc_event(
    db: Session, disc_event_id: int, disc_event_data: DiscEventUpdate
) -> DiscEvent | None:
    db_disc_event = db.query(DiscEvent).filter(DiscEvent.id == disc_event_id).first()
    if db_disc_event:
        for key, value in disc_event_data.model_dump().items():
            setattr(db_disc_event, key, value)
        db.commit()
        db.refresh(db_disc_event)
    return db_disc_event
