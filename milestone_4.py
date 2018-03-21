import pyb, time
from pyb import LED, DAC, ADC, Pin, Timer, UART
from oled_938 import OLED_938
from mpu6050 import MPU6050

# ----- POTENTIOMETER + USER BUTTON ASSIGNMENT ----- #
pot = ADC(Pin('X11'))
usr = pyb.Switch()

# ----- IMU ASSIGNMENT (to X9 and X10) ----- #
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

# ----- SPEED CONTROL WITH BLUETOOTH ----- #
uart = UART(6)
uart.init(9600, bits=8, parity=None, stop=2)

# ----- OLED ASSIGNMENT ----- #
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64, external_vcc=False, i2c_devid=61)
oled.poweron()
oled.init_display()
oled.draw_text(0,0, 'Group 9')
oled.draw_text(0,10, 'Milestone 4')
oled.draw_text(0,20, 'Initialising...')
oled.draw_text(0,30, 'Press USER button to continue')
oled.display()


while not usr():  # prevent program from running until user is ready to continue
    time.sleep(0.001)  # repeats sleep until USER button is pressed
while usr(): pass  # when USER button is pressed, move on

'''
while not usr(): # prevent program from running until user is ready and has chosen value on POT
    time.sleep(0.001)
    kp = pot.read() * 8 / 4095 # use pot to set Kp
    oled.draw_text(0, 30, 'Kp = {:5.2f}'.format(kp)) # display live value on oled
    oled.display()
while usr(): pass # wait for button release
while not usr(): # prevent program from running until user is ready and has chosen value on POT
    time.sleep(0.001)
    ki = pot.read() / 4095 * 2 # use pot to set Ki
    oled.draw_text(0, 40, 'Ki = {:5.2f}'.format(ki)) # display live value on oled
    oled.display()
while usr(): pass # wait for button release
while not usr(): # prevent program from running until user is ready and has chosen value on POT
    time.sleep(0.001)
    kd = pot.read() / 4095 # use pot to set Kd
    oled.draw_text(0, 50, 'Kd = {:5.2f}'.format(kd)) # display live value on oled
    oled.display()
while usr(): pass # wait for button release
'''

# ----- TUNED K VALUES ----- #
kp = 4.85
ki = 0.30  # these were found from iterating using the above commented out code
kd = 0.37


# ----- UPDATE OLED SCREEN ----- #
oled.clear()
oled.draw_text(0,20, 'Variables chosen')
oled.draw_text(10, 30, 'Kp = {:5.2f}'.format(kp))  # display live value on oled
oled.draw_text(10, 40, 'Ki = {:5.2f}'.format(ki))  # display live value on oled
oled.draw_text(10, 50, 'Kd = {:5.2f}'.format(kd))  # display live value on oled
oled.display()


def pitch_angle(pitch, dt, alpha):  # function to calculate pitch angle from imu sensor
    theta = imu.pitch()  # get pitch angle from accelerometer
    pitch_dot = imu.get_gy()  # get rate of change of pitch from gyroscope
    pitch = alpha*(pitch + pitch_dot*dt) + (1-alpha)*theta  # using a complemetery filter, calculate pitch angle of robot
    return (pitch, pitch_dot)  # return new pitch and pitch_dot values


def pid_controller(pit, pit_dot, target):  # function to calculate pid value
    global kp, ki, kd, pit_error  # bring in global variables
    error = pit - target  # find error from target value
    w = (kp*error) + (kd*pit_dot) + (ki*pit_error)  # using given equation find w (as the 'dt' term is constant it is included in the 'ki' term)
    pit_error += error  # update accumulative error value
    if w >= 100:  # limiting w to +-100
        w = 100
    elif w <= -100:
        w = -100
    return w  # return pid value for assignment to motor speed



'''
Main program loop
'''

pitch = 0  # initial pitch angle
alpha = 0.95  # filter alpha value

motor_offset = 5  # remove motor deadzone for better control
pitch_offset = -4.4  # to counter-act centre of mass, -ve = lean towards front of board
pit_error = 0  # start with 0 accumulative error


try:
    tic = pyb.micros()  # start timer
    while True:

        dt = pyb.micros() - tic  # calculate time difference
        if dt > 5000:		# wait for sampling time (5ms)
            pitch, pitch_dot = pitch_angle(pitch, dt*0.000001, alpha)  # find pitch
            tic = pyb.micros()  # update tic value
            pid = pid_controller(pitch, pitch_dot, pitch_offset)  # find pid value

            
            # -- SPEED -- #
            speed = (abs(pid) + motor_offset)  # calculate speed from pid value
            motorA.pulse_width_percent(speed)  # assign this speed value to the motors
            motorB.pulse_width_percent(speed)

            if pid < 0:  # go forwards if leaning forwards
                A1.high()
                A2.low()
                B1.high()
                B2.low()
            elif pid > 0:  # go backwards if leaning backwards
                A1.low()
                A2.high()
                B1.low()
                B2.high()
            else:  # stay still if upright
                A1.high(), A2.high()
                B1.high(), B2.high()


finally:  # stop everything if it crashes
    A1.high(), A2.high()
    B1.high(), B2.high()
