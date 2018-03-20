#########################
#      MILESTONE 4      #
#########################

import pyb
import time
import micropython
from pyb import Pin, Timer, ADC, DAC, LED
from array import array				# need this for memory allocation to buffers
from oled_938 import OLED_938			# Use OLED display driver
from mpu6050 import MPU6050
from mic import MICROPHONE			# Peter's microphone code

micropython.alloc_emergency_exception_buf(100)

# -------- PERIPHERAL SETUP -------- #

# OLED Display
# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64,
                   external_vcc=False, i2c_devid=61)
oled.poweron()
oled.init_display()
oled.draw_text(0,20, 'Milestone 4: Loading')
oled.display()

# Microphone, 125 microsecond samples
N = 160
mic = MICROPHONE(Timer(7,freq=8000),ADC('Y11'),N)

# Blue LED
b_LED = LED(4)

# IMU
imu = MPU6050(1, False)

# ----- WHEEL ASSIGNMENT ----- #
A1 = Pin('X3', Pin.OUT_PP)		    # Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP)
PWMA = Pin('X1')				    # Control speed of motor A
B2 = Pin('X7', Pin.OUT_PP)		    # Control direction of motor B
B1 = Pin('X8', Pin.OUT_PP)
PWMB = Pin('X2')				    # Control speed of motor B

# ----- TIMER ASSIGNMENT ----- #
tim = Timer(2, freq = 1000)
motorA = tim.channel (1, Timer.PWM, pin = PWMA)
motorB = tim.channel (2, Timer.PWM, pin = PWMB)

# ----- FLASH SCRIPT ----- #
def flash():
    b_LED.on()
    pyb.delay(20)
    b_LED.off()

# ----- PID FUNCTIONS ----- #
def pitch_angle(pitch, dt, alpha):
    theta = imu.pitch()
    pitch_dot = imu.get_gy()
    pitch = alpha*(pitch + pitch_dot*dt) + (1-alpha)*theta
    return (pitch, pitch_dot)


def pid_controller(pit, pit_dot, target):
    global kp, ki, kd, pit_error
    error = pit - target
    w = (kp*error) + (kd*pit_dot) + (ki*pit_error)
    pit_error += error
    if w >= 100:  # limiting w to +-100
        w = 100
    elif w <= -100:
        w = -100
    return w


# ----- MAINLOOP CONSTANTS ----- #
M = 50					# number of instantaneous energy epochs to sum
BEAT_THRESHOLD = 1.6			# threshold for c to indicate a beat
SILENCE_THRESHOLD = 1.3  		# threshold for c to indicate silence


# -- K values
kp = 4.85
ki = 0.30
kd = 0.37

# ----- MAINLOOP VARIABLES ----- #
position = 0                        # position in movelist (counter)
move_list = []                      # empty list of moves to add to
next_step = 'S'                     # step to execute (initially stopped)
e_ptr = 0                           # pointer to energy buffer
e_buf = array('L', 0 for i in range(M))     # reserve storage for energy buffer
sum_energy = 0                              # total energy in last 50 epochs
pyb.delay(100)

pitch = 0           # initial pitch angle
alpha = 0.95        # filter alpha value

motor_offset = 5        # remove motor deadzone
pitch_offset = -4.4    # counteract centre of mass: -ve = lean forward
target = pitch_offset   # initial target angle
pit_error = 0  # start with 0 cumulative error

# ------- IMPORT MOVES -------- #
with open('movelist2.txt') as file:  # read movelist.txt
    for line in file:               # take each line (i.e. each move)
        line = line.strip()         # remove additional formatting (i.e. \n)
        move_list.append(line)          # add move to movelist

move_steps = {
     #   'move': [ new target angle, A speed multiplier, B speed multiplier ]
    'F': [pitch_offset - 1, 1, 1],
    'FS': [pitch_offset - 0.4, 1, 1],
    'B': [pitch_offset + 0.2, 1, 1],
    'L': [pitch_offset - 0.9, 1, 0.6],
    'LS': [pitch_offset - 0.3, 1, 0.8],
    'R': [pitch_offset - 0.9, 0.6, 1],
    'RS': [pitch_offset - 0.3, 0.6, 1],
    'S': [pitch_offset, 1, 1]
}

# ------- IDLE STATE -------- #
print('Ready to begin Milestone 4')
print('Waiting for button press')
oled.clear()
oled.draw_text(5, 20, 'MILESTONE 4: Ready')
oled.draw_text(5, 40, 'Press USR button')
oled.display()
trigger = pyb.Switch()
while not trigger():
    time.sleep(0.001)
while trigger(): pass
print('Button pressed - running')
oled.clear()
oled.draw_text(5, 20, 'MILESTONE 4: Ready')
oled.draw_text(20, 40, 'Running')
oled.display()


tic2 = pyb.millis()                 # mark time now in msec
# ----- MAIN PROGRAM LOOP ----- #
try:
    tic1 = pyb.micros()
    while True:
        # ----- PID SECTION
        dt = pyb.micros() - tic1
        if dt > 5000:  # wait for sampling time
            pitch, pitch_dot = pitch_angle(pitch, dt * 0.000001, alpha)
            tic1 = pyb.micros()
            pid = pid_controller(pitch, pitch_dot, target)

            # -- SPEED -- #
            speed = (abs(pid) + motor_offset)
            motorA.pulse_width_percent(speed * move_steps[next_step][1])
            motorB.pulse_width_percent(speed * move_steps[next_step][2])

            if pid < 0:  # go forwards
                A1.high()
                A2.low()
                B1.high()
                B2.low()
            elif pid > 0:  # go backwards
                A1.low()
                A2.high()
                B1.low()
                B2.high()
            else:  # stay still
                A1.high(), A2.high()
                B1.high(), B2.high()

        # ----- BEAT DETECTION
        if mic.buffer_full:  # semaphore signal from ISR - set if buffer is full

            # Calculate instantaneous energy
            E = mic.inst_energy()

            # compute moving sum of last 50 energy epochs
            sum_energy = sum_energy - e_buf[e_ptr] + E
            e_buf[e_ptr] = E  # over-write earlest energy with most recent
            e_ptr = (e_ptr + 1) % M  # increment e_ptr with wraparound - 0 to M-1

            # Compute ratio of instantaneous energy/average energy
            c = E * M / sum_energy

            if (pyb.millis() - tic2 > 400):     # if more than 400ms since last beat -
                if (c > BEAT_THRESHOLD):        # look for a beat
                    flash()                     # beat found, flash blue LED
                    next_step = move_list[position]
                    target = move_steps[next_step][0]
                    print(next_step)
                    position += 1
                    tic2 = pyb.millis()         # reset tic2
            mic.set_buffer_empty()

finally:
    A1.high(), A2.high()
    B1.high(), B2.high()
