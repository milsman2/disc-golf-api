"""
Scrape UDisc for a list of disc golf courses.
"""

import asyncio
from playwright.async_api import async_playwright
from icecream import ic


async def scrape_course_details(browser, course_link):
    page = await browser.new_page()
    await page.goto(f"https://udisc.com{course_link}")
    await asyncio.sleep(5)
    course_element = await page.query_selector(f"a[href='{course_link}']")
    if course_element:
        h1_element = await course_element.query_selector("h1")
        if h1_element:
            course_name = await h1_element.inner_text()
            await page.close()
            return {"link": course_link, "name": course_name}
    await page.close()
    return None


async def scrape_udisc_courses():
    ic()
    url = (
        "https://udisc.com/courses?zoom=10&lat=29.76328&lng=-95.36327&swLat=29.6319106"
        "&swLng=-95.6599009&neLat=29.8944774&neLng=-95.0666391"
    )

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

        course_details = []
        tasks = []
        for course_link in courses:
            task = scrape_course_details(browser, course_link)
            tasks.append(task)

        course_details = await asyncio.gather(*tasks)

        await browser.close()
        return [detail for detail in course_details if detail is not None]


async def main():
    course_details_data = await scrape_udisc_courses()
    ic(course_details_data)


if __name__ == "__main__":
    asyncio.run(main())
