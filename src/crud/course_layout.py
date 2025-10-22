"""
CRUD for Course Layout
"""

from sqlalchemy.orm import Session

from src.models import CourseLayout
from src.schemas import CourseLayoutCreate
from src.models.hole import Hole


def get_course_layout(db: Session, course_layout_id: int) -> CourseLayout | None:
    return db.query(CourseLayout).filter(CourseLayout.id == course_layout_id).first()


def get_course_layouts(
    db: Session, skip: int = 0, limit: int = 100
) -> list[CourseLayout]:
    return db.query(CourseLayout).offset(skip).limit(limit).all()


def create_course_layout(
    db: Session, course_layout: CourseLayoutCreate
) -> CourseLayout:
    # Build CourseLayout instance from schema, excluding holes
    layout_data = course_layout.model_dump(exclude={"holes"})
    db_course_layout = CourseLayout(**layout_data)

    # If holes are provided, construct Hole instances and attach them
    holes_payload = getattr(course_layout, "holes", None)
    if holes_payload:
        hole_objs: list[Hole] = []
        for hole in holes_payload:
            hole_data = hole.model_dump()
            hole_objs.append(Hole(**hole_data))
        db_course_layout.holes = hole_objs

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
