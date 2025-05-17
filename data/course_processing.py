"""
Module for processing and creating disc golf course data.

This script reads course data from a JSON file, validates it using Pydantic schemas,
and sends it to the API endpoint for course creation. It includes error handling for
common issues such as missing keys, validation errors, and HTTP request failures.

Intended for use in development and testing of the course creation API.
"""

import json
import os

import httpx
from icecream import ic
from pydantic import ValidationError

from src.schemas.courses import CourseCreate


def create_courses(data_directory: str = "data/courses/") -> None:
    """
    Test creating a course.
    """
    for filename in os.listdir(data_directory):
        if filename.endswith(".json"):
            with open(os.path.join(data_directory, filename), encoding="utf-8") as f:
                course_data = json.load(f)
                try:
                    course_data["layouts"] = [
                        {
                            "name": layout["name"],
                            "par": layout["par"],
                            "length": layout["length"],
                            "difficulty": layout["difficulty"],
                            "holes": [
                                {
                                    "hole_name": hole["hole_name"],
                                    "par": hole["par"],
                                    "distance": hole["distance"],
                                }
                                for hole in layout["holes"]
                            ],
                        }
                        for layout in course_data["layouts"]
                    ]
                except KeyError as e:
                    ic(f"KeyError: {e}")
                    raise

                try:
                    course_data_model = CourseCreate.model_validate(course_data)
                    ic(course_data_model)
                except ValidationError as e:
                    ic(f"ValidationError: {e}")
                    raise
                with httpx.Client(base_url="http://localhost:8000/api/v1") as client:
                    try:
                        response = client.post(
                            "/courses/",
                            json=course_data_model.model_dump(exclude_unset=True),
                            headers={"Content-Type": "application/json"},
                        )
                        response.raise_for_status()
                    except httpx.HTTPStatusError as e:
                        ic(e)
                    except httpx.RequestError as e:
                        ic(e)
                    except json.JSONDecodeError as e:
                        ic(e)


if __name__ == "__main__":
    create_courses()
