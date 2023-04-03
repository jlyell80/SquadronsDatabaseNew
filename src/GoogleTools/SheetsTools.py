import gspread
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def import_sheet_data(sheet_url, worksheet, column_names):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    client = gspread.authorize(credentials)

    # Open the Google Sheet by URL and select the appropriate worksheet
    sheet = client.open_by_url(sheet_url).worksheet(worksheet)

    # Get all values in the specified columns
    data = sheet.get_all_values()
    header_row = data[0]
    column_indices = [header_row.index(column_name) for column_name in column_names]
    selected_data = [[row[i] for i in column_indices] for row in data[1:]]

    return selected_data
