"""
All components from modules to make REST API routes for healthchecks
"""

from fastapi import APIRouter

router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])


@router.get("/")
def healthcheck():
    """
    Ping style health check
    """
    return {"status": "ok"}
