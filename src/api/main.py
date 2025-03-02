"""
Main module for the API
"""

from fastapi import APIRouter

from src.api.routes import (
    healthcheck_router,
    login_router,
    courses_layouts_router,
    courses_router,
)

router = APIRouter()

router.include_router(healthcheck_router)
router.include_router(login_router)
router.include_router(courses_layouts_router)
router.include_router(courses_router)
