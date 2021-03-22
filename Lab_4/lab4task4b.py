'''
-------------------------------------------------------
Name: Lab 4 Task 4b
-------------------------------------------------------
Learning to use the OLED display driver

Creator:  	Peter YK Cheung and Samanatha Foong
Date:   	27 Feb 2021
Revision: 	1.
-------------------------------------------------------
'''
import pyb						# Pyboard basic  library
from pyb import LED, ADC, Pin	# Use various class libraries in pyb
from oled_938 import OLED_938	# Use OLED display driver

# Create peripheral objects
b_LED = LED(4)					# blue LED
pot = ADC(Pin('X11'))			# 5k ohm potentiometer to ADC input on pin X11

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64,
                   external_vcc=False, i2c_devid=60)
oled.poweron()
oled.init_display()

#  Simple Hello world message
oled.draw_text(0,0,'Hello World!')   # each character is 6x8 pixels

tic = pyb.millis()			# store start time	
while True:
	b_LED.toggle()
	toc = pyb.millis()		# read elapsed time
	oled.draw_text(0,20,'Delay time:{:6.3f}sec'.format((toc-tic)*0.001))
	oled.draw_text(0,40,'POT5K reading:{:5d}'.format(pot.read()))
	tic = pyb.millis()		# start time
	oled.display()
	delay = pyb.rng()%1000  # Generate random number btw 0 and 999
	pyb.delay(delay)		# delay in milliseconds
	
	