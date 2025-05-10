"""
Calculates round points based on position_raw for each division in a CSV file
and posts event results to an API endpoint.
"""

import pandas as pd
from icecream import ic
from pathlib import Path
import httpx


def assign_round_points(df: pd.DataFrame, max_points: int = 30) -> pd.DataFrame:
    """
    Assign points based on position_raw for each division.
    Handles ties by averaging points.
    :param df: DataFrame containing 'division' and 'position_raw' columns.
    :return: DataFrame with the 'round_points' column updated.
    """
    ic()

    def calculate_points(group: pd.DataFrame) -> pd.DataFrame:
        ic()
        group = group.sort_values(by="position_raw").reset_index(drop=True)
        points = []
        i = 0
        while i < len(group):
            tied_positions = group[
                group["position_raw"] == group.loc[i, "position_raw"]
            ].index
            num_tied = len(tied_positions)
            if num_tied > 1:
                start_points = max_points - i
                end_points = max_points - (i + num_tied - 1)
                avg_points = sum(range(start_points, end_points - 1, -1)) / num_tied
                points.extend([avg_points] * num_tied)
                i += num_tied
            else:
                points.append(max_points - i)
                i += 1
        group["round_points"] = points
        return group

    result = (
        df.groupby("division", group_keys=False)
        .apply(calculate_points)
        .reset_index(drop=True)
    )
    return result


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

        df = pd.read_csv(file_path)

        # Check if required columns exist
        required_columns = {
            "division",
            "position_raw",
            "name",
            "event_relative_score",
            "event_total_score",
            "pdga_number",
            "username",
            "round_relative_score",
            "round_total_score",
        }

        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise KeyError(f"Missing required columns: {missing_columns}")

        selected_columns = df[["division", "position_raw", "name"]].copy()
        selected_columns.loc[:, "position_raw"] = pd.to_numeric(
            selected_columns["position_raw"], errors="coerce"
        )
        selected_columns = assign_round_points(selected_columns)
        ic(selected_columns)

        # Post each row as an event result
        for _, row in selected_columns.iterrows():
            event_result = {
                "division": row["division"],
                "position_raw": row["position_raw"],
                "name": row["name"],
                "event_relative_score": row["event_relative_score"],
                "event_total_score": row["event_total_score"],
                "pdga_number": row["pdga_number"],
                "username": row["username"],
                "round_relative_score": row["round_relative_score"],
                "round_total_score": row["round_total_score"],
                "round_points": row["round_points"],
            }
            post_event_result(event_result)

    except FileNotFoundError as e:
        ic(f"FileNotFoundError: {e}")
    except pd.errors.EmptyDataError as e:
        ic(f"EmptyDataError: {e}")
    except KeyError as e:
        ic(f"KeyError: {e}")
    except ValueError as e:
        ic(f"ValueError: {e}")


def process_all_csv_files(folder_path):
    """
    Loop through all .csv files in the specified folder, process them, and post event results.
    :param folder_path: Path to the folder containing CSV files.
    """
    ic(f"Looking for CSV files in folder: {folder_path}")
    csv_files = Path(folder_path).glob("*.csv")
    for csv_file in csv_files:
        import_and_process_csv(csv_file)


if __name__ == "__main__":
    process_all_csv_files("data/event_results")
