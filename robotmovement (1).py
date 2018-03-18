import pyb
from pyb import Pin, Timer

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
	
def left(value): #Wheel A moves forward (assuming it's the left wheel)
	A1.high()    #Wheel B stays (assuming it's the right wheel)
	A2.low()
	motorA.pulse_width_percent(value)
	B1.high()
	B2.high()

def right(value):
	A1.high()
	A2.high()
	B1.high()
	B2.low()
	motorB.pulse_width_percent(value)

def back(value):
	A1.low()
	A2.high()
	motorA.pulse_width_percent(value)
	B1.low()
	B2.high()
	motorB.pulse_width_percent(value)
	

def left_hop(value): #right wheel stays 
	B1.high()		 #left wheel goes front for 1 sec and comes back
	B2.high()
	A1.high()
	A2.low()
	motorA.pulse_width_percent(value)	
	# delay in here?
	A1.low()
	A2.high()
	motorA.pulse_width_percent(value)

def right_hop(value):
	A1.high()
	A2.high()
	B1.high()
	B2.low()
	motorB.pulse_width_percent(value)
	# delay in here?
	B1.low()
	B2.high()
	motorB.pulse_width_percent(value)
	

def criss_cross_1(value): #right wheel goes forward and left goes back
	B1.low()
	B2.high()
	morotB.pulse_width_percent(value)
	A1.high()
	A2.low()
	motorA.pulse_width_percent(value)
	
def cris_cross_2(value):
	B1.high()
	B2.low()
	motorB.pulse_width_percent(value)
	A1.low()
	A2.high()
	motorA.pulse_width_percent(value)
		

def chacha_1(value): #both wheel goes backward, but one wheel goes half speed of the other
	B1.low()
	B2.high()
	motorB.pulse_width_percent(value)
	A1.low()
	A2.high()
	motorA.pulse_width_percent(value/2)
	
def chacha_2(value):
	B1.low()
	B2.high()
	motorB.pulse_width_percent(value/3)
	A1.low()
	A2.high()
	motorA.pulse_width_percent(value)
	
def chacha_3(value):
	B1.high()
	B2.low()
	motorB.pulse_width_percent(value/2)
	A1.high()
	A2.low()
	motorA.pulse_width_percent(value)

def chacha_4(value):
	B1.high()
	B2.low()
	motorB.pulse_width_percent(value)
	A1.high()
	A2.low()
	motorA.pulse_width_percent(value/3)
