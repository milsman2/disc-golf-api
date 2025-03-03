"""
User CRUD operations.
"""

from typing import Any

from sqlalchemy.orm import Session

from src.core.security import get_password_hash, verify_password
from src.models import User
from src.schemas import UserCreate, UserUpdate


def create_user(*, db: Session, user_create: UserCreate) -> User:
    """
    Create a new user.
    """
    hashed_password = get_password_hash(user_create.password)
    db_obj = User(
        email=user_create.email,
        hashed_password=hashed_password,
        full_name=user_create.full_name,
        is_active=user_create.is_active,
        is_superuser=user_create.is_superuser,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_user(*, db: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    if "password" in user_data:
        password = user_data.pop("password")
        hashed_password = get_password_hash(password)
        db_user.hashed_password = hashed_password
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(*, db: Session, email: str) -> User | None:
    session_user = db.query(User).filter(User.email == email).first()
    return session_user


def authenticate(*, db: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(db=db, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
