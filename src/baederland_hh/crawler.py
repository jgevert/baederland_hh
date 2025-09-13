import asyncio
import aiohttp

from src.baederland_hh.utils import (
    getCurrentDate,
    getSwimmingPoolURL,
    filterCourses
)
from src.baederland_hh.constants import SWIMMING_POOLS
from src.baederland_hh.parser import parse_swimming_classes, extract_class_info

class BaederlandCrawler:
    def __init__(self, base_url):
        self.base_url = base_url

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
            print(available_courses)

    def run(self):
        asyncio.run(self.crawl())

if __name__ == "__main__":
    current_date = getCurrentDate()
    course_name = "Silber"
    swimming_pool = "Parkbad"
    weekdays = ["Monatag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    url = getSwimmingPoolURL(swimming_pool, SWIMMING_POOLS)
    crawler = BaederlandCrawler(url)
    crawler.run()