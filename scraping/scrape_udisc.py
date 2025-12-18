"""
Scrape UDisc for a list of disc golf courses.
"""

import asyncio

from icecream import ic
from pydantic import ValidationError

from scraping.fetch_course_details import get_course_details
from scraping.fetch_course_pages import get_course_list
from scraping.schemas import generated_url
from src.schemas import CourseCreate


async def main():
    ic()
    courses_list = await get_course_list(url=generated_url)
    course_details = await get_course_details(courses_list)
    for course in course_details:
        try:
            rating = None if course["rating"] == "-" else course["rating"]
            course_out = CourseCreate(
                name=course["name"],
                location=course["location"],
                rating=rating,
                reviews_count=course["reviews_count"],
            )
            ic(course_out.model_dump_json(indent=2))
        except ValidationError as e:
            ic(e)


if __name__ == "__main__":
    ic()
    asyncio.run(main())
