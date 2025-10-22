"""CRUD operations for DiscEvent (disc golf events).

Provides helpers to create, read, update and delete DiscEvent records.
Notable behavior:
- `create_disc_event` persists a new DiscEvent.
- `update_disc_event` intentionally ignores `None` values in the provided
    `DiscEventUpdate` schema to support partial-update semantics (fields not
    provided will not overwrite existing values).
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
        # Only set attributes that are explicitly provided (not None)
        for key, value in disc_event_data.model_dump().items():
            if value is None:
                continue
            setattr(db_disc_event, key, value)
        db.commit()
        db.refresh(db_disc_event)
    return db_disc_event
