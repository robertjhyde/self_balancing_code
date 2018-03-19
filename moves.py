from motor import MOTOR

motor = MOTOR()

def danceforward(speed):    # forward
  print('Move forward')
  motor.left_foward(speed)
  motor.right_foward(speed)
  
def danceforwardslow(speed):   # forward slow
  print('Move forward slowly')
  motor.left_forward(speed/2)
  motor.right_forward(speed/2)

def danceback(speed):    # backwards
  print('Move backwards')
  motor.left_back(speed/2)
  motor.right_back(speed/2)

def danceright(speed):    # right
  print('Turn right')
  motor.left_forward(speed)
  motor.right_back(speed/4)

def dancerightslow(speed):   # right slow
  print('Turn right slowly')
  motor.left_forward(speed/2)
  motor.right_back(speed/6)

def danceleft(speed):    # left
  print('Turn left')
  motor.left_back(speed/4)
  motor.right_forward(speed)

def danceleftslow(speed):   # left slow
  print('Turn left slowly')
  motor.left_back(speed/6)
  motor.right_forward(speed/2)
