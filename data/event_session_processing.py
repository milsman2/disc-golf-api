"""
Functions for processing and posting disc golf event session data to the API.

This module reads event session data from JSON files in a specified directory,
validates the data using Pydantic schemas, and posts valid event sessions to the API.
It provides comprehensive error handling for validation and HTTP request failures,
and processes all JSON files in the directory.
"""

import json
import os

import httpx
from icecream import ic
from pydantic import ValidationError

from src.schemas.event_sessions import EventSessionCreate


def create_event_sessions(data_directory: str = "data/event_sessions/") -> None:
    """
    Reads all JSON files in the specified directory, validates each as an
    EventSessionCreate object, and posts valid event sessions to the API endpoint.

    The function processes all JSON files in the directory sequentially. If a file
    fails validation, it logs the error and continues with the next file. If an HTTP
    request fails, it logs the error and continues processing remaining files.

    Args:
        data_directory (str): Path to the directory containing event session JSON files.
                             Defaults to "data/event_sessions/".

    Returns:
        None

    Side Effects:
        - Posts each valid event session to the API at /api/v1/event-sessions/
        - Logs validation errors, HTTP errors, and successful operations using icecream
        - Continues processing all files even if individual files fail

    Raises:
        FileNotFoundError: If the specified directory does not exist
        PermissionError: If the directory or files cannot be read
    """
    for filename in os.listdir(data_directory):
        if filename.endswith(".json"):
            with open(os.path.join(data_directory, filename), encoding="utf-8") as f:
                event_session_data = json.load(f)
                try:
                    event_session = EventSessionCreate.model_validate(
                        event_session_data
                    )
                    ic(event_session)
                except ValidationError as e:
                    ic(e)
                    continue
                try:
                    response = httpx.post(
                        "http://localhost:8000/api/v1/event-sessions/",
                        json=event_session.model_dump(mode="json"),
                        headers={"Content-Type": "application/json"},
                    )
                    response.raise_for_status()
                    ic(
                        "Successfully posted event session from "
                        f"{filename}: {response.json()}"
                    )
                except httpx.HTTPStatusError as e:
                    ic(f"HTTP error posting {filename}: {e}")
                except httpx.RequestError as e:
                    ic(f"Request error posting {filename}: {e}")


if __name__ == "__main__":
    create_event_sessions()
