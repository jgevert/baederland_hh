import os
import json
from datetime import date, timedelta


def getCurrentDate(days_ahead: int = 2) -> date:
    """
    Function to return current datetime object plus x days ahead
    :param days_ahead: integer for current date plus
    :return: datetime
    """
    return date.today() + timedelta(days_ahead)


def getSwimmingPoolURL(swimming_pool: str, translation_dict: dict) -> str:
    """
    Function to construct URL for swimming pool booking
    :param swimming_pool: Swimming pool name
    :param translation_dict: dictionary mapping swimming pool names to IDs
    :return:
    """
    return f"https://www.baederland-shop.de/schwimmschule?standort={translation_dict[swimming_pool]}"


def filterCourses(courses: list, course_name: str, weekdays: list) -> list:
    """
    Function to filter courses based on course name and weekdays
    :param courses: list of dictionaries representing swimming classes
    :param course_name: name of the swimming course
    :param weekdays: list of weekdays
    :return: list of matching courses
    """
    return [course for course in courses if course["course_name"] == course_name]


def getJson(file: str) -> dict:
    """
    Function to load JSON data from a file
    :param file: file path
    :return: dictionary
    """
    with open(file, "r") as f:
        return json.load(f)


def getControls() -> dict:
    """
    Function to load control data from JSON file
    :return: dictionary with user input
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(
            current_dir, "..", "..", "steering", "controls.json"
        )
    with open(file, "r") as f:
        return json.load(f)
