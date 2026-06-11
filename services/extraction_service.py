import pandas as pd
import os
import json

from pathlib import Path


# =============================================================
# PATHS
# =============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "Wohlig Active Employee Data.xlsx"
)

OUTPUT_JSON_FILE = (
    BASE_DIR
    / "data"
    / "all_files_extracted_data.json"
)


# =============================================================
# EXTRACTION LOGIC
# =============================================================

def extract_all_excel_data(file_path):
    """
    Extract all sheets from workbook.
    """

    print(
        f"\n[{os.path.basename(file_path)}] Reading file..."
    )

    try:

        all_sheets = pd.read_excel(
            file_path,
            sheet_name=None,
            engine="openpyxl"
        )

        extracted_data = {}

        for sheet_name, df in all_sheets.items():

            df_cleaned = (
                df.dropna(how="all", axis=0)
                  .dropna(how="all", axis=1)
            )

            extracted_data[sheet_name] = df_cleaned

            print(
                f" -> Tab '{sheet_name}': "
                f"Found {len(df_cleaned)} rows."
            )

        return extracted_data

    except Exception as e:

        print(
            f"Error reading workbook: {e}"
        )

        raise


# =============================================================
# MAIN EXTRACTION SERVICE
# =============================================================

def extract_workforce_data():

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"Workbook not found: {INPUT_FILE}"
        )

    master_json_data = {}

    file_data = extract_all_excel_data(
        INPUT_FILE
    )

    if file_data:

        json_ready_file_data = {}

        for sheet_name, df in file_data.items():

            json_ready_file_data[sheet_name] = (
                df.to_dict(orient="records")
            )

        master_json_data[
            INPUT_FILE.name
        ] = json_ready_file_data

    with open(
        OUTPUT_JSON_FILE,
        "w",
        encoding="utf-8"
    ) as json_file:

        json.dump(
            master_json_data,
            json_file,
            indent=4,
            default=str
        )

    print(
        f"\nSuccess! Saved to:"
        f"\n{OUTPUT_JSON_FILE}"
    )

    return OUTPUT_JSON_FILE


# =============================================================
# LOCAL TESTING
# =============================================================

if __name__ == "__main__":

    extract_workforce_data()