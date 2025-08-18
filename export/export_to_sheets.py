import duckdb
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import os

DUCKDB_PATH = "data/load/sales.duckdb"
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
WORKSHEET_NAME = "Sales"
BQ_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS_PATH")

def export_to_sheets():
    if not SPREADSHEET_ID:
        raise ValueError("❌ Environment variable SPREADSHEET_ID is missing.")
    if not BQ_CREDENTIALS or not os.path.exists(BQ_CREDENTIALS):
        raise ValueError("❌ GOOGLE_CREDENTIALS_PATH is missing or invalid.")

    # Query DuckDB
    con = duckdb.connect(DUCKDB_PATH)
    df = con.execute("SELECT * FROM sales").df()
    con.close()

    # Google Sheets authentication
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(BQ_CREDENTIALS, scope)
    client = gspread.authorize(creds)

    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError(
            f"❌ Spreadsheet with ID {SPREADSHEET_ID} not found. "
            f"Make sure you shared it with your service account email."
        )

    try:
        sheet = spreadsheet.worksheet(WORKSHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows="1000", cols="20")

    sheet.clear()
    set_with_dataframe(sheet, df)

    print(f"✅ Exported {len(df)} rows to Google Sheet: {SPREADSHEET_ID} (tab: {WORKSHEET_NAME})")

if __name__ == "__main__":
    export_to_sheets()
