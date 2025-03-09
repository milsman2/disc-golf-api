"""
Scrape UDisc for a list of disc golf courses.
"""

import asyncio
from icecream import ic
from scraping.schemas import generated_url
from scraping.fetch_course_pages import get_course_list
from scraping.fetch_course_details import get_course_details


async def main():
    ic()
    courses_list = await get_course_list(url=generated_url)
    course_details = await get_course_details(courses_list)
    ic(course_details)


if __name__ == "__main__":
    ic()
    asyncio.run(main())
