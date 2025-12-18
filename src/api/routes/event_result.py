"""API routes for EventResult resources."""

from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
from src.crud import (
    create_event_result,
    delete_event_result,
    get_disc_event,
    get_disc_event_summary,
    get_event_result,
    get_event_results,
    get_event_results_by_disc_event,
    get_event_results_with_division_stats,
    get_multiple_disc_event_summaries,
    get_round_score_statistics,
    update_event_result,
)
from src.crud.event_result import get_event_results_by_username
from src.schemas.event_results import (
    EventResultCreate,
    EventResultPublic,
    EventResultsGroupedPublic,
    EventResultsGroupedWithStatsPublic,
    EventResultsPublic,
    EventResultStats,
)

router = APIRouter(
    prefix="/event-results",
    tags=["Event Results"],
)


@router.get(
    "/",
    response_model=EventResultsPublic
    | EventResultsGroupedPublic
    | EventResultsGroupedWithStatsPublic,
)
def get_event_results_route(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
    disc_event_id: int | None = None,
    group_by_division: bool = False,
    sort_by_position_raw: bool = False,
    include_stats: bool = False,
):
    """Retrieve event results with optional pagination, filtering, and grouping."""
    if disc_event_id:
        disc_event = get_disc_event(session, disc_event_id)
        if not disc_event:
            raise HTTPException(
                status_code=404,
                detail=f"Disc event with ID {disc_event_id} not found",
            )

        # Enhanced grouping with statistics
        if group_by_division and include_stats:
            division_data = get_event_results_with_division_stats(
                db=session, disc_event_id=disc_event_id, skip=skip, limit=limit
            )
            grouped_with_stats = []
            for division, data_dict in sorted(division_data.items()):
                grouped_with_stats.append(
                    {
                        "division": division,
                        "stats": data_dict["stats"],
                        "results": data_dict["results"],
                    }
                )
            return {"disc_event_id": disc_event_id, "grouped": grouped_with_stats}

        # Original grouping logic
        raw_results = get_event_results_by_disc_event(
            db=session, disc_event_id=disc_event_id, skip=skip, limit=limit
        )
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

        return {"event_results": raw_results or []}
    else:
        # Handle case where no specific disc_event_id is provided
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
def create_event_result_route(
    session: SessionDep,
    event_result: EventResultCreate,
):
    """Create a new EventResult."""
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
    """Retrieve aggregated event results statistics."""
    stats = get_round_score_statistics(
        db=session, disc_event_id=disc_event_id, division=division
    )
    if not stats:
        raise HTTPException(status_code=404, detail="No event results found.")
    return stats


@router.get("/id/{event_result_id}", response_model=EventResultPublic)
def get_event_result_by_id(session: SessionDep, event_result_id: int):
    """Retrieve an EventResult by its ID, or return 404 if not found."""
    db_event_result = get_event_result(db=session, event_result_id=event_result_id)
    if not db_event_result:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return db_event_result


@router.put("/id/{event_result_id}", response_model=EventResultPublic)
def update_event_result_route(
    session: SessionDep,
    event_result_id: int,
    updated_event_result: EventResultCreate,
):
    """Update an EventResult by ID."""
    db_event_result = update_event_result(
        db=session,
        event_result_id=event_result_id,
        updated_event_result=updated_event_result,
    )
    if not db_event_result:
        raise HTTPException(status_code=404, detail="EventResult not found")
    return db_event_result


def delete_event_result_route(session: SessionDep, event_result_id: int):
    """Delete an EventResult by ID."""
    success = delete_event_result(db=session, event_result_id=event_result_id)
    if not success:
        raise HTTPException(status_code=404, detail="EventResult not found")


def get_multiple_event_summaries_route(
    session: SessionDep,
    event_ids: str | None = None,
    skip: int = 0,
    limit: int = 20,
):
    disc_event_ids = None
    if event_ids:
        try:
            disc_event_ids = [int(id.strip()) for id in event_ids.split(",")]
        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail="event_ids must be a comma-separated list of integers",
            ) from exc

    summaries = get_multiple_disc_event_summaries(
        db=session, disc_event_ids=disc_event_ids, skip=skip, limit=limit
    )

    if not summaries:
        raise HTTPException(status_code=404, detail="No event summaries found")

    return {"events": summaries}


def get_disc_event_summary_route(session: SessionDep, disc_event_id: int):
    """Get comprehensive summary of a disc event including division statistics."""
    summary = get_disc_event_summary(db=session, disc_event_id=disc_event_id)
    if not summary:
        raise HTTPException(
            status_code=404,
            detail=f"No event results found for disc event ID {disc_event_id}",
        )
    return summary


@router.get("/username/{event_user}", response_model=EventResultsPublic)
def get_event_results_by_user_route(session: SessionDep, event_user: str):
    """Retrieve event results by username."""
    user_events = get_event_results_by_username(db=session, username=event_user)
    if not user_events:
        raise HTTPException(
            status_code=404, detail=f"No events found for user: {event_user}"
        )
    return {"event_results": user_events}
