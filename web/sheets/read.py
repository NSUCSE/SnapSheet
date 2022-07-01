from __future__ import print_function

from Utils.utils import get_sheet_id
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_values(spreadsheet_id, range_name):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
        """
    creds,_ = google.auth.load_credentials_from_file("keys.json",scopes=SCOPES)
    # pylint: disable=maybe-no-member
    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    print(f"{len(rows)} rows retrieved")
    return rows


# if __name__ == '__main__':
#     # Pass: spreadsheet_id, and range_name
#     print(get_values("1YW-xAqLd4Bc-ImFkCql81ZsA4Zp6xKHOM3Y9uedDv6E", "A1:A1"))