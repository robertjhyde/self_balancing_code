import pyb
from pyb import Pin, Timer, ADC, UART
from oled_938 import OLED_938

print('MILESTONE 1')

# ----- OLED CONFIG ----- #
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64, external_vcc=False, i2c_devid=61)
oled.poweron()
oled.init_display()

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

A1.high(), A2.high()  # Initial conditions - motors on break
B1.high(), B2.high()

speed = 0   # Speed variable to change
SLOW = 30   # Reference speeds
FAST = 60

oled.draw_text(5, 20, 'MILESTONE 1: Ready') # Ready to begin commands
oled.display()                              # OLED on

while True:                                 # Infinite loop
    while (uart.any() != 5):                # Wait for full command
        n = uart.any()
    command = uart.read(5)
    # print(str(command))                   # Debugging

    # -- MOVEMENT -- #
    motorA.pulse_width_percent(speed)
    motorB.pulse_width_percent(speed)

    if command[3] == ord('1'):      # On button press
        if command[2] == ord('5'):  # Up arrow
            print('Forward')
            A1.high()
            A2.low()
            B1.high()
            B2.low()
            speed = FAST
        if command[2] == ord('6'):  # Down arrow
            print('Reverse')
            A1.low()
            A2.high()
            B1.low()
            B2.high()
            speed = SLOW
        if command[2] == ord('7'):  # Left arrow
            print('Turn Left')
            A1.low()
            A2.high()
            B1.high()
            B2.low()
            speed = SLOW
        if command[2] == ord('8'):  # Right arrow
            print('Turn Right')
            A1.high()
            A2.low()
            B1.low()
            B2.high()
            speed = SLOW
    if command[3] == ord('0'):      # On button release
        print('Stopped')
        A1.low()
        A2.low()
        B1.low()
        B2.low()
