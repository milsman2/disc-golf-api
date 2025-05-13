"""
This module is used to check if the database is awake before starting the service.
"""

from icecream import ic
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_fixed

from src.core import engine

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
def init(db_engine: Engine) -> None:
    """
    Initialize the database connection and check if the database is awake.
    """
    ic()
    try:
        with Session(db_engine) as session:
            session.execute(select(1))
    except Exception as e:
        ic(e)
        raise e


def main() -> None:
    ic("Initializing service")
    init(engine)
    ic("Service finished initializing")


if __name__ == "__main__":
    main()
