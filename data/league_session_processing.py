"""
Functions for processing and posting disc golf league session data to the API.

This module reads league session data from JSON files in a specified directory,
validates the data using Pydantic schemas, and posts valid league sessions to the API.
It provides error handling for validation and HTTP request failures.
"""

import json
import os

import httpx
from icecream import ic
from pydantic import ValidationError

from src.schemas.league_sessions import LeagueSessionCreate


def post_league_session(data_directory: str = "data/league_sessions/") -> None:
    """
    Reads all JSON files in the specified directory, validates each as a
    LeagueSessionCreate object, and posts valid league sessions to the API endpoint.

    Args:
        data_directory (str): Path to the directory containing
        league session JSON files.

    Returns:
        None

    Side Effects:
        Posts each valid league session to the API at /api/v1/league_sessions/.
        Logs validation and HTTP errors using icecream.
    """
    for filename in os.listdir(data_directory):
        if filename.endswith(".json"):
            with open(os.path.join(data_directory, filename), encoding="utf-8") as f:
                league_session_data = json.load(f)
                try:
                    league_session = LeagueSessionCreate.model_validate(
                        league_session_data
                    )
                except ValidationError as e:
                    ic(e)
                    league_session = None
                if league_session is not None:
                    try:
                        response = httpx.post(
                            "http://localhost:8000/api/v1/league_sessions/",
                            json=league_session.model_dump(mode="json"),
                            headers={"Content-Type": "application/json"},
                        )
                        response.raise_for_status()
                        return response.json()
                    except httpx.HTTPStatusError as e:
                        ic(e)
                    except httpx.RequestError as e:
                        ic(e)


if __name__ == "__main__":
    post_league_session()
