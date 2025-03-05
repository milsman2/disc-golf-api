"""
Expose the router from the main module.
"""

from src.api.main import api_router
from src.api.deps import get_current_user, SessionDep

__all__ = ["api_router", "get_current_user", "SessionDep"]
