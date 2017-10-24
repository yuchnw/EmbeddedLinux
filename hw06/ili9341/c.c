/*
To test that the Linux framebuffer is set up correctly, and that the device permissions
are correct, use the program below which opens the frame buffer and draws a gradient-
filled red square:

retrieved from:
Testing the Linux Framebuffer for Qtopia Core (qt4-x11-4.2.2)

http://cep.xor.aps.anl.gov/software/qt4-x11-4.2.2/qtopiacore-testingframebuffer.html
*/

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <sys/mman.h>
#include <sys/ioctl.h>

#include "/opt/source/Robotics_Cape_Installer/libraries/rc_usefulincludes.h"
#include "/opt/source/Robotics_Cape_Installer/libraries/roboticscape.h"

int main()
{
    int fbfd = 0;
    struct fb_var_screeninfo vinfo;
    struct fb_fix_screeninfo finfo;
    long int screensize = 0;
    char *fbp = 0;
    int x = 0, y = 1;       // Make it so the it runs before the encoder is moved
    int xold = 0, yold = 0;
    long int location = 0;
    long int l1=0;
    long int l2=0;
    int r;
    int g;
    int b;
    char wid[10];
    char Color;
   
    printf("Welcome to Etch-A-Sketch! Please select a color: \n Blue->b Red->r Green ->g \n");
    Color=getchar();
    if(Color=='r'){
       r=14;
       g=0;
       b=0;
    }
    if(Color=='g'){
       r=0;
       g=14;
       b=0;
    }
    if(Color=='b'){
       r=0;
       g=0;
       b=14;
    }
    
    printf("PLease enter the width of the line: /n");
    scanf("%s", &wid);
    int w=atol(wid);
    if(w>20||w<1){
       printf("Index Out Of Bound!");
    }
    //printf("w: %d\n", w);

    // Open the file for reading and writing
    fbfd = open("/dev/fb0", O_RDWR);
    if (fbfd == -1) {
        perror("Error: cannot open framebuffer device");
        exit(1);
    }
    printf("The framebuffer device was opened successfully.\n");

    // Get fixed screen information
    if (ioctl(fbfd, FBIOGET_FSCREENINFO, &finfo) == -1) {
        perror("Error reading fixed information");
        exit(2);
    }
    // Get variable screen information
    if (ioctl(fbfd, FBIOGET_VSCREENINFO, &vinfo) == -1) {
        perror("Error reading variable information");
        exit(3);
    }

    printf("%dx%d, %dbpp\n", vinfo.xres, vinfo.yres, vinfo.bits_per_pixel);
    printf("Offset: %dx%d, line_length: %d\n", vinfo.xoffset, vinfo.yoffset, finfo.line_length);
    
    if (vinfo.bits_per_pixel != 16) {
        printf("Can't handle %d bpp, can only do 16.\n", vinfo.bits_per_pixel);
        exit(5);
    }

    // Figure out the size of the screen in bytes
    screensize = vinfo.xres * vinfo.yres * vinfo.bits_per_pixel / 8;

    // Map the device to memory
    fbp = (char *)mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fbfd, 0);
    if ((int)fbp == -1) {
        perror("Error: failed to map framebuffer device to memory");
        exit(4);
    }
    printf("The framebuffer device was mapped to memory successfully.\n");

    // initialize hardware first
        if(rc_initialize()){
                fprintf(stderr,"ERROR: failed to run rc_initialize(), are you root?\n");
                return -1;
        }

        printf("\nRaw encoder positions\n");
        printf("   E1   |");
        printf("   E2   |");
        printf("   E3   |");
        printf("   E4   |");
        printf(" \n");

        // Black out the screen
        short color = (0<<11) | (0 << 5) | 8;  // RGB
        for(int i=0; i<screensize; i+=2) {
            fbp[i  ] = color;      // Lower 8 bits
            fbp[i+1] = color>>8;   // Upper 8 bits
        }

        while(rc_get_state() != EXITING) {
	printf("\r");
	for(int i=1; i<=4; i++){
	printf("%6d |", rc_get_encoder_pos(i));
	}
	fflush(stdout);
	// Update framebuffer
	// Figure out where in memory to put the pixel
	x = (rc_get_encoder_pos(1)/2 + vinfo.xres) % vinfo.xres;
	y = (rc_get_encoder_pos(3)/2 + vinfo.yres) % vinfo.yres;

        if((x != xold) || (y != yold)) {
            location = (xold+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (yold+vinfo.yoffset) * finfo.line_length;
            printf("Updating location to %d, %d (%d)\n", x, y, location);
            unsigned short int t = r<<11 | g << 5 | b;
            *((unsigned short int*)(fbp + location)) = t;
            // Set old location to green
            for(int i=0;i<w;i++){
                if(x!=xold){
                   l1 = (xold+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (yold+i+vinfo.yoffset) * finfo.line_length;
                   //printf("l1: %d\n", l1);
                   *((unsigned short int*)(fbp + l1)) = t;
                }
                if(y!=yold){
                   l2 = (xold+vinfo.xoffset+i) * (vinfo.bits_per_pixel/8) + (yold+vinfo.yoffset) * finfo.line_length;
                   //printf("l2: %d\n", l2);
                   *((unsigned short int*)(fbp + l2)) = t;
                }
            }
        location = (x+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (y+vinfo.yoffset) * finfo.line_length;
        //printf("Updating location to %d, %d, %d\n", x, y, location);
        *((unsigned short int*)(fbp + location)) = 0xff;
        }
        rc_usleep(5000);
        }

        rc_cleanup();
    
    munmap(fbp, screensize);
    close(fbfd);
    return 0;
}
