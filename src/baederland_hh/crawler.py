import asyncio
import os
import json

import aiohttp

from src.baederland_hh.constants import SWIMMING_POOLS
from src.baederland_hh.email_sender import send_email
from src.baederland_hh.parser import extract_class_info, parse_swimming_classes
from src.baederland_hh.utils import filterCourses, getCurrentDate, getSwimmingPoolURL, getControls
from src.baederland_hh.database import Database


class BaederlandCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate to the project root and then to the credentials directory
        self.creds_path = os.path.join(
            current_dir, "..", "..", "credentials", "creds.json"
        )
        self.db_path = os.path.join(current_dir, "..", "..", "database", "courses.db")
        self.list_of_recipients = json.load(open(self.creds_path))["recipients"]

    async def fetch(self, session, url):
        async with session.get(url) as response:
            await asyncio.sleep(5)
            return await response.text()

    async def crawl(self):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, self.base_url)
            found_classes = parse_swimming_classes(html)
            extracted_info = extract_class_info(found_classes)
            available_courses = filterCourses(extracted_info, course_name, weekdays)
            database = Database(self.db_path)
            final_course_list = []
            for course in available_courses:
                result = database.check_course_exists(
                    course_name=course["course_name"],
                    date_range=course["date_range"],
                    weekdays=course["weekdays"],
                )
                if not result:
                    final_course_list.append(course)
                    database.insert_course(
                        course_name=course.get("course_name"),
                        date_range=course.get("date_range"),
                        weekdays=course.get("weekdays"),
                        free_spots=course.get("free_spots"),
                        price=course.get("price"),
                    )
            if len(final_course_list) > 0:
                send_email(
                    subject=f"Available {course_name} classes",
                    body=final_course_list,
                    recipient=self.list_of_recipients,
                    credentials_path=self.creds_path,
                    base_url=self.base_url,
                )

    def run(self):
        asyncio.run(self.crawl())


if __name__ == "__main__":
    controls = getControls()
    current_date = getCurrentDate()
    course_name = controls.get("course_name")
    swimming_pool = controls.get("swimming_pool")
    weekdays = controls.get("weekdays")
    url = getSwimmingPoolURL(swimming_pool, SWIMMING_POOLS)
    crawler = BaederlandCrawler(url)
    crawler.run()
