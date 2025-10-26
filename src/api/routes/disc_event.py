"""
API routes for managing DiscEvent resources.

This module provides RESTful endpoints for CRUD operations on DiscEvent objects.
Disc events represent specific disc golf events or tournaments.

Routes (grouped by endpoint path, ordered by HTTP method):
- Collection endpoints (/disc-events):
    - GET /disc-events: Retrieve all disc events with pagination
    - POST /disc-events: Create a new disc event
- Item endpoints (/disc-events/id/{id}):
    - GET /disc-events/id/{disc_event_id}: Retrieve a single disc event by ID
    - PUT /disc-events/id/{disc_event_id}: Update an existing disc event
    - DELETE /disc-events/id/{disc_event_id}: Delete a disc event

Dependencies:
- SessionDep: Database session dependency injection
- Pydantic schemas for request/response validation
- CRUD operations with proper error handling
"""

from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
from src.crud import (
    create_disc_event,
    delete_disc_event,
    get_disc_event,
    get_disc_event_by_name,
    get_disc_events,
    update_disc_event,
)
from src.schemas import DiscEventCreate, DiscEventPublic, DiscEventUpdate

router = APIRouter(prefix="/disc-events", tags=["Disc Events"])


@router.get("/", response_model=list[DiscEventPublic])
def get_disc_events_route(db: SessionDep, skip: int = 0, limit: int = 100):
    """
    Get a list of disc events with pagination.
    """
    return get_disc_events(db, skip=skip, limit=limit)


@router.post("/", response_model=DiscEventPublic, status_code=201)
def create_disc_event_route(
    disc_event: DiscEventCreate,
    db: SessionDep,
):
    """
    Create a new disc event.
    """
    existing_event = get_disc_event_by_name(db, disc_event.name)
    if existing_event:
        raise HTTPException(
            status_code=409,
            detail=f"Disc event with name '{disc_event.name}' already exists",
        )

    return create_disc_event(db, disc_event)


@router.get("/id/{disc_event_id}", response_model=DiscEventPublic)
def get_disc_event_route(
    disc_event_id: int,
    db: SessionDep,
):
    """
    Get a disc event by ID.
    """
    disc_event = get_disc_event(db, disc_event_id)
    if not disc_event:
        raise HTTPException(status_code=404, detail="Disc event not found")
    return disc_event


@router.put("/id/{disc_event_id}", response_model=DiscEventPublic)
def update_disc_event_route(
    disc_event_id: int,
    disc_event_data: DiscEventUpdate,
    db: SessionDep,
):
    """
    Update a disc event by ID.

    Partial-update semantics:
    - The request body should be a `DiscEventUpdate` where all fields are optional.
    - Only provided fields (non-null) will be updated; fields omitted or set to `null`
        in the payload will be ignored and not overwrite existing values.
    - If you want to explicitly clear a value (set it to NULL in the DB), the
        current implementation treats `null` as "not provided"; explicit-clearing
        behavior can be added later if desired.
    """
    disc_event = update_disc_event(db, disc_event_id, disc_event_data)
    if not disc_event:
        raise HTTPException(status_code=404, detail="Disc event not found")
    return disc_event


@router.delete("/id/{disc_event_id}", status_code=204)
def delete_disc_event_route(
    disc_event_id: int,
    db: SessionDep,
):
    """
    Delete a disc event by ID.
    """
    disc_event = delete_disc_event(db, disc_event_id)
    if not disc_event:
        raise HTTPException(status_code=404, detail="Disc event not found")
