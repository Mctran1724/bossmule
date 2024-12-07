import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def access_google_sheet(google_sheet_url: str, sheet_num: int = 0) -> pd.DataFrame:
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    creds_file = "C:/Users/Micha/Desktop/Projects/personal/maplestory_calculators/bossing_calculator/bossmule/MS_sheets_credentials.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)

    client = gspread.authorize(creds)

    sheet = client.open_by_url(google_sheet_url)
    party_candidates_sheet = sheet.get_worksheet(sheet_num)

    party_candidates_dict = party_candidates_sheet.get_all_records()
    return pd.DataFrame(party_candidates_dict)