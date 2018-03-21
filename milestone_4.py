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
oled.draw_text(0,0, 'Self_balance_ting.py')
oled.draw_text(0,10, 'Initialising...')
oled.draw_text(0,20, 'Press USER button to continue')
oled.display()


while not usr():
    time.sleep(0.001)
while usr(): pass

'''
while not usr(): # prevent program from running until user is ready and has chosen value on POT
    time.sleep(0.001)
    kp = pot.read() * 8 / 4095 # use pot to set Kp = 5.41
    oled.draw_text(0, 30, 'Kp = {:5.2f}'.format(kp)) # display live value on oled
    oled.display()
while usr(): pass # wait for button release
while not usr(): # prevent program from running until user is ready and has chosen value on POT
    time.sleep(0.001)
    ki = pot.read() / 4095 * 2 # use pot to set Ki = 0.22
    oled.draw_text(0, 40, 'Ki = {:5.2f}'.format(ki)) # display live value on oled
    oled.display()
while usr(): pass # wait for button release
while not usr(): # prevent program from running until user is ready and has chosen value on POT
    time.sleep(0.001)
    kd = pot.read() / 4095 # use pot to set Kd = 0.33
    oled.draw_text(0, 50, 'Kd = {:5.2f}'.format(kd)) # display live value on oled
    oled.display()
while usr(): pass # wait for button release
'''

kp = 4.85
ki = 0.30
kd = 0.37

oled.clear()
oled.draw_text(0,20, 'Variables chosen')
oled.display()


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


oled.draw_text(10, 30, 'Kp = {:5.2f}'.format(kp))  # display live value on oled
oled.draw_text(10, 40, 'Ki = {:5.2f}'.format(ki))  # display live value on oled
oled.draw_text(10, 50, 'Kd = {:5.2f}'.format(kd))  # display live value on oled
oled.display()


'''
Main program loop
'''

pitch = 0  # initial pitch angle
alpha = 0.95  # filter alpha value

motor_offset = 5  # remove motor deadzone for better control
pitch_offset = -4.4  # to counter-act centre of mass, -ve = lean towards front of board
pit_error = 0  # start with 0 cumulative error


try:
    tic = pyb.micros()
    while True:

        dt = pyb.micros() - tic
        if dt > 5000:		# wait for sampling time
            pitch, pitch_dot = pitch_angle(pitch, dt*0.000001, alpha)
            tic = pyb.micros()
            pid = pid_controller(pitch, pitch_dot, pitch_offset)

            #print(pid,pitch,pitch_dot)

            # -- SPEED -- #
            speed = (abs(pid) + motor_offset)
            motorA.pulse_width_percent(speed)
            motorB.pulse_width_percent(speed)

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
                #speed = (abs(pid)+motor_offset)
            else:  # stay still
                A1.high(), A2.high()
                B1.high(), B2.high()


finally:  # stop everything if it crashes
    A1.high(), A2.high()
    B1.high(), B2.high()
