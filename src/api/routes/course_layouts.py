"""
API routes for managing CourseLayout resources.

This module provides RESTful endpoints for CRUD operations on CourseLayout objects.
Course layouts represent different configurations of holes within a disc golf course.

Routes (grouped by endpoint path, ordered by HTTP method):
- Collection endpoints (/course-layouts):
  - GET /course-layouts: Retrieve all course layouts with pagination
  - POST /course-layouts: Create a new course layout
- Item endpoints (/course-layouts/id/{id}):
  - GET /course-layouts/id/{course_layout_id}: Retrieve a single course layout by ID
  - DELETE /course-layouts/id/{course_layout_id}: Delete a course layout
- Search endpoints (/course-layouts/search):
  - GET /course-layouts/search: Search course layouts by course name

Dependencies:
- session_dep: Database session dependency injection
- Pydantic schemas for request/response validation
- CRUD operations with proper error handling
"""

from fastapi import APIRouter, HTTPException

from src.api.deps import session_dep
from src.crud.course import get_course_by_name
from src.crud.course_layout import (
    create_course_layout,
    delete_course_layout,
    get_course_layout,
    get_course_layouts,
)
from src.schemas.course_layouts import (
    CourseLayoutCreate,
    CourseLayoutPublic,
    CourseLayoutsPublic,
)

router = APIRouter(prefix="/course-layouts", tags=["Course Layouts"])


@router.get("/", response_model=CourseLayoutsPublic)
def read_course_layouts(
    session: session_dep,
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all course layouts with optional pagination.
    """
    course_layouts = get_course_layouts(db=session, skip=skip, limit=limit)
    return {"course_layouts": course_layouts, "count": len(course_layouts)}


@router.post("/", response_model=CourseLayoutPublic, status_code=201)
def create_new_course_layout(session: session_dep, course_layout: CourseLayoutCreate):
    """
    Create a new course layout.
    """
    return create_course_layout(db=session, course_layout=course_layout)


@router.get("/id/{course_layout_id}", response_model=CourseLayoutPublic)
def read_course_layout(session: session_dep, course_layout_id: int):
    """
    Retrieve a single course layout by ID.
    """
    db_course_layout = get_course_layout(db=session, course_layout_id=course_layout_id)
    if db_course_layout is None:
        raise HTTPException(status_code=404, detail="Course layout not found")
    return db_course_layout


@router.delete("/id/{course_layout_id}", status_code=204)
def delete_existing_course_layout(session: session_dep, course_layout_id: int):
    """
    Delete a course layout by ID.
    """
    db_course_layout = delete_course_layout(
        db=session, course_layout_id=course_layout_id
    )
    if db_course_layout is None:
        raise HTTPException(status_code=404, detail="Course layout not found")


@router.get("/search", response_model=CourseLayoutsPublic)
def search_course_layouts(session: session_dep, name: str):
    """
    Search course layouts by course name.
    """
    if name:
        db_course = get_course_by_name(db=session, name=name)
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        layouts = db_course.layouts or []
        return {"course_layouts": layouts, "count": len(layouts)}
    else:
        return {"course_layouts": [], "count": 0}
    raise HTTPException(status_code=400, detail="Name parameter is required")
