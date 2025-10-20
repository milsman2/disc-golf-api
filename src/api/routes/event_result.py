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

from typing import Union

from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
from src.crud import (
    create_event_result,
    delete_event_result,
    get_disc_event,
    get_event_result,
    get_event_results,
    get_event_results_by_disc_event,
    get_median_round_score,
    update_event_result,
)
from src.crud.event_result import get_event_results_by_username
from src.schemas.event_results import (
    EventResultCreate,
    EventResultPublic,
    EventResultsGroupedPublic,
    EventResultsPublic,
    EventResultStats,
)

router = APIRouter(
    prefix="/event-results",
    tags=["Event Results"],
)


@router.get("/", response_model=Union[EventResultsPublic, EventResultsGroupedPublic])
def get_event_results_route(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
    disc_event_id: int | None = None,
    group_by_division: bool = False,
    sort_by_position_raw: bool = False,
):
    """
    Retrieve a list of EventResults with optional pagination and filtering.

    Query Parameters:
    - disc_event_id: Filter results by disc event
    - username: Filter results by username
    - skip: Number of records to skip for pagination
    - limit: Maximum number of records to return
        - group_by_division: If true, group results by `division` and return a structure
            where each division contains its list of results.
        - sort_by_position_raw: If true, sort results by `position_raw` (numeric positions
            first, None values such as DNF last). This flag works for both grouped and
            ungrouped responses and can be combined with `group_by_division`.
    """
    if disc_event_id:
        disc_event = get_disc_event(session, disc_event_id)
        if not disc_event:
            raise HTTPException(
                status_code=404,
                detail=f"Disc event with ID {disc_event_id} not found",
            )

        raw_results = get_event_results_by_disc_event(
            db=session, disc_event_id=disc_event_id, skip=skip, limit=limit
        )
        # Optionally group results by division
        if group_by_division:
            divisions: dict[str, list] = {}
            for r in raw_results:
                divisions.setdefault(r.division, []).append(r)
            grouped = []
            for division, items in sorted(divisions.items()):
                if sort_by_position_raw:
                    items_sorted = sorted(
                        items, key=lambda x: (x.position_raw is None, x.position_raw)
                    )
                else:
                    items_sorted = items
                grouped.append({"division": division, "results": items_sorted})
            return {"grouped": grouped}
        # Return empty list for valid disc event with no results
        return {"event_results": raw_results or []}
    else:
        raw_results = get_event_results(db=session, skip=skip, limit=limit)
        if not raw_results:
            raise HTTPException(status_code=404, detail="No EventResults found")
        if group_by_division:
            divisions: dict[str, list] = {}
            for r in raw_results:
                divisions.setdefault(r.division, []).append(r)
            grouped = []
            for division, items in sorted(divisions.items()):
                if sort_by_position_raw:
                    items_sorted = sorted(
                        items, key=lambda x: (x.position_raw is None, x.position_raw)
                    )
                else:
                    items_sorted = items
                grouped.append({"division": division, "results": items_sorted})
            return {"grouped": grouped}
        return {"event_results": raw_results}


@router.post("/", response_model=EventResultPublic, status_code=201)
def create_event_result_route(event_result: EventResultCreate, session: SessionDep):
    """
    Create a new EventResult.
    Returns the created EventResult.
    """
    disc_event = get_disc_event(session, event_result.disc_event_id)
    if not disc_event:
        raise HTTPException(
            status_code=422,
            detail=(f"disc_event_id {event_result.disc_event_id} does not exist."),
        )

    existing_results = get_event_results_by_username(
        db=session, username=event_result.username
    )
    if existing_results:
        for existing in existing_results:
            if existing.date.date() == event_result.date.date():
                raise HTTPException(
                    status_code=409,
                    detail=f"Event result for username '{event_result.username}' "
                    f"on date '{event_result.date.date()}' already exists",
                )

    return create_event_result(db=session, event_result=event_result)


@router.get("/aggregated", response_model=EventResultStats)
def get_aggregated_event_results(
    session: SessionDep,
    disc_event_id: int | None = None,
    division: str | None = None,
):
    """
    Retrieve aggregated event results.
    """
    stats = get_median_round_score(
        db=session, disc_event_id=disc_event_id, division=division
    )
    if not stats:
        raise HTTPException(status_code=404, detail="No event results found.")
    return stats


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


@router.get("/username/{event_user}")
def get_event_results_by_user_route(event_user: str, session: SessionDep):
    """
    Retrieve event results by username.
    Returns 404 if no results found for the user.
    """
    user_events = get_event_results_by_username(db=session, username=event_user)
    if not user_events:
        raise HTTPException(
            status_code=404, detail=f"No events found for user: {event_user}"
        )
    return user_events
