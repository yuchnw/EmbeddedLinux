#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import time

# Setup BTN and LED
BTN = "GP1_3"
LED = "GP1_4"
GPIO.setup(BTN, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# map button to led
map = {BTN: LED}

def updateLED(channel):
#	print("channel = " + channel)
	state = GPIO.input(channel)
	GPIO.output(map[channel], state)
#        print(map[channel] + " Toggled")

print("Running...")

GPIO.add_event_detect(BTN, GPIO.BOTH, callback=updateLED)

try:
	while True:
		time.sleep(100)
except KeyboardInterrupt:
	print("Cleaning Up")
	GPIO.cleanup()
GPIO.cleanup()
