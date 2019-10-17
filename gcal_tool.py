from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#Modified from Google Calendar API Quickstart

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_events():
    creds = get_creds()

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    colors = service.colors().get(fields = 'event').execute()
    events_result  = service.events().list(calendarId='primary', timeMin=now, maxResults =10,
                                        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', []) 
    return events, colors

def calculate_hours_spent(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    datetime_diff = datetime.datetime.strptime(end[:end.rfind("-")],'%Y-%m-%dT%H:%M:%S%f') - datetime.datetime.strptime(start[:start.rfind("-")],'%Y-%m-%dT%H:%M:%S%f')
    return datetime_diff.seconds / 3600
    

def create_event_color_map():
    events = get_events()[0]
    colors = get_events()[1]
    event_color_map = {}
    if not events:
        print('No upcoming events found.')
    for event in events:
        hours = calculate_hours_spent(event)
        name = event['summary']
        if 'colorId' in event:
            clr = colors['event'][event['colorId']]['background']
        else:
            clr = "None"
        if event_color_map.get(name, -1) == -1:
            event_color_map[name] = [clr, hours]
        else:
            event_color_map[name][1] += hours
    return event_color_map

def main():
    emap = create_event_color_map()
    print(emap)

if __name__ == '__main__':
    main()

