#########################
#      MILESTONE 3      #
#########################

import pyb
import time
import micropython
from pyb import Pin, Timer, ADC, DAC, LED
from array import array				# need this for memory allocation to buffers
from oled_938 import OLED_938			# Use OLED display driver
from mic import MICROPHONE			# Peter's microphone code
from moves import *				# Dance moves

micropython.alloc_emergency_exception_buf(100)	# allocate memory for iterrupts

# -------- PERIPHERAL SETUP -------- #

# OLED Display
# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64,
                   external_vcc=False, i2c_devid=61)
oled.poweron()
oled.init_display()
oled.draw_text(0,20, 'Milestone 3: Loading')
oled.display()

# Microphone, 125 microsecond samples
N = 160
mic = MICROPHONE(Timer(7,freq=8000),ADC('Y11'),N)

# Blue LED
b_LED = LED(4)

# ----- FLASH SCRIPT ----- #
def flash():	
    b_LED.on()
    pyb.delay(20)
    b_LED.off()

# ----- MAINLOOP CONSTANTS ----- #
M = 50					# number of instantaneous energy epochs to sum
BEAT_THRESHOLD = 1.6			# threshold for c to indicate a beat
SILENCE_THRESHOLD = 1.3  		# threshold for c to indicate silence
s = 35  				# baseline motor speed
move_steps = {				# relates moves in text file to dance functions
    'F': forward,
    'FS': forwardslow,
    'B': back,
    'L': left,
    'LS': leftslow,
    'R': right,
    'RS': rightslow,
    'S': stop
}

# ----- MAINLOOP VARIABLES ----- #
position = 0  				# position in movelist (counter)
move_list = []  			# empty list of moves to add to
e_ptr = 0					# pointer to energy buffer
e_buf = array('L', 0 for i in range(M))		# reserve storage for energy buffer
sum_energy = 0					# total energy in last 50 epochs
pyb.delay(100)
tic = pyb.millis()				# mark time now in msec

# ------- IMPORT MOVES -------- #
with open('movelist.txt') as file:  	# read movelist.txt
    for line in file:  			# take each line (i.e. each move)
        line = line.strip()  		# remove additional formatting (i.e. \n)
        move_list.append(line)  	# add move to movelist
	
# ------- IDLE STATE -------- #
print('Ready to begin Milestone 3')	# Debug
print('Waiting for button press')
oled.clear()
oled.draw_text(5, 20, 'MILESTONE 3: Ready')
oled.draw_text(5, 40, 'Press USR button')
oled.display()
trigger = pyb.Switch()			# Trigger on USR button press
while not trigger():			# Wait for press
    time.sleep(0.001)
while trigger(): pass			# Continue to main loop
print('Button pressed - running')	
oled.clear()
oled.draw_text(5, 20, 'MILESTONE 3: Ready')
oled.draw_text(20, 40, 'Running')
oled.display()

# ----- MAIN PROGRAM LOOP ----- #

try:
	while True:
        	if mic.buffer_full():		# semaphore signal from ISR - set if buffer is full
			E = mic.inst_energy()	# get the instantaneous energy from the microphone

            		# compute moving sum of last 50 energy epochs
			sum_energy = sum_energy - e_buf[e_ptr] + E
            		e_buf[e_ptr] = E		# over-write earliest energy with most recent
            		e_ptr = (e_ptr + 1) % M	# increment e_ptr with wraparound - 0 to M-1

			# Compute ratio of instantaneous energy/average energy
			c = E*M/sum_energy
			# Look for a beat
			if (pyb.millis()-tic > 400):	# if more than 400ms since last beat
				if (c>BEAT_THRESHOLD):			# check threshold
					flash()         		# beat found, flash blue LED ON
                    			next_step = move_list[position]		# find next move in list
                    			#print(next_step)			# debug
                    			if next_step != 'w':			# if not w(ait) i.e. no move
                        			step = move_steps[next_step]	# find corresponding function in dict
                        			step(s)				# execute corresponding function
                        		position += 1			# ready for next move
                        		tic = pyb.millis()		# reset tic
			mic.set_buffer_empty()				# reset the buffer_full flag

finally: # in case of unexpected (or expected) end, stop motors
	motor.A_stop()
	motor.B_stop()

