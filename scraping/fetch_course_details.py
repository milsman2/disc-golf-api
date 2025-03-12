"""
Fetch course details from UDisc
"""

from icecream import ic
from playwright.async_api import async_playwright, Browser
import asyncio


async def parse_course_details(browser: Browser, course_link):
    ic()
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(f"https://udisc.com{course_link}")
    await asyncio.sleep(5)

    name_element = await page.query_selector(
        "div.border-divider.mx-3.space-y-2.border-b.pb-4.md\\:mx-0 h1"
    )
    course_name = await name_element.inner_text() if name_element else None
    ic(course_name)

    location_element = await page.query_selector(
        "span.my-auto.whitespace-nowrap.pr-4.text-sm.md\\:text-base"
    )
    location = await location_element.inner_text() if location_element else None

    reviews_link_element = await page.query_selector(f"a[href='{course_link}/reviews']")
    rating = None
    reviews_count = None
    if reviews_link_element:
        rating_element = await reviews_link_element.query_selector("div")
        rating = await rating_element.inner_text() if rating_element else None
        reviews_element = await reviews_link_element.query_selector("span")
        reviews_text = await reviews_element.inner_text() if reviews_element else None
        reviews_count = (
            int("".join(filter(str.isdigit, reviews_text))) if reviews_text else None
        )

    await page.close()
    await context.close()
    return {
        "name": course_name,
        "location": location,
        "rating": rating,
        "reviews_count": reviews_count,
    }


async def get_course_details(courses):
    ic()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = [parse_course_details(browser, course) for course in courses]
        course_details = await asyncio.gather(*tasks)
        await browser.close()
    return course_details
