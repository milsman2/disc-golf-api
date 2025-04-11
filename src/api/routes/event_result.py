"""
Routes for managing EventResult resources.

This module defines the FastAPI routes for performing CRUD operations on
EventResult resources. These routes allow clients to create, retrieve, update,
and delete EventResults in the system.

Routes:
- POST /event-results/:
    Create a new EventResult.
- GET /event-results/:
    Retrieve a list of EventResults with optional pagination.
- GET /event-results/{event_result_id}:
    Retrieve a single EventResult by its ID.
- PUT /event-results/{event_result_id}:
    Update an existing EventResult by its ID.
- DELETE /event-results/{event_result_id}:
    Delete an EventResult by its ID.

Dependencies:
- SessionDep: A dependency that provides a database session for interacting
  with the database.

Modules Used:
- src.schemas.event_results: Defines the Pydantic schemas for EventResult.
- src.crud: Contains the CRUD operations for EventResult.
- src.api.deps: Provides shared dependencies for API routes.
"""

from fastapi import APIRouter, HTTPException
from typing import List

from src.schemas.event_results import EventResultPublic, EventResultCreate
from src.crud import (
    create_event_result,
    get_event_result,
    get_event_results,
    update_event_result,
    delete_event_result,
)
from src.api.deps import SessionDep

router = APIRouter(
    prefix="/event-results",
    tags=["Event Results"],
)


@router.post("/", response_model=EventResultPublic)
def create_event_result_route(event_result: EventResultCreate, session: SessionDep):
    """
    Create a new EventResult.
    """
    return create_event_result(session, event_result)


@router.get("/", response_model=List[EventResultPublic])
def get_event_results_route(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve a list of EventResults.
    """
    return get_event_results(session, skip, limit)


@router.get("/{event_result_id}", response_model=EventResultPublic)
def get_event_result_route(event_result_id: int, session: SessionDep):
    """
    Retrieve a single EventResult by ID.
    """
    db_event_result = get_event_result(session, event_result_id)
    if not db_event_result:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return db_event_result


@router.put("/{event_result_id}", response_model=EventResultPublic)
def update_event_result_route(
    event_result_id: int,
    updated_event_result: EventResultCreate,
    session: SessionDep,
):
    """
    Update an existing EventResult by ID.
    """
    db_event_result = update_event_result(
        session, event_result_id, updated_event_result
    )
    if not db_event_result:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return db_event_result


@router.delete("/{event_result_id}")
def delete_event_result_route(event_result_id: int, session: SessionDep):
    """
    Delete an EventResult by ID.
    """
    success = delete_event_result(session, event_result_id)
    if not success:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return {"detail": "EventResult deleted successfully"}
