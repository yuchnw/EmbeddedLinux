#!/usr/bin/env python
import twilio
from twilio.rest import TwilioRestClient
import time
import Adafruit_BBIO.GPIO as GPIO

#Define and assign BTN
BTN = "GP0_3"
GPIO.setup(BTN,GPIO.IN)

#Setup Twilio Account
ACCOUNT_SID = "AC95d29203d467ad68fcbb249d36c65f53"
AUTH_TOKEN = "5a30c5bb9ea30835b72d1e5dfd22158d"

def sendEmergency():
    client = TwilioRestClient(ACCOUNT_SID,AUTH_TOKEN)
    client.messages.create(to="7066151900",from_="+18128783295",body="Emergency! Need help!",)

time.sleep(0.1)
GPIO.add_event_detect(BTN,GPIO.FALLING,callback=sendEmergency)
time.sleep(0.1)

try:
    while True:
          time.sleep(200)
except KeyboardInterrupt:
    print("Cleaning up")
    GPIO.cleanup()
GPIO.cleanup()
