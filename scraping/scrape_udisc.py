"""
Scrape UDisc for a list of disc golf courses.
"""

import asyncio
from icecream import ic
from pydantic import ValidationError
from scraping.schemas import generated_url
from scraping.fetch_course_pages import get_course_list
from scraping.fetch_course_details import get_course_details
from src.schemas import CourseCreate


async def main():
    ic()
    courses_list = await get_course_list(url=generated_url)
    course_details = await get_course_details(courses_list)
    for course in course_details:
        try:
            course_out = CourseCreate(name=course["name"])
            ic(course_out)
        except ValidationError as e:
            ic(e)


if __name__ == "__main__":
    ic()
    asyncio.run(main())
