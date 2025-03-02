"""
Courses API routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.api.deps import get_db
from src.schemas.courses import Course, CourseCreate
from src.crud.course import (
    get_course,
    get_courses,
    create_course,
    delete_course,
)

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=List[Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = get_courses(db, skip=skip, limit=limit)
    return courses


@router.get("/{course_id}", response_model=Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.post("/", response_model=Course)
def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db=db, course=course)


@router.delete("/{course_id}", response_model=Course)
def delete_existing_course(course_id: int, db: Session = Depends(get_db)):
    db_course = delete_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course
