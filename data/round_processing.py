"""
Calculates round points based on position_raw for each division in a CSV file.
"""

import pandas as pd
from icecream import ic


def assign_round_points(df):
    """
    Assign points based on position_raw for each division. Handles ties by averaging points.
    :param df: DataFrame containing 'division' and 'position_raw' columns.
    :return: DataFrame with the 'round_points' column updated.
    """
    max_points = 30

    def calculate_points(group):
        group = group.sort_values(by="position_raw").reset_index(drop=True)
        points = []
        i = 0
        while i < len(group):
            tied_positions = group[
                group["position_raw"] == group.loc[i, "position_raw"]
            ].index
            num_tied = len(tied_positions)
            if num_tied > 1:
                # Calculate average points for tied positions
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


def import_and_print_csv(file_path):
    """
    Import a CSV file, assign points for each division, and print its contents.
    :param file_path: Path to the CSV file.
    """
    ic()
    try:
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)

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
        print(f"Error: One or more specified columns are missing in the CSV file. {e}")


if __name__ == "__main__":
    import_and_print_csv("data/event_results/tc-jester-hfds-league-2025-03-12.csv")
