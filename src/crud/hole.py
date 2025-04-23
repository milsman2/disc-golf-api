"""
CRUD for Hole
"""

from sqlalchemy.orm import Session

from src.models import Hole
from src.schemas import HoleCreate, HoleUpdate


def get_hole(db: Session, hole_id: int) -> Hole | None:
    return db.query(Hole).filter(Hole.id == hole_id).first()


def get_holes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Hole).offset(skip).limit(limit).all()


def create_hole(db: Session, hole: HoleCreate) -> Hole:
    db_hole = Hole(**hole.dict())
    db.add(db_hole)
    db.commit()
    db.refresh(db_hole)
    return db_hole


def update_hole(db: Session, hole_id: int, hole: HoleUpdate) -> Hole | None:
    db_hole = db.query(Hole).filter(Hole.id == hole_id).first()
    if db_hole:
        for key, value in hole.model_dump(exclude_unset=True).items():
            setattr(db_hole, key, value)
        db.commit()
        db.refresh(db_hole)
    return db_hole


def delete_hole(db: Session, hole_id: int) -> Hole | None:
    db_hole = db.query(Hole).filter(Hole.id == hole_id).first()
    if db_hole:
        db.delete(db_hole)
        db.commit()
    return db_hole
