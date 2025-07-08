"""
API routes for managing disc golf event sessions.

This module defines FastAPI endpoints for creating, retrieving, updating, and deleting
EventSession records. It supports operations such as fetching a single event session
by ID, listing all event sessions with pagination, and handling standard HTTP
errors for not found resources. The endpoints use Pydantic schemas for request
validation and response serialization.
"""

from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
from src.crud.event_session import (
    create_event_session,
    delete_event_session,
    get_event_session,
    get_event_sessions,
    update_event_session,
)
from src.schemas import EventSessionCreate, EventSessionPublic, EventSessionUpdate

router = APIRouter(prefix="/event_sessions", tags=["event_sessions"])


@router.get("/{event_session_id}", response_model=EventSessionPublic)
def get_event_session_route(
    event_session_id: int,
    db: SessionDep,
):
    """
    Get a event session by ID.
    """
    event_session = get_event_session(db, event_session_id)
    if not event_session:
        raise HTTPException(status_code=404, detail="Event session not found")
    return event_session


@router.get("/", response_model=list[EventSessionPublic])
def get_event_sessions_route(db: SessionDep, skip: int = 0, limit: int = 100):
    """
    Get a list of event sessions with pagination.
    """
    return get_event_sessions(db, skip=skip, limit=limit)


@router.post("/", response_model=EventSessionPublic, status_code=201)
def create_event_session_route(
    event_session: EventSessionCreate,
    db: SessionDep,
):
    """
    Create a new event session.
    """
    return create_event_session(db, event_session)


@router.delete("/{event_session_id}", response_model=EventSessionPublic)
def delete_event_session_route(
    event_session_id: int,
    db: SessionDep,
):
    """
    Delete a event session by ID.
    """
    event_session = delete_event_session(db, event_session_id)
    if not event_session:
        raise HTTPException(status_code=404, detail="Event session not found")
    return event_session


@router.put("/{event_session_id}", response_model=EventSessionPublic)
def update_event_session_route(
    event_session_id: int,
    event_session_data: EventSessionUpdate,
    db: SessionDep,
):
    """
    Update an event session by ID.
    """
    event_session = update_event_session(db, event_session_id, event_session_data)
    if not event_session:
        raise HTTPException(status_code=404, detail="Event session not found")
    return event_session
