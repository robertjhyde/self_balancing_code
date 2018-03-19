'''    Start of comment section
-------------------------------------------------------
Name: Basic Beat Detection implementation using microphone class
Creator:  Peter YK Cheung
Date:   16 March 2017
Revision:  1.5
-------------------------------------------------------
'''
import pyb
import time
import micropython
from pyb import Pin, Timer, ADC, DAC, LED
from array import array				# need this for memory allocation to buffers
from oled_938 import OLED_938			# Use OLED display driver
from mic import MICROPHONE
from moves import *


#  The following two lines are needed by micropython 
#   ... must include if you use interrupt in your program
micropython.alloc_emergency_exception_buf(100)

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64,
                   external_vcc=False, i2c_devid=61)  
oled.poweron()
oled.init_display()
oled.draw_text(0,20, 'Milestone 3: Loading')
oled.display()


# Create microphone object
N = 160
mic = MICROPHONE(Timer(7,freq=8000),ADC('Y11'),N)

# define ports for microphone, LEDs and trigger out (X5)
b_LED = LED(4)		# flash for beats on blue LED

def flash():  # routine to flash blue LED when beat detected
    b_LED.on()
    pyb.delay(20)
    b_LED.off()

# Define constants for main program loop - shown in UPPERCASE
M = 50						# number of instantaneous energy epochs to sum
BEAT_THRESHOLD = 1.8		# threshold for c to indicate a beat
SILENCE_THRESHOLD = 1.3  	# threshold for c to indicate silence
position = 0  			# position in movelist
s = 20  			# baseline motor speed
move_list = []  		# empty list of moves to add to
move_steps = {
    'F': forward,
    'FS': forwardslow,
    'B': back,
    'L': left,
    'LS': leftslow,
    'R': right,
    'RS': rightslow,
    'S': stop
}

# ------- IMPORT MOVES -------- #
with open('movelist.txt') as file:  # read movelist.txt
    for line in file:  # take each line (i.e. each move)
        line = line.strip()  # remove additional formatting (i.e. \n)
        move_list.append(line)  # add move to movelist

# initialise variables for main program loop 
e_ptr = 0					# pointer to energy buffer
e_buf = array('L', 0 for i in range(M))		# reserve storage for energy buffer
sum_energy = 0					# total energy in last 50 epochs
pyb.delay(100)
tic = pyb.millis()				# mark time now in msec

# ------- IDLE STATE -------- #
print('Ready to begin Milestone 3')
print('Waiting for button press')
oled.clear()
oled.draw_text(5, 20, 'MILESTONE 3: Ready')
oled.draw_text(5, 40, 'Press USR button')
oled.display()
trigger = pyb.Switch()
while not trigger():
    time.sleep(0.001)
while trigger(): pass
print('Button pressed - running')
oled.clear()
oled.draw_text(5, 20, 'MILESTONE 3: Ready')
oled.draw_text(20, 40, 'Running')
oled.display()
# real-time program loop

try:
	while True:				# Main program loop
        	if mic.buffer_full():		# semaphore signal from ISR - set if buffer is full
		# Get instantaneous energy
			E = mic.inst_energy()	# get the instantaneous energy from the microphone

            	# compute moving sum of last 50 energy epochs
			sum_energy = sum_energy - e_buf[e_ptr] + E
            		e_buf[e_ptr] = E		# over-write earliest energy with most recent
            		e_ptr = (e_ptr + 1) % M	# increment e_ptr with wraparound - 0 to M-1

			# Compute ratio of instantaneous energy/average energy
			c = E*M/sum_energy
			# Look for a beat
			if (pyb.millis()-tic > 400):	# if more than 400ms since last beat
				if (c>BEAT_THRESHOLD):
					# look for a beat, or if not found, timeout
					tic = pyb.millis()		# reset tic
					flash()         # beat found, flash blue LED ON
                    			next_step = move_list[position]
                    			print(next_step)
                    			if next_step != 'w':
                        			step = move_steps[next_step]
                        			step(s)
                        			position += 1			# increment a counter when beat detected
                        			tic = pyb.millis()
			mic.set_buffer_empty()			# reset the buffer_full flag

finally: # in the event of a crash or keyboard interrupt turn of motors before exiting program
	motor.A_stop()
	motor.B_stop()
		
