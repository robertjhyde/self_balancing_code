import pyb
from pyb import Pin, Timer, ADC, UART
from oled_938 import OLED_938
print('TEST: Run both wheels')

# ----- OLED CONFIG ----- #
old = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height = 64, external_vcc=False, i2c_devid=61)
oled.poweron()
oled.init_display()

# ----- WHEEL DIRECTION ASSIGNMENT ----- #
L1 = Pin('X7' ,Pin.OUT_PP)                           # Left FORWARD                   
L2 = Pin('X8' ,Pin.OUT_PP)                          # Left REVERSE
R1 = Pin('X3', Pin.OUT_PP)                           # Right FORWARD
R2 = Pin('X4', Pin.OUT_PP)                           # Right REVERSE

# ----- POTENTIOMETER AND PWM ----- #
pot = ADC(Pin('X8'))                                 # I/O Pin for ADC
PWMR = Pin('X1')                                     # PWM for right motor
PWML = Pin('X2')                                     # PWM for left wheel

# ----- TIMERS ----- #
tim = Timer(2, freq = 1000)                          # Timer2 controls both PWM signals
motorL = tim.channel(1, Timer.PWM, pin = PWML)       # PWM for left motor
motorR = tim.channel(2, Timer.PWM, pin = PWMR)       # PWM for right motor

# ----- SPEED CONTROL WITH BLUETOOTH ----- #
uart = UART(6)
uart.init(9600, bits=8, parity = None, stop = 2)

ADCL = ADC(Pin('X2'))
ADCR = ADC(Pin('X1'))
                
L1.high()                                          # Initial conditions - motors on break
L2.high()
R1.high()
R2.high()

speed = 0
DEADZONE = 5
SLOW = 20
HALF = 40
MAX = 80

oled.draw_text(0,20,'MILESTONE 1: Ready')         # Ready to begin commands

while True:                                       # loop forever until CTRL-C
    while (uart.any()!=5):                        # Wait until we have 5 chars
        n = uart.any()
    command = uart.read(5)
    motorL.pulse_width_percent(speed)
    motorR.pulse_width_percent(speed)

# -- MOVEMENT -- #
    if command[3] == ord('1'):
        if command[2] == ord('5'):
            print('Forward')
            L1.high()
            L2.low()
            R1.high()
            R2.low()
            speed = HALF
        if command[2] == ord('6'):
            print('Reverse')
            L1.low()
            L2.high()
            R1.low()
            R2.high()
            speed = SLOW
        if command[2] == ord('7'):
            print('Turn Left')
            L1.high()
            L2.low()
            R1.low()
            R2.high()
            speed = HALF
        if command[2] == ord('8'):
            print('Turn Right')
            L1.low()
            L2.high()
            R1.low()
            R2.high()
            speed = HALF
    if command[3] == ord('0') and command[2]==ord('5') or command[2]==ord('6') or command[2]==ord('7') or command[2]==ord('8'):
        print('Stopped')
        L1.low()
        L2.low()
        R1.low()
        R2.low()
