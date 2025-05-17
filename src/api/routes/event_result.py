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

from src.api.deps import SessionDep
from src.crud import (
    create_event_result,
    delete_event_result,
    get_event_result,
    get_event_results,
    update_event_result,
)
from src.schemas.event_results import (
    EventResultCreate,
    EventResultPublic,
    EventResultsPublic,
)

router = APIRouter(
    prefix="/event-results",
    tags=["Event Results"],
)


@router.get("/", response_model=EventResultsPublic)
def get_event_results_route(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
):
    """
    Get a list of EventResults with optional pagination.
    """
    raw_results = get_event_results(db=session, skip=skip, limit=limit)
    if not raw_results:
        raise HTTPException(status_code=404, detail="No EventResults found")
    return {"event_results": raw_results}


@router.get("/{event_result_id}", response_model=EventResultPublic)
def get_event_result_route(event_result_id: int, session: SessionDep):
    """
    Get an EventResult by ID.
    """
    db_event_result = get_event_result(db=session, event_result_id=event_result_id)
    if not db_event_result:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return db_event_result


@router.post("/", response_model=EventResultPublic)
def create_event_result_route(event_result: EventResultCreate, session: SessionDep):
    """
    Create a new EventResult.
    """
    return create_event_result(db=session, event_result=event_result)


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
        db=session,
        event_result_id=event_result_id,
        updated_event_result=updated_event_result,
    )
    if not db_event_result:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return db_event_result


@router.delete("/{event_result_id}")
def delete_event_result_route(event_result_id: int, session: SessionDep):
    """
    Delete an EventResult by ID.
    """
    success = delete_event_result(db=session, event_result_id=event_result_id)
    if not success:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return {"detail": "EventResult deleted successfully"}
