import pyb
import math
import gc
from pyb import LED, USB_VCP, DAC, Timer, ADC, Pin, UART
from array import array
from oled_938 import OLED_938
from mpu6050 import MPU6050
from motor import DRIVE

# Define various ports, pins and peripherals
a_out = DAC(1, bits=12)
a_in = ADC(Pin('X12'))
pot = ADC(Pin('X11'))
mic = ADC(Pin('Y11'))
r_LED = LED(1)
g_LED = LED(2)
y_LED = LED(3)
b_LED = LED(4)

pitch = 0

#  Configure X2:4, X7 as setting input pin - pull_up to receive switch settings
s0=Pin('Y8',pyb.Pin.IN,pyb.Pin.PULL_UP)
s1=Pin('Y3',pyb.Pin.IN,pyb.Pin.PULL_UP)
s2=Pin('X6',pyb.Pin.IN,pyb.Pin.PULL_UP)

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
i2c = pyb.I2C(2, pyb.I2C.MASTER)
devid = i2c.scan()
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64,
                   external_vcc=False, i2c_devid=i2c.scan()[0])
oled.poweron()
oled.init_display()

# IMU connected to X9 and X10
imu = MPU6050(1, False)

#  initialize UART on Y1 and Y2
uart = UART(6)
uart.init(9600, bits=8, parity = None, stop = 2)\

# create motor class to drive motors
motor = DRIVE()

sw = pyb.Switch()
tic = pyb.millis()

def send_uart(message):
	for i in range(len(message)):
		uart.writechar(ord(message[i]))
	uart.writechar(13)
	uart.writechar(10)

def sw_released():
    while sw.value() == True:
        pass        # wait for release
    return

def test_imu(dt):
	global pitch
	alpha = 0.7    # larger = longer time constant
	y_LED.on()
	pitch = int(imu.pitch())
	pitch = alpha*(pitch + imu.get_gy()*dt*0.001) + (1-alpha)*pitch
	#show info
	y = 32 - int(31*pitch/100)
	y = max(min(y,63) ,0)
	oled.clear()
	oled.draw_text(0,0,"Pitch " + str(pitch))
	oled.draw_text(0,26, "Speed " + myspeed)
	oled.display()	

speed=0
previous_et = 0
cumilative_error = 0
kp = 20
kd = 0.5
ki = 80
target = 4.2
tic = 10
while True:
	motor.stop()
	print('IMU Test')
	sw_released()
	while sw.value() == False:

        # calculate get imu data
		toc = pyb.millis()
		alpha = 0.99
		theta = imu.pitch()
		dt = toc-tic
		pitch_dot = imu.get_gy()
		pitch = alpha*(pitch + imu.get_gy()*dt*0.001) + (1-alpha)*theta

        # PID control
		if dt == 0:
			dt = 1
		et = target - pitch
		cumilative_error = cumilative_error + et*dt*0.001
		et_dot = (et-previous_et)/(dt*0.001)
		previous_et = et
		speed = (kp*(et) + kd*(et_dot) + ki*(cumilative_error) )*-1
		if speed > 100:
			speed = 100
		if speed < -100:
			speed = -100
		myspeed = str(speed)

        # drive motor
		if speed > 5 or speed < -5:
			motor.set_speed(speed)
		else:
			motor.set_speed(0)
		motor.set_turn(0)
		motor.drive()
		actual_speed = motor.get_speedB()
		actual_speed2 = motor.get_speedA()

		#show info
		# y = 32 - int(31*theta/100)
		# y = max(min(y,63) ,0)
		# oled.clear()
		# oled.draw_text(0,0,"Pitch " + str(pitch))
		# oled.draw_text(0,26, "Speed " + myspeed)
		# oled.draw_text(0,39, "Actual Speed R "+str(actual_speed))
		# oled.draw_text(0,52, "Actual Speed L "+str(actual_speed2))    
		# oled.display()	
		tic = pyb.millis()
		pyb.delay(10)
	r_LED.on()
	
