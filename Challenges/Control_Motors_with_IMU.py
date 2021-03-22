import pyb
import time
from pyb import LED, Pin, Timer, ADC
from oled_938 import OLED_938	# Use OLED display driver
from mpu6050 import MPU6050

# Define LEDs
b_LED = LED(4)

# IMU connected to X9 and X10
imu = MPU6050(1, False)    	# Use I2C port 1 on Pyboard

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
oled.draw_text(0, 0, "Hannah Knight")
oled.draw_text(0,20,"Challenge 2")	
oled.draw_text(0,40,"Press the USR switch")	
oled.display()

print("Waiting for button press")
trigger = pyb.Switch()	# create trigger switch object
while not trigger():	# wait for trigger to be pressed
	time.sleep(0.001)
while trigger(): pass	# wait for release
print("Button pressed - program running")

def read_imu(dt):
	# prints the pitch and roll angles to the screen
	# both have been passed through a complementary filter
	global g_pitch
	alpha = 0.7    # larger = longer time constant
	pitch = int(imu.pitch())  # pitch mesaured using accelerometer - measured in degrees
	g_pitch = alpha*(g_pitch + imu.get_gy()*dt*0.001) + (1-alpha)*pitch # derived pitch using gyro

def isr_motorA(self, line):
	countA += 1
			
def isr_motorB(self, line):
	countB += 1

def isr_speed_timer(self,t):
	speedA = self.countA
	speedB = self.countB
	countA = 0
	countB = 0

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
A_speed = 0
A_count = 0
B_speed = 0
B_count = 0

#-------  Section to set up Interrupts ----------
def isr_motorA(dummy):	# motor sensor ISR - just count transitions
	global A_count
	A_count += 1
	global B_count
	B_count += 1
		
def isr_speed_timer(dummy): 	# timer interrupt at 100msec intervals
	global A_count
	global A_speed
	A_speed = A_count			# remember count value
	A_count = 0					# reset the count

	global B_count
	global B_speed
	B_speed = B_count			# remember count value
	B_count = 0					# reset the count
	
# Create external interrupts for motorA Hall Effect Senor
import micropython
micropython.alloc_emergency_exception_buf(100)
from pyb import ExtInt

motorA_int = ExtInt ('Y4', ExtInt.IRQ_RISING, Pin.PULL_NONE,isr_motorA)
motorB_int = ExtInt ('Y5', ExtInt.IRQ_RISING, Pin.PULL_NONE,isr_motorB)

# Create timer interrupts at 100 msec intervals
speed_timer = pyb.Timer(4, freq=10)
speed_timer.callback(isr_speed_timer)

#-------  END of Interrupt Section  ----------

g_pitch = 0
g_roll = 0 
tic = pyb.millis()

while True:				# loop forever until CTRL-C

    b_LED.toggle()
	toc = pyb.millis()
	read_imu(toc-tic)
	tic = pyb.millis()
	
	# drive motor
	# speed derived from pitch angle which can be between +90 and -90
	# motor speed can be set between -100 and +100 (PWM)
	speed = -((g_pitch)*100/90)
	if (speed >= DEADZONE):		# forward
		A_forward(speed)
		B_forward(speed)
	elif (speed <= -DEADZONE):
		A_back(abs(speed))
		B_back(abs(speed))
	else:
		A_stop()
		B_stop()	

	# Display text
	oled.clear()
	oled.draw_text(0, 0, "Pitch angle: {:.2f}".format(g_pitch))
	oled.draw_text(0,20,'Motor A:{:5.2f} rps'.format(A_speed/39))	
	oled.draw_text(0,40,'Motor A:{:5.2f} rps'.format(B_speed/39))	
	oled.display()
	
	pyb.delay(100)