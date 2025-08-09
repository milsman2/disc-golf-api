"""
API routes for managing EventSession resources.

This module provides RESTful endpoints for CRUD operations on EventSession objects.
Event sessions represent specific instances or rounds of disc golf events.

Routes (grouped by endpoint path, ordered by HTTP method):
- Collection endpoints (/event-sessions):
  - GET /event-sessions: Retrieve all event sessions with pagination
  - POST /event-sessions: Create a new event session
- Item endpoints (/event-sessions/{id}):
  - GET /event-sessions/{event_session_id}: Retrieve a single event session by ID
- Item endpoints (/event-sessions/id/{id}):
  - PUT /event-sessions/id/{event_session_id}: Update an existing event session
  - DELETE /event-sessions/id/{event_session_id}: Delete an event session

Dependencies:
- SessionDep: Database session dependency injection
- Pydantic schemas for request/response validation
- CRUD operations with proper error handling
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

router = APIRouter(prefix="/event-sessions", tags=["Event Sessions"])


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


@router.put("/id/{event_session_id}", response_model=EventSessionPublic)
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


@router.delete("/id/{event_session_id}", status_code=204)
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
