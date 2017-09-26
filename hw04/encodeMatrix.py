#!/usr/bin/env python3

import time
import smbus
import Adafruit_BBIO.GPIO as GPIO
import rcpy
import rcpy.encoder as encoder

print("Welcome to Etch-A-Sketch!")
print("Here are the instructions:\n");
print("BTN1->up  BTN2->down  BTN3->left  BTN4->right\n");

rcpy.set_state(rcpy.RUNNING)

#Setup initials
bus=smbus.SMBus(1)
matrix=0x70
x=0
y=0
current2=0
current3=0
bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness
canvas=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
bus.write_i2c_block_data(matrix,0,canvas)

while True:
    time.sleep(0.5)
    e2=encoder.get(2)
    e3=encoder.get(3)
    if e2<current2:
        if x>0:
           print("Right")
           x=x-1
           current2=e2
           canvas[2*x+1]=canvas[2*x+1]|pow(2,y)
           bus.write_i2c_block_data(matrix,0,canvas)
        else:
           print("Out of Bound!")
    elif e2>current2:
        if x<8:
           print("Left")
           x=x+1
           current2=e2
           canvas[2*x+1]=canvas[2*x+1]|pow(2,y)
           bus.write_i2c_block_data(matrix,0,canvas)
        else:
           print("Out of Bound!")
    elif e3<current3:
        if y>0:
           print("Up")
           y=y-1
           current3=e3
           canvas[2*x+1]=canvas[2*x+1]|pow(2,y)
           bus.write_i2c_block_data(matrix,0,canvas)
        else:
           print("Out of Bound!")
    elif e3>current3:
        if y<8:
           print("Down")
           y=y+1
           current3=e3
           canvas[2*x+1]=canvas[2*x+1]|pow(2,y)
           bus.write_i2c_block_data(matrix,0,canvas)
        else:
           print("Out of Bound!")

time.sleep(0.1)

try:
    while True:
          time.sleep(100)
except KeyboardInterrupt:
       pass
