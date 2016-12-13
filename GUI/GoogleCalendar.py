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
import time

class Events:
    def __init__(self):
        # Set up a Flow object to be used if we need to authenticate. This
        # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
        # the information it needs to authenticate. Note that it is called
        # the Web Server Flow, but it can also handle the flow for native
        # applications
        
        # The client_id and client_secret can be found in Google Developers Console
        self.FLOW = OAuth2WebServerFlow(
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
        self.storage = Storage('calendar.dat')
        self.credentials = self.storage.get()
        if self.credentials is None or self.credentials.invalid == True:
          self.credentials = tools.run_flow(self.FLOW, self.storage)
        
        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with our good Credentials.
        self.http = httplib2.Http()
        self.http = self.credentials.authorize(self.http)
        
        # Build a service object for interacting with the API. Visit
        # the Google Developers Console
        # to get a developerKey for your own application.
        self.service = build(serviceName='calendar', version='v3', http=self.http,
               developerKey='')
        #
        
        self.calendar = self.service.calendars().get(calendarId='primary').execute()
        self.check_time = time.time()

        
    ''' Returns the next n events in the attached google calendar. N is 5 default.
    Events are returned as a list of (datetime object, 'Event Name').'''
    def getEvents(self, max_results=5):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        eventsResult = self.service.events().list(
            calendarId='primary', timeMin=now, maxResults=max_results, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
    
        self.check_time = time.time()

        if not events:
            return None
        event_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            #                                 2016-12-14T14:00:00-05:00
            if len(start) > 10:
                start = datetime.datetime.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
            else:
                start = datetime.datetime.strptime(start, "%Y-%m-%d")

            if start.time():
                start = start.strftime('%a, %b %d, %Y at %I:%M%p')
            else:
                start = start.strftime('%a, %b %d, %Y')
            event_list.append([start, event['summary']])
        return event_list

    def getTime(self):
        return self.check_time