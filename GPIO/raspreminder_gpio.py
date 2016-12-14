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
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client import tools
import datetime
from dateutil import tz
import picamera
from threading import Thread
import pygame

def remind():
    pygame.mixer.init()
    pygame.mixer.music.load("24k.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    return

def uploadGD():
    FLOW = OAuth2WebServerFlow(
        client_id='517930609909-qdvlcq14eq3focjou5qbu4vlhq71vrpm.apps.googleusercontent.com',
        client_secret='uVchRNDcicKAMRXhsLJQPdoE', # This can be set to a null string.
       scope='https://www.googleapis.com/auth/drive',
        redirect_uri='http://raspberrypi.example.com:80/cgi-bin/test.pl',
        user_agent='GCal.py/0.0.1a')

    storage = Storage('drive.dat')

    credentials = storage.get()

    if credentials is None or credentials.invalid == True:
        credentials = tools.run_flow(FLOW, storage)

    http = httplib2.Http()

    http = credentials.authorize(http)

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.datetime.utcnow()
    utc = utc.replace(tzinfo=from_zone)
    now = utc.astimezone(to_zone)
    now = now.strftime('%m/%d/%Y %H:%M:%S %Z')
    
    drive = build(serviceName = 'drive', version = 'v3', http = http,
            developerKey = '')

    file_metadata = {
        'name' : now,
        'mimeType' : 'application/vnd.google-apps.folder'
        }
    file = drive.files().create(body=file_metadata,fields = 'id').execute()
    print('folderid: %s' %file.get('id'))

    folder_id = file.get('id')
    file_metadata1 = {
        'name': 'image.jpg',
        'parents' :[folder_id]
    }
    media = MediaFileUpload('./image.jpg',
                            mimetype = 'image/jpeg',
                            resumable = True)
    file1 = drive.files().create(body = file_metadata1,
                                media_body = media,
                                fields = 'id').execute()
    print('FileID: %s' % file1.get('id'))

# Initialize camera and countdown timer
camera = picamera.PiCamera()
camera.resolution = (1640,1232)
countdown = time.time()-10

GPIO.setmode(GPIO.BCM)

# Pins for the sensors
door = 2
human = 3
keys = 4

# Setup pins as inputs
GPIO.setup(door, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)       # Door, 0=door open, 1=door closed
GPIO.setup(human, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)      # Human, 0=no human present, 1=human present
GPIO.setup(keys, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)       # Keys, 0=keys missing, 1=keys present

# Create interupt
GPIO.add_event_detect(door, GPIO.RISING)

# Door callback function, runs whenever the door is opened
def door_callback():
    print("Door was opened at "+datetime.datetime.now().isoformat())
    # Someone is leaving and is forgeting their keys
    if GPIO.input(keys) and GPIO.input(human):
        t = Thread(target=remind)
        t.start()
        return
    # Someone is leaving and the keys are already gone
    elif not GPIO.input(keys) and GPIO.input(human):
        return

    # Door is opening but no is leaving so wait until human is present
    while not GPIO.input(human):
        # check if the door was closed and no one came in
        if GPIO.input(door):
            print("Door was closed at "+datetime.datetime.now().isoformat())
            return
        continue

    print("Human present at "+datetime.datetime.now().isoformat())
    
    # Take picture and upload
    camera.capture('image.jpg')
    print("Picture taken at "+datetime.datetime.now().isoformat())
    t = Thread(target=uploadGD)
    t.start()

# Create callback for door
#GPIO.add_event_callback(door, door_callback)

# Run forever
while True:
    if not GPIO.input(door):
        door_callback()