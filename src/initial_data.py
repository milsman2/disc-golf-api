"""
Populate the database with initial data (schema and seed data).
Run create_db_and_roles.py separately for DB/role creation if needed.
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
    Main function to initialize schema and seed data.
    Run create_db_and_roles.py separately for DB/role creation if needed.
    """
    init()
    ic("Initial data created")
    ic(settings.ENVIRONMENT)


if __name__ == "__main__":
    main()
