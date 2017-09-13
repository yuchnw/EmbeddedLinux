#!/usr/bin/env python3

import time
import curses
import Adafruit_BBIO.GPIO as GPIO

print("Welcome to Etch-A-Sketch!")
print("Here are the instructions:\n");
print("w->up  s->down  a->left  d->right  c->clear  x->exit\n");
height = int(input("Please enter height:"))
width = int(input("Please enter width:"))
x = 0
y =0

screen=curses.initscr()
curses.noecho()
curses.cbreak()
screen.addch(y,x,'x')

#Define BTNs
BTN4="GP0_6"
BTN3="GP0_5"
BTN2="GP0_4"
BTN1="GP0_3"
BTN5="PAUSE"

#Assign GPIO to inputs and outputs
GPIO.setup(BTN1, GPIO.IN)
GPIO.setup(BTN2, GPIO.IN)
GPIO.setup(BTN3, GPIO.IN)
GPIO.setup(BTN4, GPIO.IN)
GPIO.setup(BTN5, GPIO.IN)

#Map BTNs to related LEDs
map={BTN1:'d',BTN2:'a',BTN3:'s',BTN4:'w',BTN5:'c'}

#Update Screen
def updateSketch(channel):
    global x
    global y
    global screen
    if map[channel]=='a':
	if x>0:
	   x=x-1
	   screen.addch(y,x,'x')
	   screen.refresh()
    elif map[channel]=='d':
        if x<width:
	   x=x+1
           screen.addch(y,x,'x')
           screen.refresh()
    elif map[channel]=='w':
        if y>0:
	   y=y-1
	   screen.addch(y,x,'x')
           screen.refresh()
    elif map[channel]=='s':
        if y<height:
	   y=y+1
	   screen.addch(y,x,'x')
           screen.refresh()
    elif map[channel]=='c':
	x=0
	y=0
	screen.clear()
        screen.refresh()

time.sleep(0.1)
#Detect button pressed
GPIO.add_event_detect(BTN1,GPIO.BOTH,callback=updateSketch)
GPIO.add_event_detect(BTN2,GPIO.BOTH,callback=updateSketch)
GPIO.add_event_detect(BTN3,GPIO.BOTH,callback=updateSketch)
GPIO.add_event_detect(BTN4,GPIO.BOTH,callback=updateSketch)
GPIO.add_event_detect(BTN5,GPIO.BOTH,callback=updateSketch)

time.sleep(0.1)

try:
    while True:
          time.sleep(100)
except KeyboardInterrupt:
    print("Cleaning Up")
    GPIO.cleanup()
GPIO.cleanup()


