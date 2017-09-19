#!/usr/bin/env python3

import time
import smbus
import Adafruit_BBIO.GPIO as GPIO

print("Welcome to Etch-A-Sketch!")
print("Here are the instructions:\n");
print("BTN1->up  BTN2->down  BTN3->left  BTN4->right\n");

#Define BTNs
BTN4="GP0_6"
BTN3="GP0_5"
BTN2="GP0_3"
BTN1="GP0_4"

#Assign GPIO to inputs and outputs
GPIO.setup(BTN1, GPIO.IN)
GPIO.setup(BTN2, GPIO.IN)
GPIO.setup(BTN3, GPIO.IN)
GPIO.setup(BTN4, GPIO.IN)

#Setup initials
bus=smbus.SMBus(1)
matrix=0x70
x=0
y=0
bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness
canvas=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
bus.write_i2c_block_data(matrix,0,canvas)

#Map BTNs to related directions
map={BTN1:'d',BTN2:'a',BTN3:'s',BTN4:'w'}

def updateMatrix(channel):
    global x
    global y
    global canvas
    if map[channel]=='a':
        if x>0:
           print("Left")
           x=x-1
           canvas[2*x]=canvas[2*x+1]|canvas[2*x]
           bus.write_i2c_block_data(matrix,0,canvas)
    elif map[channel]=='d':
        if x<8:
           print("Right")
           x=x+1
           canvas[2*x]=canvas[2*x+1]|canvas[2*x]
           bus.write_i2c_block_data(matrix,0,canvas)
    elif map[channel]=='w':
        if y>0:
           print("Up")
           y=y-1
           canvas[2*x]=canvas[2*x+1]|canvas[2*x]
           bus.write_i2c_block_data(matrix,0,canvas)
    elif map[channel]=='s':
        if y<8:
           print("Down")
           y=y+1
           canvas[2*x]=canvas[2*x+1]|canvas[2*x]
           bus.write_i2c_block_data(matrix,0,canvas)

time.sleep(0.1)

#Detect button pressed
GPIO.add_event_detect(BTN1,GPIO.RISING,callback=updateMatrix)
GPIO.add_event_detect(BTN2,GPIO.RISING,callback=updateMatrix)
GPIO.add_event_detect(BTN3,GPIO.RISING,callback=updateMatrix)
GPIO.add_event_detect(BTN4,GPIO.RISING,callback=updateMatrix)

try:
    while True:
          time.sleep(100)
except KeyboardInterrupt:
    print("Cleaning Up")
    GPIO.cleanup()
GPIO.cleanup()

