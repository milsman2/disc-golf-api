"""
Database connection and session handling.
"""

from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.core import settings
from src.models import Base, User
from src.schemas import UserCreate
from src.crud import create_user

engine = create_engine(
    str(settings.sql_alchemy_db_uri), connect_args=settings.sql_conn_args
)


def init_db(session: Session) -> None:
    ic(session)
    Base.metadata.create_all(bind=engine)
    user = session.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        user = UserCreate(
            email=settings.FIRST_SUPERUSER,
            is_superuser=True,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        create_user(session=session, user_create=user)
        ic("Superuser created")
