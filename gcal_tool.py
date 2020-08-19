# add change comments here
from __future__ import print_function
import re
import datetime
import pickle
import os.path
import math
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Modified from Google Calendar API Quickstart
VALID_DATETIME_FORMATS = ('%Y-%m-%dT%H:%M:%S%f', '%Y-%m-%d')
WORK_START = datetime.datetime.strptime("08:00:00", "%H:%M:%S").time()
WORK_END = datetime.datetime.strptime("17:00:00", "%H:%M:%S").time()
WORKING_HOURS = 9
CENTURY = 21
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_events(max_results):
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    colors = service.colors().get(fields='event').execute()
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=max_results,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events, colors


def get_day_of_week(event_date):
    '''Uses this formula from https://cs.uwaterloo.ca/~alopez-o/math-faq/node73.html to determine day of week from date'''
    '''Monday = 1, Tuesday = 2, etc.'''
    day = event_date.day
    month = event_date.month
    year = event_date.year
    t = [0, 3, 2, 5, 0, 3,
         5, 1, 4, 6, 2, 4]
    year -= month < 3
    return ((year + int(year / 4) - int(year / 100)
             + int(year / 400) + t[month - 1] + day) % 7)


def is_between_working_hrs(time):
    return WORK_START <= time <= WORK_END


def filter_events(events):
    pass


def is_single_day_event(datetime_str):
    regex_obj = re.compile('.*-.*-.*T.*:.*:.*')
    if regex_obj.match(datetime_str):
        return True
    return False


def convert_google_datetime(datetime_str):
    if not is_single_day_event(datetime_str[:datetime_str.rfind("-")]):
        return datetime.datetime.strptime(datetime_str, '%Y-%m-%d')
    else:
        return datetime.datetime.strptime(datetime_str[:datetime_str.rfind("-")], '%Y-%m-%dT%H:%M:%S%f')


def calculate_hours_free(hours_spent):
    '''TODO: determine when robot calendar is booked'''
    return WORKING_HOURS - hours_spent


def get_start(event):
    return event['start'].get('dateTime', event['start'].get('date'))


def get_end(event):
    return event['end'].get('dateTime', event['end'].get('date'))


def calculate_hours_spent(event):
    start = get_start(event)
    end = get_end(event)
    datetime_diff = convert_google_datetime(end) - convert_google_datetime(start)
    return datetime_diff.total_seconds() / 3600


def create_event_color_list(max_results):
    events_list = get_events(max_results)
    events = events_list[0]
    colors = events_list[1]
    event_color_list = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = get_start(event)
        end = get_end(event)
        hours_spent = calculate_hours_spent(event)
        name = event['summary']
        if 'colorId' in event:
            clr = colors['event'][event['colorId']]['background']
        else:
            clr = "None"
        event_color_list.append([name, clr, start, end, hours_spent])
    return event_color_list

def main():
    events_list = get_events(1)[0]
    start = convert_google_datetime(get_start(events_list[0]))
    weekday = get_day_of_week(start)
    print(start.time(), type(start.time()))
    print(is_between_working_hrs(start.time()))

main()
