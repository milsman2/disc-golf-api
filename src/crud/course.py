"""
CRUD operations for the Course model
"""

from sqlalchemy.orm import Session, joinedload

from src.models import Course, CourseLayout
from src.models.hole import Hole
from src.schemas.courses import CourseCreate


def get_course(db: Session, course_id: int) -> Course | None:
    return (
        db.query(Course)
        .options(joinedload(Course.layouts).joinedload(CourseLayout.holes))
        .filter(Course.id == course_id)
        .first()
    )


def get_courses(db: Session, skip: int = 0, limit: int = 100) -> list[Course]:
    courses = (
        db.query(Course)
        .options(joinedload(Course.layouts).joinedload(CourseLayout.holes))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return courses


def get_course_by_name(db: Session, name: str) -> Course | None:
    return (
        db.query(Course)
        .options(joinedload(Course.layouts).joinedload(CourseLayout.holes))
        .filter(Course.name == name)
        .first()
    )


def create_course(db: Session, course: CourseCreate) -> Course:
    db_course = Course(
        name=course.name,
        location=course.location,
        description=course.description,
        city=course.city,
        state=course.state,
        country=course.country,
        holes=course.holes,
        rating=course.rating,
        reviews_count=course.reviews_count,
        link=course.link,
        conditions=course.conditions,
        conditions_updated=course.conditions_updated,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    for layout in course.layouts:
        db_layout = CourseLayout(
            name=layout.name,
            course_id=db_course.id,
            par=layout.par,
            length=layout.length,
            difficulty=layout.difficulty,
        )
        db.add(db_layout)
        db.commit()
        db.refresh(db_layout)

        for hole in layout.holes:
            db_hole = Hole(
                hole_name=hole.hole_name,
                par=hole.par,
                distance=hole.distance,
                layout_id=db_layout.id,
            )
            db.add(db_hole)
        db.commit()

    return db_course


def delete_course(db: Session, course_id: int) -> Course | None:
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return db_course
    return None
