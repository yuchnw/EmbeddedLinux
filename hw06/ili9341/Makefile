# This is a general use makefile for robotics cape projects written in C.
# Just change the target name to match your main source code filename.

CC		:= gcc
LINKER		:= gcc -o
CFLAGS		:= -Wall -O2
LFLAGS		:= -L /opt/source/Robotics_Cape_Installer/libraries -lm -lrt -lpthread -lroboticscape

etch-a-sketch:	etch-a-sketch.c
	$(CC) $(CFLAGS) $(LFLAGS) $^ -o $@

framebuffer:	framebuffer.c
	$(CC) $(CFLAGS) $^ -o $@

c:	c.c
	$(CC) $(CFLAGS) $(LFLAGS) $^ -o $@
