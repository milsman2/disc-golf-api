"""
Private routes are routes that require authentication to access.
"""

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from src.api.deps import SessionDep
from src.core import get_password_hash
from src.schemas import UserPublic
from src.models import User

router = APIRouter(tags=["Private"], prefix="/private")


class PrivateUserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    is_verified: bool = False


@router.post("/users/", response_model=UserPublic)
def create_user(user_in: PrivateUserCreate, session: SessionDep) -> Any:
    """
    Create a new user.
    """

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
    )

    session.add(user)
    session.commit()

    return user
