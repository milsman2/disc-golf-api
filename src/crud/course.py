"""
CRUD operations for the Course model
"""

from sqlalchemy.orm import Session, joinedload

from src.models import Course, CourseLayout
from src.models.hole import Hole
from src.schemas.courses import CourseCreate, CourseUpdate


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
    # Build Course model instance (exclude nested layouts)
    course_data = course.model_dump(exclude={"layouts"})
    db_course = Course(**course_data)

    # If layouts provided, build CourseLayout and Hole model instances and attach
    layouts_payload = getattr(course, "layouts", None)
    if layouts_payload:
        layout_objs: list[CourseLayout] = []
        for layout in layouts_payload:
            layout_data = layout.model_dump(exclude={"holes", "course_id"})
            db_layout = CourseLayout(**layout_data)

            # build holes and attach to layout (SQLAlchemy will set layout_id on flush)
            holes_payload = getattr(layout, "holes", None)
            if holes_payload:
                hole_objs: list[Hole] = []
                for hole in holes_payload:
                    hole_data = hole.model_dump()
                    hole_objs.append(Hole(**hole_data))
                db_layout.holes = hole_objs

            layout_objs.append(db_layout)

        db_course.layouts = layout_objs

    # Persist the complete object graph in one transaction
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int) -> Course | None:
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return db_course
    return None


def update_course(db: Session, course_id: int, course: CourseUpdate) -> Course | None:
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        update_data = course.model_dump(exclude_unset=True, exclude={"layouts"})
        for field, value in update_data.items():
            setattr(db_course, field, value)
        db.commit()
        db.refresh(db_course)
        return db_course
    return None
