move = 0                        # move is a global variable initially set to 0

def L():                        # each move is a defined function
    print('Left')

def R():
    print('Right')

def B():
    print('Backwards')

def variable():                 # to be triggered on beat
    global move
    moves = [L, 0, 0, 0,        # full list of moves
             R, 0, 0, 0,
             B, 0, 0, 0]
    position = int(input('Enter Position'))
    move = moves[position]      # set based on position (increase position each time with beat)

for i in range(3):              # testing
    variable()
    if move != 0:               # ensure move is not placeholder value (0) before executing
        move()                  # execute relevent function
