import pyb
from pyb import Pin, Timer, ADC, UART


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


def danceforward(speed):    # forward
    print('Move forward')
    A1.high()
    A2.low()
    B1.high()
    B2.low()
    motorA.pulse_width_percent(speed)
    motorB.pulse_width_percent(speed)

def danceforwardslow(speed):   # forward slow
    print('Move forward slowly')
    A1.high()
    A2.low()
    B1.high()
    B2.low()
    motorA.pulse_width_percent(speed/2)
    motorB.pulse_width_percent(speed/2)

def danceback(speed):    # backwards
    print('Move backwards')
    A1.low()
    A2.high()
    B1.low()
    B2.high()
    motorA.pulse_width_percent(speed/2)
    motorB.pulse_width_percent(speed/2)

def danceright(speed):    # right
    print('Turn right')
    A1.high()
    A2.low()
    B1.low()
    B2.high()
    motorA.pulse_width_percent(speed)
    motorB.pulse_width_percent(speed/4)

def dancerightslow(speed):   # right slow
    print('Turn right slowly')
    A1.high()
    A2.low()
    B1.low()
    B2.high()
    motorA.pulse_width_percent(speed/2)
    motorB.pulse_width_percent(speed/6)

def danceleft(speed):    # left
    print('Turn left')
    A1.low()
    A2.high()
    B1.high()
    B2.low()
    motorA.pulse_width_percent(speed/4)
    motorB.pulse_width_percent(speed)

def danceleftslow(speed):   # left slow
    print('Turn left slowly')
    A1.low()
    A2.high()
    B1.high()
    B2.low()
    motorA.pulse_width_percent(speed/6)
    motorB.pulse_width_percent(speed/2)
