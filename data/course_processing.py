"""
Module for processing and creating disc golf course data.

This script reads course data from a JSON file, validates it using Pydantic schemas,
and sends it to the API endpoint for course creation. It includes error handling for
common issues such as missing keys, validation errors, and HTTP request failures.

Intended for use in development and testing of the course creation API.
"""

import json
import os

from icecream import ic
from pydantic import ValidationError

from data.client import post_json
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
                post_json(
                    url="/courses/",
                    json=course_data_model.model_dump(mode="json"),
                )


if __name__ == "__main__":
    create_courses()
