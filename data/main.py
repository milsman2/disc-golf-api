"""
Run all data processing tasks for the Disc Golf API.
"""

from icecream import ic

from data.course_processing import create_courses
from data.disc_event_processing import create_disc_event
from data.round_processing import create_event_rounds


def main():
    """
    Main function to run all data processing tasks.
    """
    ic()
    create_courses()
    create_disc_event()
    create_event_rounds()


if __name__ == "__main__":
    ic()
    main()
