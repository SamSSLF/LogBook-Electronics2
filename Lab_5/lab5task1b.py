import pyb
from pyb import Pin, Timer, ADC

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

# Define 10k Potentiometer
pot = pyb.ADC(Pin('X11'))

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
	
# Use keypad U and D keys to control speed
DEADZONE = 5
speed = 0

while True:				# loop forever until CTRL-C
	speed = int((pot.read()-2048)*200/4096)         #returns a number between -100 and 100
	if (speed >= DEADZONE):		# forward 5 to 100
		A_forward(speed)
		B_forward(speed)
	elif (speed <= -DEADZONE):   #backward -100 to 0
		A_back(abs(speed))
		B_back(abs(speed))
	else:
		A_stop()
		B_stop()	