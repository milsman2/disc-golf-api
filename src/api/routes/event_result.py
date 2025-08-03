"""
API routes for managing EventResult resources.

This module provides RESTful endpoints for CRUD operations on EventResult objects.
Event results represent individual player performances in disc golf events.

Routes (grouped by endpoint path, ordered by HTTP method):
- Collection endpoints (/event-results):
  - GET /event-results: Retrieve all event results with pagination
  - POST /event-results: Create a new event result
- Item endpoints (/event-results/id/{id}):
  - GET /event-results/id/{event_result_id}: Retrieve a single event result by ID
  - PUT /event-results/id/{event_result_id}: Update an existing event result
  - DELETE /event-results/id/{event_result_id}: Delete an event result

Dependencies:
- SessionDep: Database session dependency injection
- Pydantic schemas for request/response validation
- CRUD operations with proper error handling
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


@router.post("/", response_model=EventResultPublic, status_code=201)
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


@router.get("/id/{event_result_id}", response_model=EventResultPublic)
def get_event_result_route(event_result_id: int, session: SessionDep):
    """
    Retrieve a single EventResult by its ID.
    Returns 404 if not found.
    """
    db_event_result = get_event_result(db=session, event_result_id=event_result_id)
    if not db_event_result:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return db_event_result


@router.put("/id/{event_result_id}", response_model=EventResultPublic)
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


@router.delete("/id/{event_result_id}", status_code=204)
def delete_event_result_route(event_result_id: int, session: SessionDep):
    """
    Delete an EventResult by its ID.
    Returns 204 No Content if successful, or 404 if not found.
    """
    success = delete_event_result(db=session, event_result_id=event_result_id)
    if not success:
        raise HTTPException(status_code=404, detail="EventResult not found")
