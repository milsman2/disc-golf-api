"""
Expose the routers to API main module
"""

from src.api.routes.healthcheck import router as healthcheck_router
from src.api.routes.login import router as login_router

__all__ = ["healthcheck_router", "login_router"]
