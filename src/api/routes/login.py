"""
Login routes
"""

from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.api.deps import current_user_dep, session_dep
from src.core import create_access_token, get_password_hash, settings
from src.crud import authenticate, get_user_by_email
from src.schemas import Message, NewPassword, Token, UserPublic
from src.utils import verify_password_reset_token

router = APIRouter(prefix="/login", tags=["Login"])


@router.post("/access-token")
def login_access_token(
    response: Response,
    session: session_dep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(
        db=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_exp = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.id, expires_delta=access_token_exp)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
    )
    return Token(
        access_token=create_access_token(user.id, expires_delta=access_token_exp)
    )


@router.post("/test-token", response_model=UserPublic)
def test_token(current_user: current_user_dep) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/reset-password", response_model=Message)
def reset_password(session: session_dep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user_by_email(db=session, email=email)
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
