import pyb
import time
from pyb import Pin, Timer, ADC, DAC, LED
from array import array			# need this for memory allocation to buffers
from oled_938 import OLED_938	# Use OLED display driver
from mic import MICROPHONE

#  The following two lines are needed by micropython
#   ... must include if you use interrupt in your program
import micropython
micropython.alloc_emergency_exception_buf(100)

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

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64,
				   external_vcc=False, i2c_devid=60)
oled.poweron()
oled.init_display()
oled.draw_text(0, 0, "Samantha Foong")
oled.draw_text(0,20,"Challenge 4")	
oled.draw_text(0,30,"Dancing Segway")
oled.draw_text(0,50,"Press the USR switch")	
oled.display()

# define ports for microphone, LEDs and trigger out (X5)
SAMP_FREQ = 8000
N = 160				# size of sample buffer s_buf[]
mic = MICROPHONE(Timer(7,freq=SAMP_FREQ),ADC('Y11'),N)
b_LED = LED(4)		# flash for beats on blue LED

s_buf = array('H', 0 for i in range(N))  # reserve buffer memory
ptr = 0				# sample buffer index pointer
buffer_full = False	# semaphore - ISR communicate with main program

def b_flash():		# routine to flash blue LED when beat detected
	b_LED.on()
	pyb.delay(30)
	b_LED.off()

def r_flash():
		r_LED.on()
		pyb.delay(30)
		r_LED.off()
	
def energy(buf):	# Compute energy of signal in buffer
	sum = 0
	for i in range(len(buf)):
		s = buf[i] - MIC_OFFSET	# adjust sample to remove dc offset
		sum = sum + s*s			# accumulate sum of energy
	return sum

# motor controls
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


def danceMoves(filename):
	'''
	Reads a text file, splits it into characters, puts the characters into a list
	'''
	file = open(filename,'r')
	moves = file.read().split()		# splits text into characters at the whitespace
	return moves		#returns a list of characters e.g. ['F', 'B', 'F', 'B']

def nowDance(i):
	'''
	Takes a string of letters and assigns a dance move for each
	'''
	moves = danceMoves('dance_moves.txt')
	if moves[i] == 'F':
		A_forward(100)
		B_forward(100)
        pyb.delay(300)
        A_stop()
        B_stop()
	elif moves[i] == 'B':
		A_back(100)
		B_back(100)
        pyb.delay(300)
        A_stop()
        B_stop()
	elif moves[i] == 'L':
		A_forward(100)
		B_forward(50)
        pyb.delay(300)
        A_stop()
        B_stop()
	elif moves[i] == 'R':
		A_forward(50)
		B_forward(100)
        pyb.delay(300)
        A_stop()
        B_stop()


# Define constants for main program loop - shown in UPPERCASE
M = 50						# number of instantaneous energy epochs to sum
BEAT_THRESHOLD = 2.0		# threshold for c to indicate a beat
SILENCE_THRESHOLD = 1.3		# threshold for c to indicate silence

# initialise variables for main program loop
e_ptr = 0					# pointer to energy buffer
e_buf = array('L', 0 for i in range(M))	# reserve storage for energy buffer
sum_energy = 0				# total energy in last 50 epochs

print("Waiting for button press")
trigger = pyb.Switch()	# create trigger switch object
while not trigger():	# wait for trigger to be pressed
	time.sleep(0.001)	# until then, sleep
while trigger(): 
	pass	# wait for release
print("Button pressed - program running")

oled.clear()
oled.draw_text(0, 0, "Samantha Foong")
oled.draw_text(0,20,"Challenge 4")	
oled.draw_text(0,30,"Dancing Segway")
oled.draw_text(0,50, 'Ready to GO')	# Useful to show what's happening
oled.display()

pyb.delay(100)

tic = pyb.millis()			# mark time now in msec
try:
	while True:				# Main program loop
		if mic.buffer_full():		# semaphore signal from ISR - set if buffer is full
			
			# Calculate instantaneous energy
			E = mic.inst_energy()
			
			# compute moving sum of last 50 energy epochs
			sum_energy = sum_energy - e_buf[e_ptr] + E
			e_buf[e_ptr] = E		# over-write earlest energy with most recent
			e_ptr = (e_ptr + 1) % M	# increment e_ptr with wraparound - 0 to M-1
			
			# Compute ratio of instantaneous energy/average energy
			c = E*M/sum_energy
			
			# Look for beat
			if (pyb.millis()-tic > 500):	# if more than 500ms since last beat
				if (c>BEAT_THRESHOLD):		# if beat found
					i=0
					nowDance(i)				#do next dance move
					i = (i+1) % 8
			mic.set_buffer_empty()

finally:
	A_stop()
	B_stop()