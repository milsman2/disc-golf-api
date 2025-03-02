"""
CRUD for Course Layout
"""

from sqlalchemy.orm import Session

from src.models import CourseLayout
from src.schemas import CourseLayoutCreate


def get_course_layout(db: Session, course_layout_id: int) -> CourseLayout | None:
    return db.query(CourseLayout).filter(CourseLayout.id == course_layout_id).first()


def get_course_layouts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CourseLayout).offset(skip).limit(limit).all()


def create_course_layout(
    db: Session, course_layout: CourseLayoutCreate
) -> CourseLayout:
    db_course_layout = CourseLayout(**course_layout.dict())
    db.add(db_course_layout)
    db.commit()
    db.refresh(db_course_layout)
    return db_course_layout


def delete_course_layout(db: Session, course_layout_id: int) -> CourseLayout | None:
    db_course_layout = (
        db.query(CourseLayout).filter(CourseLayout.id == course_layout_id).first()
    )
    if db_course_layout:
        db.delete(db_course_layout)
        db.commit()
    return db_course_layout
