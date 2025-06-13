"""
API routes for managing disc golf league sessions.

This module defines FastAPI endpoints for creating, retrieving, updating, and deleting
LeagueSession records. It supports operations such as fetching a single league
session by ID, listing all league sessions with pagination, and handling standard HTTP
errors for not found resources. The endpoints use Pydantic schemas for request
validation and response serialization.
"""

from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
from src.crud.league_session import (
    create_league_session,
    delete_league_session,
    get_league_session,
    get_league_sessions,
    update_league_session,
)
from src.schemas import LeagueSessionCreate, LeagueSessionPublic, LeagueSessionUpdate

router = APIRouter(prefix="/league_sessions", tags=["league_sessions"])


@router.get("/{league_session_id}", response_model=LeagueSessionPublic)
def get_league_session_route(
    league_session_id: int,
    db: SessionDep,
):
    """
    Get a league session by ID.
    """
    league_session = get_league_session(db, league_session_id)
    if not league_session:
        raise HTTPException(status_code=404, detail="League session not found")
    return league_session


@router.get("/", response_model=list[LeagueSessionPublic])
def get_league_sessions_route(db: SessionDep, skip: int = 0, limit: int = 100):
    """
    Get a list of league sessions with pagination.
    """
    return get_league_sessions(db, skip=skip, limit=limit)


@router.post("/", response_model=LeagueSessionPublic, status_code=201)
def create_league_session_route(
    league_session: LeagueSessionCreate,
    db: SessionDep,
):
    """
    Create a new league session.
    """
    return create_league_session(db, league_session)


@router.delete("/{league_session_id}", response_model=LeagueSessionPublic)
def delete_league_session_route(
    league_session_id: int,
    db: SessionDep,
):
    """
    Delete a league session by ID.
    """
    league_session = delete_league_session(db, league_session_id)
    if not league_session:
        raise HTTPException(status_code=404, detail="League session not found")
    return league_session


@router.put("/{league_session_id}", response_model=LeagueSessionPublic)
def update_league_session_route(
    league_session_id: int,
    league_session_data: LeagueSessionUpdate,
    db: SessionDep,
):
    """
    Update a league session by ID.
    """
    league_session = update_league_session(db, league_session_id, league_session_data)
    if not league_session:
        raise HTTPException(status_code=404, detail="League session not found")
    return league_session
