from __future__ import print_function
import re
import datetime
import pickle
import os.path
import math
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


WORK_START = datetime.datetime.strptime("08:00:00", "%H:%M:%S").time()
WORK_END = datetime.datetime.strptime("17:00:00", "%H:%M:%S").time()
SCOPES = ['https://www.googleapis.com/auth/calendar']
robots = {
    'VS': 'osaro.com_3138373730323034343235@resource.calendar.google.com',
    'LR-MATE': 'osaro.com_3438343531333034393639@resource.calendar.google.com',
    'M-20': 'osaro.com_32373736333937323031@resource.calendar.google.com',
    'IIWA': 'osaro.com_32323831353732373733@resource.calendar.google.com',
    'KR10': 'osaro.com_3137363632333931383736@resource.calendar.google.com',
    'UR10': 'osaro.com_383639353138393738@resource.calendar.google.com',
    'YASK': 'osaro.com_1887m7gjkdtjkiaoj5c7kc6rrtcg06gb6or3ie1i6gqj8d1p6s@resource.calendar.google.com',
    'KWSK': 'osaro.com_3637383431393334343032@resource.calendar.google.com',
    'IRB': 'osaro.com_3234333336343235363734@resource.calendar.google.com'
}

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


def get_start(event):
    return event['start'].get('dateTime', event['start'].get('date'))


def get_end(event):
    return event['end'].get('dateTime', event['end'].get('date'))


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


def get_events(max_results):
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    colors = service.colors().get(fields='event').execute()
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=max_results,
                                          singleEvents=True, orderBy='startTime').execute() #chng to timeMin=sprint start and timeMax=sprint end
    events = events_result.get('items', [])
    return events, colors


def get_freebusy(robot_id): #params: robot, start, end
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
    time_min = datetime.datetime(2019, 12, 18).isoformat() + 'Z'
    time_max = datetime.datetime(2019, 12, 20).isoformat() + 'Z'
    body= {
        "timeMin": time_min,
        "timeMax": time_max,
        "timeZone": 'US/Central',
        "items": [
            {
                #"id": 'primary'
                "id": robots[robot_id]
            }
        ]
    }

    events_result = service.freebusy().query(body=body).execute()
    calendar = events_result[u'calendars']
    booked = calendar[robots[robot_id]]['busy']
    if booked:
        for event in booked:
            print("{} is booked {} until {}".format(robot_id, event['start'], event['end']))


def next_available(booked_event):

    return #next available event aka whetever is in between event 1 and event 2


def book_robot():
    pass

def main():
    '''Input: start date, end date, robot'''
    get_freebusy('M-20')
    #datetime.datetime(2019, 12, 18)
    #get_events(1)

main()