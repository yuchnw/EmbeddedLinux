// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
#ifndef _BEAGLEBONE_GPIO_H_
#define _BEAGLEBONE_GPIO_H_

//#define GPIO1_START_ADDR 0x4804C000
#define GPIO3_START_ADDR 0x481ae000
#define GPIO3_END_ADDR 0x481b0000
#define GPIO3_SIZE (GPIO3_END_ADDR - GPIO3_START_ADDR)

#define GPIO1_START_ADDR 0x4804c000
#define GPIO1_END_ADDR 0x4804e000
#define GPIO1_SIZE (GPIO1_END_ADDR - GPIO1_START_ADDR)

#define GPIO_OE 0x134
#define GPIO_DATAIN 0x138
#define GPIO_SETDATAOUT 0x194
#define GPIO_CLEARDATAOUT 0x190

#define USR2 (1<<23)
#define USR3 (1<<24)
#define GPIO_49  (1<<17)
#define GPIO_113 (1<<17)
#endif
