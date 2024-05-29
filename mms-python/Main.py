import API
import sys
import random
cur_direction = 0
cur_position = [0,0]
def update_position(move_direction=1):
    global cur_position
    if cur_position == [0,0]:
        cur_position[0] = 0
        cur_position[1] = 0
    if cur_direction == 0:    # facing north
        cur_position[1] = cur_position[1] + move_direction
    elif cur_direction == 1:  # facing east
        cur_position[0] = cur_position[0] + move_direction
    elif cur_direction == 2:  # facing south
        cur_position[1] = cur_position[1] - move_direction
    elif cur_direction == 3:  # facing west
        cur_position[0] = cur_position[0] - move_direction

# update direction (-1 is left, 1 is right)
def update_direction(turn_direction):
    global cur_direction  # we are modifying global current direction
    cur_direction = (cur_direction + turn_direction) % 4

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def main():
    frente = API.wallFront()
    esquerda = API.wallLeft()
    direita = API.wallRight()
    log(cur_direction)
    log("Running...")
    API.setColor(0, 0, "G")
    API.setText(0, 0, "abc")
    while True:
        log(cur_position)
        if not frente:
            API.moveForward()
            frente = API.wallFront()
            esquerda = API.wallLeft()
            direita = API.wallRight()
            update_position(+1)
        if not esquerda:
            API.turnLeft()
            frente = API.wallFront()
            esquerda = API.wallLeft()
            direita = API.wallRight()
            update_direction(-1)
        if not direita:
            API.turnRight()
            frente = API.wallFront()
            esquerda = API.wallLeft()
            direita = API.wallRight()
            update_direction(+1)
        if frente and esquerda and direita == True:
            API.turnLeft()
            API.turnLeft()
            frente = API.wallFront()
            esquerda = API.wallLeft()
            direita = API.wallRight()
            if cur_direction == 2:
                update_direction(2)
                continue
            if cur_direction == 0:
                update_direction(2) 

if __name__ == "__main__":
    main()
