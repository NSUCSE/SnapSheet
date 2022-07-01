from __future__ import print_function
from errno import EROFS

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def update_value(spreadsheet_id, range_name,value):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
        """
    creds,_ = google.auth.load_credentials_from_file("keys.json",scopes=SCOPES)
    value_input_option = "USER_ENTERED"
    # pylint: disable=maybe-no-member
    service = build('sheets', 'v4', credentials=creds)
    values = [
        [
            value
        ],
        # Additional rows ...
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print(f"{result.get('updatedCells')} cells updated.")
    return result

# if __name__ == '__main__':
#     # Pass: spreadsheet_id,  range_name, value_input_option and  _values
#     print(update_value("1YW-xAqLd4Bc-ImFkCql81ZsA4Zp6xKHOM3Y9uedDv6E",
#                   "B1:B1",'X'))