"""
Routes for Course Layouts
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.api.deps import get_db
from src.schemas.course_layouts import (
    CourseLayout,
    CourseLayoutCreate,
    CourseLayoutUpdate,
)
from src.crud.course_layout import (
    get_course_layout,
    get_course_layouts,
    create_course_layout,
    update_course_layout,
    delete_course_layout,
)

router = APIRouter(prefix="/course_layouts", tags=["Course Layouts"])


@router.get("/", response_model=List[CourseLayout])
def read_course_layouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    course_layouts = get_course_layouts(db, skip=skip, limit=limit)
    return course_layouts


@router.get("/{course_layout_id}", response_model=CourseLayout)
def read_course_layout(course_layout_id: int, db: Session = Depends(get_db)):
    db_course_layout = get_course_layout(db, course_layout_id=course_layout_id)
    if db_course_layout is None:
        raise HTTPException(status_code=404, detail="Course layout not found")
    return db_course_layout


@router.post("/", response_model=CourseLayout)
def create_new_course_layout(
    course_layout: CourseLayoutCreate, db: Session = Depends(get_db)
):
    return create_course_layout(db=db, course_layout=course_layout)


@router.put("/{course_layout_id}", response_model=CourseLayout)
def update_existing_course_layout(
    course_layout_id: int,
    course_layout: CourseLayoutUpdate,
    db: Session = Depends(get_db),
):
    db_course_layout = update_course_layout(
        db, course_layout_id=course_layout_id, course_layout=course_layout
    )
    if db_course_layout is None:
        raise HTTPException(status_code=404, detail="Course layout not found")
    return db_course_layout


@router.delete("/{course_layout_id}", response_model=CourseLayout)
def delete_existing_course_layout(course_layout_id: int, db: Session = Depends(get_db)):
    db_course_layout = delete_course_layout(db, course_layout_id=course_layout_id)
    if db_course_layout is None:
        raise HTTPException(status_code=404, detail="Course layout not found")
    return db_course_layout
