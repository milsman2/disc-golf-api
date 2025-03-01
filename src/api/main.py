"""
Main module for the API
"""

from fastapi import APIRouter

from src.api.routes import healthcheck_router
from src.api.routes import login_router

router = APIRouter()

router.include_router(healthcheck_router)
router.include_router(login_router)
