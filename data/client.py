"""
Shared HTTP client and centralized request/exception handling for
data modules. Provides get_json and post_json helpers using a common
base URL and consistent error handling.
"""

import httpx
from icecream import ic

from src.core.config import settings


def _request_json(method, url, *, params=None, json=None, headers=None):
    """
    Internal helper to make HTTP requests using the shared client,
    with centralized exception handling. Returns (response, error) tuple.
    Only one will be non-None.
    """
    try:
        with httpx.Client(base_url=settings.api_base_url) as client:
            ic(settings.api_base_url)
            if method == "GET":
                response = client.get(url, params=params, headers=headers)
            elif method == "POST":
                response = client.post(url, json=json, headers=headers)
            else:
                return None, f"Unsupported HTTP method: {method}"
            response.raise_for_status()
            return response, None
    except (
        httpx.ConnectError,
        httpx.TimeoutException,
        httpx.HTTPStatusError,
        httpx.RequestError,
    ) as e:
        return None, f"HTTP error: {e}"


def get_json(url, params=None, headers=None):
    """
    Helper to GET JSON using the shared client, with centralized exception handling.
    Returns (response, error) tuple. Only one will be non-None.
    """
    return _request_json("GET", url, params=params, headers=headers)


def post_json(url, json=None, headers=None):
    """
    Helper to POST JSON using the shared client, with centralized exception handling.
    Returns (response, error) tuple. Only one will be non-None.
    """
    return _request_json("POST", url, json=json, headers=headers)
