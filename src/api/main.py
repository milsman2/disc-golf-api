"""
Main module for the API
"""

from fastapi import APIRouter

from src.api.routes import (
    courses_layouts_router,
    courses_router,
    event_result_router,
    event_sessions_router,
    healthcheck_router,
    login_router,
    private_router,
)
from src.core import settings

api_router = APIRouter()

api_router.include_router(healthcheck_router)
api_router.include_router(login_router)
api_router.include_router(courses_layouts_router)
api_router.include_router(courses_router)
api_router.include_router(private_router)
api_router.include_router(event_result_router)
api_router.include_router(event_sessions_router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private_router)
