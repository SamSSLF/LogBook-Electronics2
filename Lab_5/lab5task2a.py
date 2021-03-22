'''    Marks the start of comment section
-------------------------------------------------------
Name: Lab 4 Exercise 3a - Detect speed of motor by polling
Creator:  Peter YK Cheung
Date:   28 Feb 2016
Revision:  1.0
-------------------------------------------------------
'''

import pyb
from pyb import Pin, Timer, ADC
from oled_938 import OLED_938	# Use OLED display driver

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP)		# Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP)
PWMA = Pin('X1')				# Control speed of motor A
B1 = Pin('X7', Pin.OUT_PP)		# Control direction of motor B
B2 = Pin('X8', Pin.OUT_PP)
PWMB = Pin('X2')				# Control speed of motor B

# Configure timer 2 to produce 1KHz clock for PWM control
tim = Timer(2, freq = 1000)
motorA = tim.channel (1, Timer.PWM, pin = PWMA)
motorB = tim.channel (2, Timer.PWM, pin = PWMB)

# Define 5k Potentiometer
pot = pyb.ADC(Pin('X11'))

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64,
                   external_vcc=False, i2c_devid=60)
oled.poweron()
oled.init_display()
oled.draw_text(0,0, 'Lab 5 - Exercise 3a')
oled.display()

# Define pins for motor speed sensors
A_sense = Pin('Y4', Pin.PULL_NONE)	#  Pin.PULL_NONE = leave this as input pin
B_sense = Pin('Y6', Pin.PULL_NONE)

def A_forward(value):
	A1.low()
	A2.high()
	motorA.pulse_width_percent(value)

def A_back(value):
	A2.low()
	A1.high()
	motorA.pulse_width_percent(value)
	
def A_stop():
	A1.high()
	A2.high()
	
def B_forward(value):
	B2.low()
	B1.high()
	motorB.pulse_width_percent(value)

def B_back(value):
	B1.low()
	B2.high()
	motorB.pulse_width_percent(value)
	
def B_stop():
	B1.high()
	B2.high()
	
# Initialise variables
DEADZONE = 5
speed = 0
A_state = 0
A_speed = 0
A_count = 0
tic = pyb.millis();

while True:				# loop forever until CTRL-C
	# detect rising edge on sensor A
	if (A_state == 0) and (A_sense.value()==1):	# rising edge detected on A
		A_count += 1
	A_state = A_sense.value()
	
	# Check to see if 100 msec has elapsed
	toc = pyb.millis()
	if ((toc-tic) >= 100):
		A_speed = A_count
		
		# drive motor - controlled by potentiometer
		speed = int((pot.read()-2048)*200/4096)
		if (speed >= DEADZONE):		# forward
			A_forward(speed)
			B_forward(speed)
		elif (speed <= -DEADZONE):
			A_back(abs(speed))
			B_back(abs(speed))
		else:
			A_stop()
			B_stop()	

		A_count = 0
		
	# Display new speed
		oled.draw_text(0,20,'Motor A:{:5.2f} rps'.format(A_speed/39))	
		oled.display()
		tic = pyb.millis()


	