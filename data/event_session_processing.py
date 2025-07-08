"""
Functions for processing and posting disc golf event session data to the API.

This module reads event session data from JSON files in a specified directory,
validates the data using Pydantic schemas, and posts valid event sessions to the API.
It provides error handling for validation and HTTP request failures.
"""

import json
import os

import httpx
from icecream import ic
from pydantic import ValidationError

from src.schemas.event_sessions import EventSessionCreate


def post_event_session(data_directory: str = "data/event_sessions/") -> None:
    """
    Reads all JSON files in the specified directory, validates each as a
    EventSessionCreate object, and posts valid event sessions to the API endpoint.

    Args:
        data_directory (str): Path to the directory containing
        event session JSON files.

    Returns:
        None

    Side Effects:
        Posts each valid event session to the API at /api/v1/event_sessions/.
        Logs validation and HTTP errors using icecream.
    """
    for filename in os.listdir(data_directory):
        if filename.endswith(".json"):
            with open(os.path.join(data_directory, filename), encoding="utf-8") as f:
                event_session_data = json.load(f)
                try:
                    event_session = EventSessionCreate.model_validate(
                        event_session_data
                    )
                except ValidationError as e:
                    ic(e)
                    event_session = None
                if event_session is not None:
                    try:
                        response = httpx.post(
                            "http://localhost:8000/api/v1/event_sessions/",
                            json=event_session.model_dump(mode="json"),
                            headers={"Content-Type": "application/json"},
                        )
                        response.raise_for_status()
                        return response.json()
                    except httpx.HTTPStatusError as e:
                        ic(e)
                    except httpx.RequestError as e:
                        ic(e)


if __name__ == "__main__":
    post_event_session()
