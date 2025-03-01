"""
Utility functions for sending emails and generating tokens.
"""

from datetime import datetime, timedelta, timezone

import jwt
from icecream import ic
from jwt.exceptions import InvalidTokenError

from src.core import security, settings


def generate_password_reset_token(email: str) -> str:
    ic()
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=security.ALGO,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGO]
        )
        return str(decoded_token["sub"])
    except InvalidTokenError:
        return None
