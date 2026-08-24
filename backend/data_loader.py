import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EXCEL_FILE = BASE_DIR / "data" / "ParcelPilot_Assessment_Data.xlsx"


def show_sheet(sheet_name):
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)

    print("\n" + "=" * 70)
    print(f"SHEET: {sheet_name.upper()}")
    print("=" * 70)

    print("\nCOLUMNS:")
    for column in df.columns:
        print(f"- {column}")

    print(f"\nTOTAL ROWS: {len(df)}")

    print("\nFIRST 5 RECORDS:")
    print(df.head(5).to_string(index=False))


if __name__ == "__main__":
   show_sheet("tickets")