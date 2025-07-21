"""
Routes for Course Layouts
"""

from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
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
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
):
    course_layouts = get_course_layouts(db=session, skip=skip, limit=limit)
    return course_layouts


@router.get("/{course_layout_id}", response_model=CourseLayoutPublic)
def read_course_layout(session: SessionDep, course_layout_id: int):
    db_course_layout = get_course_layout(db=session, course_layout_id=course_layout_id)
    if db_course_layout is None:
        raise HTTPException(status_code=404, detail="Course layout not found")
    return db_course_layout


@router.post("/", response_model=CourseLayoutPublic)
def create_new_course_layout(session: SessionDep, course_layout: CourseLayoutCreate):
    return create_course_layout(db=session, course_layout=course_layout)


@router.delete("/{course_layout_id}", response_model=CourseLayoutPublic)
def delete_existing_course_layout(session: SessionDep, course_layout_id: int):
    db_course_layout = delete_course_layout(
        db=session, course_layout_id=course_layout_id
    )
    if db_course_layout is None:
        raise HTTPException(status_code=404, detail="Course layout not found")
    return db_course_layout


@router.get("/search", response_model=CourseLayoutsPublic)
def search_course_layouts(session: SessionDep, name: str):
    if name:
        db_course = get_course_by_name(db=session, name=name)
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return db_course.layouts
    raise HTTPException(status_code=400, detail="Name parameter is required")
