"""
Pre-startup utilities for database readiness and retry logic.
"""

from icecream import ic
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_fixed

from src.api import session_local

max_tries = 60 * 5
wait_seconds = 1


def before_retry(retry_state):
    ic(f"Retrying... Attempt {retry_state.attempt_number}")


def after_retry(retry_state):
    ic(f"Retry failed. Attempt {retry_state.attempt_number}")


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_retry,
    after=after_retry,
)
def init() -> None:
    """
    Initialize the database connection and check if the database is awake.
    """
    ic()
    session: Session = session_local()
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError as e:
        ic(e)
        raise e
    finally:
        session.close()


def main() -> None:
    ic("Initializing service")
    init()
    ic("Service finished initializing")


if __name__ == "__main__":
    main()
