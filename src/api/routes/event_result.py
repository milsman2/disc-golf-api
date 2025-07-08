"""
API routes for managing EventResult resources.

This module defines the FastAPI endpoints for CRUD operations on EventResult objects,
including creation, retrieval (single and multiple), update, and deletion.

Routes:
- POST /event-results/: Create a new EventResult.
- GET /event-results/: Retrieve a list of EventResults with optional pagination.
- GET /event-results/{event_result_id}: Retrieve a single EventResult by its ID.
- PUT /event-results/{event_result_id}: Update an existing EventResult by its ID.
- DELETE /event-results/{event_result_id}: Delete an EventResult by its ID.

Dependencies:
- SessionDep: Provides a database session for route handlers.

Modules Used:
- src.schemas.event_results: Pydantic schemas for EventResult.
- src.crud: CRUD operations for EventResult.
- src.api.deps: Shared dependencies for API routes.
"""

from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
from src.crud import (
    create_event_result,
    delete_event_result,
    get_event_result,
    get_event_results,
    get_event_session,
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
    Retrieve a list of EventResults with optional pagination.
    Returns 404 if no results are found.
    """
    raw_results = get_event_results(db=session, skip=skip, limit=limit)
    if not raw_results:
        raise HTTPException(status_code=404, detail="No EventResults found")
    return {"event_results": raw_results}


@router.get("/{event_result_id}", response_model=EventResultPublic)
def get_event_result_route(event_result_id: int, session: SessionDep):
    """
    Retrieve a single EventResult by its ID.
    Returns 404 if not found.
    """
    db_event_result = get_event_result(db=session, event_result_id=event_result_id)
    if not db_event_result:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return db_event_result


@router.post("/", response_model=EventResultPublic)
def create_event_result_route(event_result: EventResultCreate, session: SessionDep):
    """
    Create a new EventResult.
    Returns the created EventResult.
    """
    event_session = get_event_session(session, event_result.event_session_id)
    if not event_session:
        raise HTTPException(
            status_code=422,
            detail=(
                f"event_session_id {event_result.event_session_id} does not exist."
            ),
        )
    return create_event_result(db=session, event_result=event_result)


@router.put("/{event_result_id}", response_model=EventResultPublic)
def update_event_result_route(
    event_result_id: int,
    updated_event_result: EventResultCreate,
    session: SessionDep,
):
    """
    Update an existing EventResult by its ID.
    Returns the updated EventResult, or 404 if not found.
    """
    db_event_result = update_event_result(
        db=session,
        event_result_id=event_result_id,
        updated_event_result=updated_event_result,
    )
    if not db_event_result:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return db_event_result


@router.delete("/{event_result_id}", status_code=204)
def delete_event_result_route(event_result_id: int, session: SessionDep):
    """
    Delete an EventResult by its ID.
    Returns 204 No Content if successful, or 404 if not found.
    """
    success = delete_event_result(db=session, event_result_id=event_result_id)
    if not success:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return None
