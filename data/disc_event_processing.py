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

from src.core.config import settings
from src.schemas.disc_events import DiscEventCreate


def create_disc_event(data_directory: str = "data/disc_events/") -> None:
    """
    Reads all JSON files in the specified directory, validates each as a
    DiscEventCreate object, and posts valid disc events to the API endpoint.

    The function processes all JSON files in the directory sequentially. If a file
    fails validation, it logs the error and continues with the next file. If an HTTP
    request fails, it logs the error and continues processing remaining files.

    Args:
        data_directory (str): Path to the directory containing disc event JSON files.
                             Defaults to "data/disc_events/".

    Returns:
        None

    Side Effects:
        - Posts each valid disc event to the API at /api/v1/disc-events/
        - Logs validation errors, HTTP errors, and successful operations using icecream
        - Continues processing all files even if individual files fail

    Raises:
        FileNotFoundError: If the specified directory does not exist
        PermissionError: If the directory or files cannot be read
    """
    for filename in os.listdir(data_directory):
        if filename.endswith(".json"):
            with open(os.path.join(data_directory, filename), encoding="utf-8") as f:
                disc_event_data = json.load(f)
                try:
                    disc_event = DiscEventCreate.model_validate(disc_event_data)
                    ic(disc_event)
                except ValidationError as e:
                    ic(e)
                    continue
                try:
                    with httpx.Client(
                        base_url=settings.api_base_url,
                        timeout=30.0,  # 30 second timeout
                    ) as client:
                        ic(f"Posting to: {settings.api_base_url}/disc-events/")
                        response = client.post(
                            "/disc-events/",
                            json=disc_event.model_dump(mode="json"),
                            headers={"Content-Type": "application/json"},
                        )
                        response.raise_for_status()
                        ic(
                            "Successfully posted disc event from "
                            f"{filename}: {response.json()}"
                        )
                except httpx.ConnectError as e:
                    ic(f"Connection error posting {filename}: {e}")
                    ic(f"Make sure API is running at: {settings.api_base_url}")
                    continue
                except httpx.TimeoutException as e:
                    ic(f"Timeout error posting {filename}: {e}")
                    continue
                except httpx.HTTPStatusError as e:
                    ic(f"HTTP error posting {filename}: {e}")
                    ic(f"Response content: {e.response.text}")
                    continue
                except httpx.RequestError as e:
                    ic(f"Request error posting {filename}: {e}")
                    continue


if __name__ == "__main__":
    create_disc_event()
