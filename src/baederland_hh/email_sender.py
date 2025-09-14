from typing import List
import smtplib
from email.message import EmailMessage

from src.baederland_hh.utils import getJson


def make_body(courses: list) -> str:
    """
    Function to create a formatted body for the email
    :param courses: List of dictionaries representing swimming classes
    :return: Formatted string
    :param courses:
    :return: string
    """
    return "\n".join(
        [
            f"{course['course_name']} Kurs vom {course['date_range']}, am Wochentag {course['weekdays']} mit {course['free_spots']} freien Plätzen für {course['price']}"
            for course in courses
        ]
    )


def send_email(
    subject: str, body: list, recipient: List[str], credentials_path: str, base_url: str
) -> None:
    """
    Function to send an email notification
    :param subject: Subject of the email
    :param body: Body of the email
    :param recipient: Email address of the recipient
    :param credentials_path: Path to JSON file containing SMTP credentials
    :param base_url: Base URL of the website
    :return: None
    """
    credentials = getJson(credentials_path)
    server = smtplib.SMTP_SSL(credentials.get("host"), credentials.get("port"))

    for rec in recipient:
        email_body = make_body(body)
        email_body += f"\n\nWeitere Infos: {base_url}"
        msg = EmailMessage()
        msg.set_content(email_body)

        msg["Subject"] = subject
        msg["From"] = credentials.get("from")
        msg["To"] = rec

        server.login(credentials.get("from"), credentials.get("password"))
        server.send_message(msg)

    server.quit()
