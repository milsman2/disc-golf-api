"""
API routes for managing Course resources.

This module provides RESTful endpoints for CRUD operations on Course objects.
Courses represent disc golf courses with their layouts, holes, and metadata.

Routes (grouped by endpoint path, ordered by HTTP method):
- Collection endpoints (/courses):
  - GET /courses: Retrieve all courses with pagination
  - POST /courses: Create a new course
- Item endpoints (/courses/id/{id}):
  - GET /courses/id/{course_id}: Retrieve a single course by ID
  - PUT /courses/id/{course_id}: Update an existing course
  - DELETE /courses/id/{course_id}: Delete a course
- Search endpoints (/courses/name/{name}):
  - GET /courses/name/{course_name}: Retrieve a course by name

Dependencies:
- SessionDep: Database session dependency injection
- Pydantic schemas for request/response validation
- CRUD operations with proper error handling
"""

from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
from src.crud.course import (
    create_course,
    delete_course,
    get_course,
    get_course_by_name,
    get_courses,
    update_course,
)
from src.schemas.courses import CourseCreate, CoursePublic, CoursesPublic, CourseUpdate

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=CoursesPublic)
def read_courses(session: SessionDep, skip: int = 0, limit: int = 100):
    """
    Retrieve all courses with optional pagination.
    """
    courses_data = get_courses(db=session, skip=skip, limit=limit)
    return {"courses": courses_data}


@router.post("/", response_model=CoursePublic, status_code=201)
def create_new_course(session: SessionDep, course: CourseCreate):
    """
    Create a new course.
    """
    course_check = get_course_by_name(db=session, name=course.name)
    if course_check is not None:
        raise HTTPException(status_code=409, detail="Course already exists")
    db_course = create_course(db=session, course=course)
    return db_course


@router.get("/id/{course_id}", response_model=CoursePublic)
def read_course(session: SessionDep, course_id: int):
    """
    Retrieve a single course by ID.
    """
    db_course = get_course(db=session, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.put("/id/{course_id}", response_model=CoursePublic)
def update_existing_course(session: SessionDep, course_id: int, course: CourseUpdate):
    """
    Update an existing course by ID.
    """
    existing_course = get_course(db=session, course_id=course_id)
    if existing_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    updated_course = update_course(db=session, course_id=course_id, course=course)
    return updated_course


@router.delete("/id/{course_id}", response_model=None, status_code=204)
def delete_existing_course(session: SessionDep, course_id: int):
    """
    Delete a course by ID.
    """
    db_course = delete_course(db=session, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")


@router.get("/name/{course_name}", response_model=CoursePublic)
def read_course_by_name(session: SessionDep, course_name: str):
    """
    Retrieve a course by name.
    """
    db_course = get_course_by_name(db=session, name=course_name)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course
