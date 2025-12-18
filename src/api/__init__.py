"""
Expose the router from the main module.
"""

from src.api.deps import SessionDep, TokenDep, get_current_user, session_local
from src.api.main import api_router

__all__ = ["api_router", "get_current_user", "session_local", "SessionDep", "TokenDep"]
