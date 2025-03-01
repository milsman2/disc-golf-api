"""
Expose CRUD operations for the User model.
"""

from src.crud.user import authenticate, create_user, get_user_by_email, update_user

__all__ = ["create_user", "get_user_by_email", "authenticate", "update_user"]
