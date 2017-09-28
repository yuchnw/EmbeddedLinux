#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
#include "beaglebone_gpio.h"

int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
    printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
        keepgoing = 0;
}

int main(int argc, char *argv[]) {
    volatile void *gpio1_addr;
    volatile unsigned int *gpio1_oe_addr;
    volatile unsigned int *gpio1_datain;
    volatile unsigned int *gpio1_setdataout_addr;
    volatile unsigned int *gpio1_cleardataout_addr;

    volatile void *gpio3_addr;
    volatile unsigned int *gpio3_oe_addr;
    volatile unsigned int *gpio3_datain;
    volatile unsigned int *gpio3_setdataout_addr;
    volatile unsigned int *gpio3_cleardataout_addr;

    unsigned int reg;

    // Set the signal callback for Ctrl-C
    signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);

    printf("Mapping %X - %X (size: %X)\n", GPIO1_START_ADDR, GPIO1_END_ADDR,
                                           GPIO1_SIZE);
    printf("Mapping %X - %X (size: %X)\n", GPIO3_START_ADDR, GPIO3_END_ADDR,
                                           GPIO3_SIZE);

    gpio1_addr = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd,
                        GPIO1_START_ADDR);
    gpio3_addr = mmap(0, GPIO3_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd,
                        GPIO3_START_ADDR);

    gpio1_oe_addr           = gpio1_addr + GPIO_OE;
    gpio1_datain            = gpio1_addr + GPIO_DATAIN;
    gpio1_setdataout_addr   = gpio1_addr + GPIO_SETDATAOUT;
    gpio1_cleardataout_addr = gpio1_addr + GPIO_CLEARDATAOUT;
    gpio3_datain            = gpio3_addr + GPIO_DATAIN;
    gpio3_oe_addr           = gpio3_addr + GPIO_OE;
    gpio3_setdataout_addr   = gpio3_addr + GPIO_SETDATAOUT;
    gpio3_cleardataout_addr = gpio3_addr + GPIO_CLEARDATAOUT;

    if(gpio1_addr == MAP_FAILED) {
        printf("Unable to map GPIO1\n");
        exit(1);
    }
    if(gpio3_addr == MAP_FAILED) {
        printf("Unable to map GPIO3\n");
        exit(1);
    }

    while(keepgoing) {
        if(*gpio1_datain & GPIO_49) {
            *gpio1_setdataout_addr= USR2;
            //printf("Left BTN toggled\n");
        } else {
            *gpio1_cleardataout_addr = USR2;
            printf("Left BTN toggled\n");
        }
        if(*gpio3_datain & GPIO_113) {
            *gpio1_setdataout_addr= USR3;
            //printf("Right BTN ON\n");
        } else {
            *gpio1_cleardataout_addr = USR3;
            printf("Right BTN toggled\n");
        }

        usleep(100000);
    }

    munmap((void *)gpio1_addr, GPIO1_SIZE);
    munmap((void *)gpio3_addr, GPIO3_SIZE);
    
    close(fd);
    return 0;
}
