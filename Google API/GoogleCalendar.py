#!/usr/bin/python
from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import time
import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client import tools
import datetime

def main():
    # Set up a Flow object to be used if we need to authenticate. This
    # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
    # the information it needs to authenticate. Note that it is called
    # the Web Server Flow, but it can also handle the flow for native
    # applications
    
    # The client_id and client_secret can be found in Google Developers Console
    FLOW = OAuth2WebServerFlow(
        client_id='517930609909-qdvlcq14eq3focjou5qbu4vlhq71vrpm.apps.googleusercontent.com',
        client_secret='uVchRNDcicKAMRXhsLJQPdoE', # This can be set to a null string.
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri='http://raspberrypi.example.com:80/cgi-bin/test.pl',
        user_agent='GCal.py/0.0.1a')
    
    # To disable the local server feature, uncomment the following line:
    #FLAGS.auth_local_webserver = False
    
    # If the Credentials don't exist or are invalid, run through the native client
    # flow. The Storage object will ensure that if successful the good
    # Credentials will get written back to a file.
    storage = Storage('calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
      credentials = tools.run_flow(FLOW, storage)
    
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    # Build a service object for interacting with the API. Visit
    # the Google Developers Console
    # to get a developerKey for your own application.
    service = build(serviceName='calendar', version='v3', http=http,
           developerKey='')
    #
    
    calendar = service.calendars().get(calendarId='primary').execute()

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Getting the upcoming 5 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    while True:
        time.sleep(5)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        eventsResult1 = service.events().list(
            calendarId='primary', timeMin=now, maxResults=5, singleEvents=True,
            orderBy='startTime').execute()
        events1 = eventsResult1.get('items', [])
        if events1 != events:
            print('New events updated')
            for event in events1:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
            events = events1

if __name__ == '__main__':
    main()
