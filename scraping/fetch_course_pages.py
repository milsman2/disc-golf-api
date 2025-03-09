"""
Fetches the list of courses from UDisc for a given location.
"""

from icecream import ic
from playwright.async_api import async_playwright
import asyncio


async def get_course_list(url: str):
    ic()

    async with async_playwright() as p:
        courses = []
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        await asyncio.sleep(5)

        elements_with_class = await page.query_selector_all(
            ".divide-divider.border-divider.mt-2.flex-1.flex-col.divide-y.border-y"
        )
        for element in elements_with_class:
            course_links = await element.query_selector_all("a[href^='/courses']")
            for course_link in course_links:
                href = await course_link.get_attribute("href")
                courses.append(href)

        await browser.close()
        return courses
