"""
Scrape UDisc for a list of disc golf courses.
"""

from playwright.sync_api import sync_playwright
import time
from icecream import ic


def scrape_udisc_courses():
    ic()
    url = (
        "https://udisc.com/courses?zoom=10&lat=29.76328&lng=-95.36327&swLat=29.6319106"
        "&swLng=-95.6599009&neLat=29.8944774&neLng=-95.0666391"
    )

    with sync_playwright() as p:
        courses = []
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        time.sleep(5)

        elements_with_class = page.query_selector_all(
            ".divide-divider.border-divider.mt-2.flex-1.flex-col.divide-y.border-y"
        )
        for element in elements_with_class:
            course_links = element.query_selector_all("a[href^='/courses']")
            for course_link in course_links:
                href = course_link.get_attribute("href")
                courses.append(href)
        browser.close()
        return courses


if __name__ == "__main__":
    course_names = scrape_udisc_courses()
    ic(course_names)
