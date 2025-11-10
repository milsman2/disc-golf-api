"""
CRUD operations for EventResult resources.

This module provides functions to perform Create, Read, Update, and Delete (CRUD)
operations on EventResult resources in the database. These functions interact
with the SQLAlchemy ORM models and are used by the FastAPI routes to manage
EventResult data.
"""

from typing import Any, Dict

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import functions

from src.models.disc_event import DiscEvent as DiscEventModel
from src.models.event_result import EventResult as EventResultModel
from src.schemas.event_results import (
    DiscEventSummary,
    DivisionStats,
    EventResultCreate,
    EventResultStats,
)


def get_event_result(db: Session, event_result_id: int) -> EventResultModel | None:
    """Retrieve a single EventResult by its ID."""
    return (
        db.query(EventResultModel)
        .options(joinedload(EventResultModel.course_layout))
        .filter(EventResultModel.id == event_result_id)
        .first()
    )


def get_event_results(
    db: Session, skip: int = 0, limit: int = 100
) -> list[EventResultModel]:
    """Get a list of EventResults with optional pagination."""
    return (
        db.query(EventResultModel)
        .options(joinedload(EventResultModel.course_layout))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_event_results_by_username(db: Session, username: str) -> list[EventResultModel]:
    """Get all event results for a specific username."""
    return (
        db.query(EventResultModel).filter(EventResultModel.username == username).all()
    )


def get_event_results_by_disc_event(
    db: Session, disc_event_id: int, skip: int = 0, limit: int = 100
) -> list[EventResultModel]:
    """Retrieve all event results for a specific disc event with pagination."""
    return (
        db.query(EventResultModel)
        .filter(EventResultModel.disc_event_id == disc_event_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_round_score_statistics(
    db: Session, disc_event_id: int | None = None, division: str | None = None
) -> EventResultStats:
    """Calculate comprehensive round score statistics for event results."""
    base_query = db.query(EventResultModel.round_total_score).filter(
        EventResultModel.round_total_score.isnot(None)
    )
    if disc_event_id is not None:
        base_query = base_query.filter(EventResultModel.disc_event_id == disc_event_id)
    if division is not None:
        base_query = base_query.filter(EventResultModel.division == division)

    median = base_query.with_entities(
        functions.percentile_cont(0.5).within_group(
            EventResultModel.round_total_score.asc()
        )
    ).scalar()
    mode = base_query.with_entities(
        functions.mode().within_group(EventResultModel.round_total_score.asc())
    ).scalar()
    min_score = base_query.with_entities(
        functions.min(EventResultModel.round_total_score)
    ).scalar()
    max_score = base_query.with_entities(
        functions.max(EventResultModel.round_total_score)
    ).scalar()
    count = base_query.with_entities(
        functions.count(EventResultModel.round_total_score)
    ).scalar()

    return EventResultStats(
        disc_event_id=disc_event_id,
        division=division,
        median=float(median) if median is not None else None,
        mode=float(mode) if mode is not None else None,
        minimum=float(min_score) if min_score is not None else None,
        maximum=float(max_score) if max_score is not None else None,
        count=int(count) if count is not None else 0,
    )


def create_event_result(
    db: Session, event_result: EventResultCreate
) -> EventResultModel:
    """Create a new EventResult in the database."""
    db_event_result = EventResultModel(**event_result.model_dump())
    db.add(db_event_result)
    db.commit()
    db.refresh(db_event_result)
    return db_event_result


def update_event_result(
    db: Session, event_result_id: int, updated_event_result: EventResultCreate
) -> EventResultModel | None:
    """Update an existing EventResult by its ID."""
    db_event_result = (
        db.query(EventResultModel)
        .filter(EventResultModel.id == event_result_id)
        .first()
    )
    if not db_event_result:
        return None
    for key, value in updated_event_result.model_dump().items():
        setattr(db_event_result, key, value)
    db.commit()
    db.refresh(db_event_result)
    return db_event_result


def delete_event_result(db: Session, event_result_id: int) -> bool:
    """Delete an EventResult by its ID."""
    db_event_result = (
        db.query(EventResultModel)
        .filter(EventResultModel.id == event_result_id)
        .first()
    )
    if not db_event_result:
        return False
    db.delete(db_event_result)
    db.commit()
    return True


def get_division_stats(
    db: Session, disc_event_id: int, division: str
) -> DivisionStats | None:
    """Calculate comprehensive statistics for a specific division
    within a disc event."""
    query = db.query(EventResultModel).filter(
        EventResultModel.disc_event_id == disc_event_id,
        EventResultModel.division == division,
    )
    results = query.all()
    if not results:
        return None
    round_scores = [
        r.round_total_score for r in results if r.round_total_score is not None
    ]
    event_scores = [
        r.event_total_score for r in results if r.event_total_score is not None
    ]
    if not round_scores:
        return None
    return DivisionStats(
        division=division,
        count=len(results),
        average_round_score=sum(round_scores) / len(round_scores),
        median_round_score=sorted(round_scores)[len(round_scores) // 2],
        average_event_score=(
            sum(event_scores) / len(event_scores) if event_scores else None
        ),
        median_event_score=(
            sorted(event_scores)[len(event_scores) // 2] if event_scores else None
        ),
        best_round_score=min(round_scores),
        worst_round_score=max(round_scores),
        best_event_score=min(event_scores) if event_scores else None,
        worst_event_score=max(event_scores) if event_scores else None,
    )


def get_event_results_with_division_stats(
    db: Session, disc_event_id: int, skip: int = 0, limit: int = 100
) -> Dict[str, Dict[str, Any]]:
    """Get event results grouped by division with statistics for each division."""
    all_results = (
        db.query(EventResultModel)
        .filter(EventResultModel.disc_event_id == disc_event_id)
        .all()
    )
    if not all_results:
        return {}
    divisions = {}
    for result in all_results:
        if result.division not in divisions:
            divisions[result.division] = []
        divisions[result.division].append(result)
    division_data = {}
    for division, results in divisions.items():
        sorted_results = sorted(
            results, key=lambda x: (x.position_raw is None, x.position_raw)
        )
        paginated_results = sorted_results[skip : skip + limit]
        stats = get_division_stats(db, disc_event_id, division)
        division_data[division] = {"stats": stats, "results": paginated_results}
    return division_data


def get_disc_event_summary(db: Session, disc_event_id: int) -> DiscEventSummary | None:
    """Get a comprehensive summary of a disc event including division statistics."""
    disc_event = (
        db.query(DiscEventModel).filter(DiscEventModel.id == disc_event_id).first()
    )
    if not disc_event:
        return None
    results = (
        db.query(EventResultModel)
        .filter(EventResultModel.disc_event_id == disc_event_id)
        .all()
    )
    if not results:
        return DiscEventSummary(
            disc_event_id=disc_event_id,
            event_name=disc_event.name,
            event_date=disc_event.start_date,
            total_players=0,
            division_stats=[],
        )
    divisions = set(result.division for result in results)
    division_stats = []
    for division in sorted(divisions):
        stats = get_division_stats(db, disc_event_id, division)
        if stats:
            division_stats.append(stats)
    return DiscEventSummary(
        disc_event_id=disc_event_id,
        event_name=disc_event.name,
        event_date=disc_event.start_date,
        total_players=len(results),
        division_stats=division_stats,
    )


def get_multiple_disc_event_summaries(
    db: Session,
    disc_event_ids: list[int] | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[DiscEventSummary]:
    """Get summaries for multiple disc events."""
    if disc_event_ids:
        summaries = []
        for event_id in disc_event_ids:
            summary = get_disc_event_summary(db, event_id)
            if summary:
                summaries.append(summary)
        return summaries
    unique_event_ids = (
        db.query(EventResultModel.disc_event_id)
        .distinct()
        .offset(skip)
        .limit(limit)
        .all()
    )
    event_ids = [row.disc_event_id for row in unique_event_ids]
    summaries = []
    for event_id in event_ids:
        summary = get_disc_event_summary(db, event_id)
        if summary:
            summaries.append(summary)
    return summaries
