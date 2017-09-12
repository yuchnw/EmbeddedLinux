#!/usr/bin/env python3
import curses
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

while True:
	ori=screen.getch()
	if ori == ord('w'):
		if y>0:
			y=y-1
			screen.addch(y,x,'x')
	elif ori == ord('s'):
		if y<height:
			y=y+1
			screen.addch(y,x,'x')
	elif ori == ord('a'):
		if x>0:
			x=x-1
			screen.addch(y,x,'x')
	elif ori == ord('d'):
		if x<width:
			x=x+1
			screen.addch(y,x,'x')
	elif ori == ord('c'):
		x=0
		y=0
		screen.clear()
	elif ori == ord('q'):
		break

curses.endwin()
