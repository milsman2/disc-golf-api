"""
Main module for the API
"""

from fastapi import APIRouter

from src.api.routes import (
    course_layouts_router,
    courses_router,
    disc_event_router,
    event_result_router,
    healthcheck_router,
    login_router,
    private_router,
)
from src.core import settings

api_router = APIRouter()

api_router.include_router(healthcheck_router)
api_router.include_router(login_router)
api_router.include_router(course_layouts_router)
api_router.include_router(courses_router)
api_router.include_router(private_router)
api_router.include_router(event_result_router)
api_router.include_router(disc_event_router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private_router)
