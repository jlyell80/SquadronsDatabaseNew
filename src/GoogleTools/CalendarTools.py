from datetime import datetime, time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_calendar_events(calendar_id, start_date=None, end_date=None, search_string=None):
    """
    Retrieves a list of calendar events from a Google Calendar.
    :param calendar_id: the ID of the calendar to retrieve events from
    :param start_date: (optional) the start date of the range of events to retrieve (in yyyy-mm-dd format)
    :param end_date: (optional) the end date of the range of events to retrieve (in yyyy-mm-dd format)
    :param search_string: (optional) a string to search for in the event summary or description
    :return: a list of dictionaries containing event details
    """
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

    service = build('calendar', 'v3', credentials=credentials)

    events_result = []
    page_token = None

    while True:
        events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
        events_result.extend(events['items'])
        page_token = events.get('nextPageToken')

        if not page_token:
            break

    event_list = []

    for event in events_result:
        if start_date and datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%SZ').date() < datetime.strptime(start_date, '%Y-%m-%d').date():
            continue
        if end_date and datetime.strptime(event['end']['dateTime'], '%Y-%m-%dT%H:%M:%SZ').date() > datetime.strptime(end_date, '%Y-%m-%d').date():
            continue
        if search_string and search_string not in event['summary'] and search_string not in event.get('description', ''):
            continue

        event_dict = {}
        event_dict['name'] = event['summary']
        if 'dateTime' in event['start']:
            event_dict['date'] = datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%SZ').date()
            event_dict['time'] = datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%SZ').time()
        else:
            event_dict['date'] = datetime.strptime(event['start']['date'], '%Y-%m-%d').date()
            event_dict['time'] = time(0, 0)
        print(event_dict)
        event_list.append(event_dict)

    return event_list
