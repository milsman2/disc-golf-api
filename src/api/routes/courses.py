"""
Courses API routes
"""

from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
from src.crud.course import create_course, delete_course, get_course, get_courses
from src.schemas.courses import CoursePublic, CourseCreate, CoursesPublic

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=CoursesPublic)
def read_courses(session: SessionDep, skip: int = 0, limit: int = 100):
    courses = get_courses(db=session, skip=skip, limit=limit)
    return courses


@router.get("/{course_id}", response_model=CoursePublic)
def read_course(session: SessionDep, course_id: int):
    db_course = get_course(db=session, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.post("/", response_model=CoursePublic)
def create_new_course(
    session: SessionDep,
    course: CourseCreate,
):
    return create_course(db=session, course=course)


@router.delete("/{course_id}", response_model=CoursePublic)
def delete_existing_course(session: SessionDep, course_id: int):
    db_course = delete_course(db=session, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course
