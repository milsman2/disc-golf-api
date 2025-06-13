"""
CRUD operations for disc golf league sessions.

This module provides functions to create, retrieve, update, and
delete LeagueSession records in the database using SQLAlchemy ORM.
It supports operations for single league sessions as well as listing
multiple sessions with pagination.
"""

from sqlalchemy.orm import Session

from src.models import LeagueSession
from src.schemas import LeagueSessionCreate, LeagueSessionUpdate


def create_league_session(
    db: Session, league_session: LeagueSessionCreate
) -> LeagueSession:
    db_league_session = LeagueSession(**league_session.model_dump())
    db.add(db_league_session)
    db.commit()
    db.refresh(db_league_session)
    return db_league_session


def get_league_session(db: Session, league_session_id: int) -> LeagueSession | None:
    return db.query(LeagueSession).filter(LeagueSession.id == league_session_id).first()


def get_league_sessions(
    db: Session, skip: int = 0, limit: int = 100
) -> list[LeagueSession]:
    return db.query(LeagueSession).offset(skip).limit(limit).all()


def delete_league_session(db: Session, league_session_id: int) -> LeagueSession | None:
    db_league_session = (
        db.query(LeagueSession).filter(LeagueSession.id == league_session_id).first()
    )
    if db_league_session:
        db.delete(db_league_session)
        db.commit()
    return db_league_session


def update_league_session(
    db: Session, league_session_id: int, league_session_data: LeagueSessionUpdate
) -> LeagueSession | None:
    db_league_session = (
        db.query(LeagueSession).filter(LeagueSession.id == league_session_id).first()
    )
    if db_league_session:
        for key, value in league_session_data.model_dump().items():
            setattr(db_league_session, key, value)
        db.commit()
        db.refresh(db_league_session)
    return db_league_session
