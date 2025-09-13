from bs4 import BeautifulSoup
from typing import List, Dict


def parse_swimming_classes(html) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('div', class_='teaser')


def extract_class_info(class_elements) -> List[dict]:
    return_list = []

    for class_element in class_elements:
        course_name = class_element.find('h4', class_='mb-3').text.strip()

        info_list = class_element.find('ul', class_='info')

        free_spots = info_list.find('li', class_='freie-plaetze').text.strip().split()[0]

        date_info = info_list.find('li', class_='datum')
        date_range = date_info.contents[0].strip()
        weekdays = date_info.find('div').text.strip().replace('Wochentag: ', '')

        time = info_list.find('li', class_='termin').text.strip()
        location = info_list.find('li', class_='standort').text.strip()
        price = info_list.find('li', class_='euro').contents[0].strip()

        return_list.append(
            {
                'course_name': course_name,
                'free_spots': free_spots,
                'date_range': date_range,
                'weekdays': weekdays,
                'time': time,
                'location': location,
                'price': price
            }
        )
    return return_list
