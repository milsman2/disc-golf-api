"""
Run all data processing tasks for the Disc Golf API.
"""

from icecream import ic

from data.course_processing import create_courses
from data.event_session_processing import post_event_session
from data.round_processing import process_all_csv_files


def main():
    """
    Main function to run all data processing tasks.
    """
    ic()
    create_courses()
    post_event_session()
    process_all_csv_files("data/event_results")


if __name__ == "__main__":
    ic()
    main()
