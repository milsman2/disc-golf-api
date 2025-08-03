"""
Courses API routes
"""

from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
from src.crud.course import (
    create_course,
    delete_course,
    get_course,
    get_course_by_name,
    get_courses,
)
from src.schemas.courses import CourseCreate, CoursePublic, CoursesPublic

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=CoursesPublic)
def read_courses(session: SessionDep, skip: int = 0, limit: int = 100):
    courses_data = get_courses(db=session, skip=skip, limit=limit)
    return {"courses": courses_data}


@router.get("/{course_id}", response_model=CoursePublic)
def read_course(session: SessionDep, course_id: int):
    db_course = get_course(db=session, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.get("/{course_name}", response_model=CoursePublic)
def read_course_by_name(session: SessionDep, course_name: str):
    db_course = get_course_by_name(db=session, name=course_name)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.post("/", response_model=CoursePublic, status_code=201)
def create_new_course(session: SessionDep, course: CourseCreate):
    course_check = get_course_by_name(db=session, name=course.name)
    if course_check is not None:
        raise HTTPException(status_code=409, detail="Course already exists")
    db_course = create_course(db=session, course=course)
    return db_course


@router.delete("/{course_id}", response_model=None, status_code=204)
def delete_existing_course(session: SessionDep, course_id: int):
    db_course = delete_course(db=session, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
