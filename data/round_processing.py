"""
Calculates round points based on position_raw for each division in a CSV file
and posts event results to an API endpoint.
"""

import datetime
import math
import re
from pathlib import Path

import httpx
import pandas as pd
from icecream import ic
from pydantic import ValidationError

from src.schemas.event_results import EventResultCreate


def assign_points(df: pd.DataFrame) -> pd.DataFrame:
    """Assigns points based on position_raw for each division in the DataFrame.
    :param df: DataFrame containing event results.
    :return: DataFrame with assigned points.
    """
    ic()
    points_dict = {}
    keys = range(1, 31)
    for key in keys:
        most_points_plus = 31
        points_dict[key] = most_points_plus - key
    df2 = (
        df.groupby(["division", "position_raw"])["name"]
        .nunique()
        .reset_index()
        .rename(columns={"name": "players"})
    )
    df2["points_value"] = df2["position_raw"].map(points_dict)
    df2["adjusted_points"] = (
        df2["points_value"] + (df2["points_value"] + 1) - (df2["players"])
    ) / 2
    df3 = pd.merge(df, df2, on=["position_raw", "division"], how="left")
    ic(df3)
    return df3


def post_event_result(event_result: dict):
    """
    Post an event result to the API endpoint.
    :param event_result: Dictionary containing event result data.
    """
    api_url = "http://localhost:8000/api/v1/event-results/"
    ic(f"Posting event result to {api_url}: {event_result}")
    try:
        with httpx.Client() as client:
            response = client.post(api_url, json=event_result)
            response.raise_for_status()
            ic(f"Successfully posted event result: {response.json()}")
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
        df = pd.read_csv(file_path)
        df = assign_points(df)
        df.insert(0, "date", date_val)
        df = df.loc[:, ~df.columns.str.startswith("hole_")]
        df = df.replace([float("inf"), -float("inf")], pd.NA)
        df = df.where(pd.notnull(df), None)
        df.loc[:, "position_raw"] = pd.to_numeric(
            df["position_raw"],
            errors="coerce",
            downcast="float",
        )
        for _, row in df.iterrows():
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
                "event_session_id": 1,
            }
            try:
                EventResultCreate(**event_result)
            except ValidationError as e:
                ic(e)
            post_event_result(event_result)
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


if __name__ == "__main__":
    process_all_csv_files("data/event_sessions")
