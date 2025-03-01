"""
Login routes
"""

from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.api.deps import CurrentUser, SessionDep
from src.core import security, settings
from src.core.security import get_password_hash
from src.crud import authenticate, get_user_by_email
from src.schemas import Message, NewPassword, Token, UserPublic
from src.utils import (
    verify_password_reset_token,
)

router = APIRouter(prefix="/login", tags=["Login"])


@router.post("/access-token")
def login_access_token(
    response: Response,
    db: SessionDep,
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(session=db, email=data.username, password=data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email/password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_exp = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.id, expires_delta=access_token_exp
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.post("/test-token", response_model=UserPublic)
def test_token(request: Request, current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return current_user


@router.post("/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    return Message(message="Password updated successfully")
