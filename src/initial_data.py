"""
Populate the database with initial data.
"""

from icecream import ic
from sqlalchemy.orm import Session

from src.core import settings
from src.core.db import engine, init_db


def init() -> None:
    """
    Initialize the database with initial data.

    This function creates a new database session and calls the init_db function
    to populate the database with initial data.
    """
    ic()
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    """
    Main function to create initial data.

    This function logs the start and end of the initial data creation process
    and calls the init function to initialize the database.
    """
    ic("Creating initial data")
    init()
    ic("Initial data created")
    ic(settings.ENVIRONMENT)


if __name__ == "__main__":
    main()
