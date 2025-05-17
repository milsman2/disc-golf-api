"""
Expose CRUD operations for the User model.
"""

from src.crud.course import (
    create_course,
    delete_course,
    get_course,
    get_course_by_name,
    get_courses,
)
from src.crud.course_layout import (
    create_course_layout,
    delete_course_layout,
    get_course_layout,
    get_course_layouts,
)
from src.crud.event_result import (
    create_event_result,
    delete_event_result,
    get_event_result,
    get_event_results,
    update_event_result,
)
from src.crud.user import authenticate, create_user, get_user_by_email, update_user

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
    "create_event_result",
    "get_event_result",
    "update_event_result",
    "delete_event_result",
    "get_event_results",
]
