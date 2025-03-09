"""
Fetch course details from UDisc
"""

from icecream import ic
from playwright.async_api import async_playwright
import asyncio


async def get_course_name(browser, course_link):
    ic()
    page = await browser.new_page()
    await page.goto(f"https://udisc.com{course_link}")
    await asyncio.sleep(5)
    course_element = await page.query_selector(f"a[href='{course_link}']")
    if course_element:
        h1_element = await course_element.query_selector("h1")
        if h1_element:
            course_name = await h1_element.inner_text()
            await page.close()
            return {"name": course_name}
    await page.close()
    return None


async def get_course_details(courses):
    ic()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        course_details = []
        tasks = []
        for course_link in courses:
            task = get_course_name(browser, course_link)
            tasks.append(task)
        course_details = await asyncio.gather(*tasks)

        await browser.close()
        return [detail for detail in course_details if detail is not None]
