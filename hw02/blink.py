#!/usr/bin/env python3

import time
import Adafruit_BBIO.GPIO as GPIO

#Define LEDs and BTNs
BTN1="GP0_6"
BTN2="GP0_4"
BTN3="GP0_5"
BTN4="GP0_3"
LED1="GP1_3"
LED2="GP1_4"
LED3="RED"
LED4="GREEN"

#Assign GPIO to inputs and outputs
GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED2,GPIO.OUT)
GPIO.setup(LED3,GPIO.OUT)
GPIO.setup(LED4,GPIO.OUT)

GPIO.setup(BTN1, GPIO.IN)
GPIO.setup(BTN2, GPIO.IN)
GPIO.setup(BTN3, GPIO.IN)
GPIO.setup(BTN4, GPIO.IN)

#Map BTNs to related LEDs
map={BTN1:LED1,BTN2:LED2,BTN3:LED3,BTN4:LED4}

#Update LED
def updateLED(channel):
    state=GPIO.input(channel)
    GPIO.output(map[channel],state)

#Detect button pressed
GPIO.add_event_detect(BTN1,GPIO.BOTH,callback=updateLED)
GPIO.add_event_detect(BTN2,GPIO.BOTH,callback=updateLED)
GPIO.add_event_detect(BTN3,GPIO.BOTH,callback=updateLED)
GPIO.add_event_detect(BTN4,GPIO.BOTH,callback=updateLED)

try:
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    printf("Cleaning Up")
    GPIO.cleanup()
GPIO.cleanup()

