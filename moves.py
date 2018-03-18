from motor import MOTOR

motor = MOTOR()

def F(speed):    # forward
  print('Move forward')
  motor.A_foward(speed)
  motor.B_foward(speed)
  
def FS(speed):   # forward slow
  print('Move forward slowly')
  motor.A_forward(speed/2)
  motor.B_forward(speed/2)

def B(speed):    # backwards
  print('Move backwards')
  motor.A_back(speed/2)
  motor.B_back(speed/2)

def R(speed):    # right
  print('Turn right')
  motor.A_forward(speed)
  motor.B_forward(speed/4)

def RS(speed):   # right slow
  print('Turn right slowly')
  motor.A_forward(speed/2)
  motor.A_backwards(speed/6)

def L(speed):    # left
  print('Turn left')
  motor.A_forward(speed/4)
  motor.B_forward(speed)

def LS(speed):   # left slow
  print('Turn left slowly')
  motor.A_forward(speed/6)
  motor.B_forward(speed/2)
