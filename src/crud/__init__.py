"""
Expose CRUD operations for the User model.
"""

from src.crud.user import authenticate, create_user, get_user_by_email, update_user
from src.crud.course import (
    create_course,
    get_course,
    get_courses,
    delete_course,
    get_course_by_name,
)
from src.crud.course_layout import (
    create_course_layout,
    get_course_layout,
    get_course_layouts,
    delete_course_layout,
)

__all__ = [
    "create_user",
    "get_user_by_email",
    "authenticate",
    "update_user",
    "create_course",
    "get_course",
    "get_courses",
    "delete_course",
    "get_course_by_name",
    "create_course_layout",
    "get_course_layout",
    "get_course_layouts",
    "delete_course_layout",
]
