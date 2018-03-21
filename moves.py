from motor import MOTOR

motor = MOTOR()

def forward(speed):  # forwards
    print('forward')
    motor.B_back(speed)
    motor.A_back(speed)


def forwardslow(speed):  # slow forwards
    print('forward slowly')
    motor.B_back(2*speed/3)
    motor.A_back(2*speed/3)


def back(speed):  # backwards
    print('back')
    motor.A_forward(2*speed/3)
    motor.B_forward(2*speed/3)


def left(speed):  # left
    print('left')
    motor.B_back(speed)
    motor.A_forward(speed / 4)


def leftslow(speed):  # slow left
    print('left slowly')
    motor.B_back(2 * speed / 3)
    motor.A_forward(speed / 3)


def right(speed):  # right
    print('right')
    motor.B_forward(speed / 4)
    motor.A_back(speed)


def rightslow(speed):  # slow right
    print('right slowly')
    motor.B_forward(speed / 3)
    motor.A_back(2 * speed / 3)


def stop(speed):  # stop
    print('stop')
    motor.A_stop()
    motor.B_stop()
