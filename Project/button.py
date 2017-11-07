#!/usr/bin/env python
import subprocess
import twilio
from twilio.rest import Client
import logging
import bluetooth
import evdev
import time

#Setup Twilio Account
ACCOUNT_SID = "AC95d29203d467ad68fcbb249d36c65f53"
AUTH_TOKEN = "5a30c5bb9ea30835b72d1e5dfd22158d"

def connect():
    cmd = ['./connect.sh']
    subprocess.call(cmd)
    time.sleep(5)
    try:
        dev = evdev.InputDevice('/dev/input/event1')
        print("Connected..")
        return dev
    except OSError:
        logging.error("No bluetooth device found. Exiting the program")
    raise

connected = False
flag=0

while True:
     try:
        # first connection try
        if not connected:
           device = connect()
           connected = True
        if connected:
           for event in device.read_loop():
           # 28 is the event code for Android button
               if event.code == 28 and event.value == 1:
                  client = Client(ACCOUNT_SID,AUTH_TOKEN)
                  client.messages.create(to="+18128783295",from_="+18126457346",body="This is Yuchen! Emergency Situation! Need help!",)
                  print("Emergency sent.")
     except (OSError, IOError):
            # try connecting last time
            # if failed then exit the program
            # if connected then continue the inner for loop
            device = connect()
            connected = True
