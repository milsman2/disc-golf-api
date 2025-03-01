"""
Create a declarative base class to be inherited by all models.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all models.
    """
