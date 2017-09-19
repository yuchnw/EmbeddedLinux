#!/usr/bin/env python3

import Adafruit_BBIO.GPIO as GPIO
import time
import smbus

bus=smbus.SMBus(1)
add1=0x48
add2=0x4a
LED1="RED"
LED2="GREEN"
GPIO.setup("GP1_4",GPIO.IN)
GPIO.setup("GP1_3",GPIO.IN)
GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED2,GPIO.OUT)

map1={"GP1_4":add1,"GP1_3":add2}
map2={"GP1_4":LED1,"GP1_3":LED2}
GPIO.output(LED1,1)
GPIO.output(LED2,1)

bus.write_byte_data(add1,3,0x1b)
bus.write_byte_data(add1,2,0x19)
bus.write_byte_data(add2,3,0x1b)
bus.write_byte_data(add2,2,0x19)

def update(channel):
    state=GPIO.input(channel)
    GPIO.output(map2[channel],state)
    temp=bus.read_byte_data(map1[channel],0)
   # temp2=bus.read_byte_data(add2,0)
    print(temp*9/5+32)
   # print(temp2*9/5+32)

GPIO.add_event_detect("GP1_4",GPIO.BOTH,callback=update)
GPIO.add_event_detect("GP1_3",GPIO.BOTH,callback=update)

try:
   while True:
         time.sleep(100)
except KeyboardInterrupt:
       GPIO.cleanup()
GPIO.cleanup()
