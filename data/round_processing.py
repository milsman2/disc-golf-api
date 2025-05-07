"""
Calculates round points based on position_raw for each division in a CSV file.
"""

import pandas as pd
from icecream import ic
from pathlib import Path


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

    return df.groupby("division", group_keys=False).apply(
        calculate_points, include_groups=False
    )


def import_and_process_csv(file_path):
    """
    Import a CSV file, assign points for each division, and print its contents.
    :param file_path: Path to the CSV file.
    """
    ic(f"Processing file: {file_path}")
    try:
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)

        df = pd.read_csv(file_path)
        selected_columns = df[["division", "position_raw", "name"]].copy()
        selected_columns.loc[:, "position_raw"] = pd.to_numeric(
            selected_columns["position_raw"], errors="coerce"
        )
        selected_columns = assign_round_points(selected_columns)
        ic(selected_columns)
    except FileNotFoundError as e:
        ic(e)
    except pd.errors.EmptyDataError as e:
        ic(e)
    except KeyError as e:
        ic(e)


def process_all_csv_files(folder_path):
    """
    Loop through all .csv files in the specified folder and process them.
    :param folder_path: Path to the folder containing CSV files.
    """
    ic(f"Looking for CSV files in folder: {folder_path}")
    csv_files = Path(folder_path).glob("*.csv")
    for csv_file in csv_files:
        import_and_process_csv(csv_file)


if __name__ == "__main__":
    process_all_csv_files("data/event_results")
