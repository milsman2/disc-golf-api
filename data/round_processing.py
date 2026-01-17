"""
Calculates round points based on position_raw for each division in a CSV file
and posts event results to an API endpoint. Associates results with disc events.
"""

import datetime
import math
import re
from pathlib import Path

import httpx
import numpy as np
import pandas as pd
from icecream import ic
from pydantic import ValidationError

from src.core.config import settings
from src.schemas.event_results import EventResultCreate


def convert_xlsx_to_csv(folder_path):
    """
    Convert all .xlsx files in the specified folder to .csv files using pandas.
    :param folder_path: Path to the folder containing .xlsx files.
    """
    ic(f"Looking for XLSX files in folder: {folder_path}")
    xlsx_files = Path(folder_path).glob("*.xlsx")
    for xlsx_file in xlsx_files:
        try:
            df = pd.read_excel(xlsx_file)
            csv_file = xlsx_file.with_suffix(".csv")
            df.to_csv(csv_file, index=False)
            ic(f"Converted {xlsx_file} to {csv_file}")
        except (
            pd.errors.EmptyDataError,
            pd.errors.ParserError,
            OSError,
            ValueError,
        ) as e:
            ic(f"Failed to convert {xlsx_file}: {e}")


def get_disc_event_id_for_date(event_date: str) -> int:
    """
    Get the appropriate disc event ID for a given date.
    :param event_date: Date string in ISO format (YYYY-MM-DDTHH:MM:SS)
    :return: Disc event ID or 1 as fallback
    """
    try:
        event_datetime = datetime.datetime.fromisoformat(
            event_date.replace("Z", "+00:00")
        )
        ic(f"Looking for disc event for date: {event_datetime}")

        with httpx.Client(base_url=settings.api_base_url, timeout=30.0) as client:
            ic(f"Fetching disc events from: {settings.api_base_url}/disc-events/")
            response = client.get("/disc-events/")
            response.raise_for_status()
            disc_events = response.json()

            ic(f"Found {len(disc_events)} disc events")
            for event in disc_events:
                start_date = datetime.datetime.fromisoformat(
                    event["start_date"].replace("Z", "+00:00")
                )
                end_date = datetime.datetime.fromisoformat(
                    event["end_date"].replace("Z", "+00:00")
                )

                ic(
                    f'DiscEvent {event["id"]}: '
                    f'{event["name"]} ({start_date} to {end_date})'
                )
                if start_date <= event_datetime <= end_date:
                    ic(f'✓ Date {event_datetime} falls within disc event {event["id"]}')
                    return event["id"]
                else:
                    ic(f'✗ Date {event_datetime} out of disc event {event["id"]} range')

            if disc_events:
                ic(
                    f"No matching disc event found for {event_date}, using first "
                    f'available disc event ID: {disc_events[0]["id"]}'
                )
                return disc_events[0]["id"]

    except httpx.ConnectError as e:
        ic(f"Connection error getting disc events: {e}")
        ic(f"Make sure API is running at: {settings.api_base_url}")
    except httpx.TimeoutException as e:
        ic(f"Timeout error getting disc events: {e}")
    except (httpx.RequestError, httpx.HTTPStatusError, ValueError) as e:
        ic(f"Error getting event session ID for date {event_date}: {e}")

    ic(f"Falling back to event session ID 1 for date {event_date}")
    return 1


def assign_points(df: pd.DataFrame) -> pd.DataFrame:
    """Assigns points based on position_raw for each division in the DataFrame.
    :param df: DataFrame containing event results.
    :return: DataFrame with assigned points.
    """
    ic()
    points_dict = {}
    for key in range(1, 31):
        points_dict[key] = 31 - key
    df_clean = df.copy()
    df_clean["position_raw"] = pd.to_numeric(df_clean["position_raw"], errors="coerce")
    df2 = (
        df_clean.groupby(["division", "position_raw"], as_index=False)
        .agg(players=("name", "nunique"))
        .reset_index()
    )
    df2["points_value"] = df2["position_raw"].map(points_dict).fillna(0)
    df2["adjusted_points"] = (
        df2["points_value"] + (df2["points_value"] + 1) - df2["players"]
    ) / 2
    df3 = pd.merge(
        df_clean,
        df2[["division", "position_raw", "adjusted_points"]],
        on=["position_raw", "division"],
        how="left",
    )
    return df3


def post_event_result(event_result: dict):
    """
    Post an event result to the API endpoint.
    :param event_result: Dictionary containing event result data.
    """

    def clean_nans(obj):
        if isinstance(obj, dict):
            return {k: clean_nans(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_nans(v) for v in obj]
        elif isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return None
            return obj
        else:
            return obj

    cleaned_event_result = clean_nans(event_result)
    ic(f"Posting event result to {settings.api_base_url}/event-results/")
    try:
        with httpx.Client(base_url=settings.api_base_url, timeout=30.0) as client:
            response = client.post("/event-results/", json=cleaned_event_result)
            response.raise_for_status()
            ic(f"Successfully posted event result: {response.json()}")
    except httpx.ConnectError as e:
        ic(f"Connection error posting event result: {e}")
        ic(f"Make sure API is running at: {settings.api_base_url}")
    except httpx.TimeoutException as e:
        ic(f"Timeout error posting event result: {e}")
    except httpx.HTTPStatusError as e:
        ic(f"HTTPStatusError: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        ic(f"RequestError: {e}")


def import_and_process_csv(file_path):
    """
    Import a CSV file, assign points for each division, and post event results.
    :param file_path: Path to the CSV file.
    """
    ic(f"Processing file: {file_path}")
    try:
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        match = re.search(r"(\d{4}-\d{2}-\d{2})", str(file_path))
        if match:
            date_str = match.group(1)
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(hour=18)
            date_val = dt.isoformat()
        else:
            date_val = None
        ic(f"Reading CSV file: {file_path}")
        df = pd.read_csv(file_path)
        ic(f"Loaded {len(df)} rows from CSV")
        ic("Assigning points...")
        df = assign_points(df)
        df.insert(0, "date", date_val)
        df = df.loc[:, ~df.columns.str.startswith("hole_")]
        df = df.replace([float("inf"), -float("inf")], pd.NA)
        df = df.where(pd.notnull(df), np.nan)
        df.loc[:, "position_raw"] = pd.to_numeric(
            df["position_raw"],
            errors="coerce",
            downcast="float",
        )
        ic(f"Processing {len(df)} rows for API posting...")
        disc_event_id = get_disc_event_id_for_date(date_val) if date_val else 1
        for row_index, row in df.iterrows():
            if isinstance(row_index, int) and row_index % 10 == 0:  # Progress indicator
                ic(f"Processing row {row_index + 1}/{len(df)}")
            pdga_number = row.get("pdga_number")
            if isinstance(pdga_number, float) and math.isnan(pdga_number):
                pdga_number = None
            position_raw = row.get("position_raw")
            if position_raw is None or (
                isinstance(position_raw, float) and math.isnan(position_raw)
            ):
                position = ""
                position_raw_clean = None
            else:
                position = str(position_raw)
                position_raw_clean = float(position_raw)
            course_layout_id = 1
            event_result = {
                "date": row.get("date"),
                "division": row.get("division"),
                "position": position,
                "position_raw": position_raw_clean,
                "name": row.get("name"),
                "event_relative_score": row.get("event_relative_score"),
                "event_total_score": row.get("event_total_score"),
                "pdga_number": pdga_number,
                "username": row.get("username"),
                "round_relative_score": row.get("round_relative_score"),
                "round_total_score": row.get("round_total_score"),
                "course_layout_id": course_layout_id,
                "round_points": row.get("adjusted_points", 0.0),
                "disc_event_id": disc_event_id,
            }
            try:
                EventResultCreate(**event_result)
            except ValidationError as e:
                ic(f"Validation error for row {row_index}: {e}")
                continue
            post_event_result(event_result)
        ic(f"Completed processing file: {file_path}")
    except KeyboardInterrupt:
        ic("Processing interrupted by user")
        raise
    except FileNotFoundError as e:
        ic(f"FileNotFoundError: {e}")
    except pd.errors.EmptyDataError as e:
        ic(f"EmptyDataError: {e}")
    except pd.errors.ParserError as e:
        ic(f"ParserError: {e}")
    except ValueError as e:
        ic(f"ValueError: {e}")


def process_all_csv_files(folder_path):
    """
    Loop through all .csv files in the specified folder, process them, and
    post event results.
    :param folder_path: Path to the folder containing CSV files.
    """
    ic(f"Looking for CSV files in folder: {folder_path}")
    csv_files = Path(folder_path).glob("*.csv")
    for csv_file in csv_files:
        import_and_process_csv(csv_file)


def create_event_rounds():
    folder = "data/event_results/"
    convert_xlsx_to_csv(folder)
    process_all_csv_files(folder)


if __name__ == "__main__":
    create_event_rounds()
