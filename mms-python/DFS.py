import sys
from queue import LifoQueue
import API
import location
import time  # Importando a biblioteca time

# Update width and height with your maze
# this code is to maze 16x16
MAZE_WIDTH = 16
MAZE_HEIGHT = 16

# for tracking global direction
# 0 = North
# 1 = East
# 2 = South
# 3 = West
cur_direction = 0

# for tracking global 'physical' position in maze as [x, y], initialized to [0, 0]
cur_position = [0, 0]

# for tracking all maze data, create 2d array of Locations
maze = [[location.Location([i, j]) for j in range(0, MAZE_WIDTH)] for i in range(0, MAZE_HEIGHT)]

# location object stack for tracking locations that may need to be explored during mapping
loc_stack = LifoQueue()

# direction stack for easy backtracking through maze when a dead end is found during mapping
dir_stack = LifoQueue()

directions_to_center = []

# update position (-1 is move backward, 1 is move forward), currently only ever moves forward
def update_position(move_direction=1):
    global cur_position
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

# returns list of walls around current state
# example:
#   OUTPUT: [False, True, False, True] means walls to the north and south but not east or west
def get_walls():
    walls = [False, False, False, False]
    walls[cur_direction] = API.wallFront()  # is there a wall in front
    walls[(cur_direction + 1) % 4] = API.wallRight()  # is there a wall to the right
    walls[(cur_direction + 2) % 4] = False  # no wall from direction we came from
    walls[(cur_direction + 3) % 4] = API.wallLeft()  # is there a wall to the left
    if cur_position == [0, 0]:  # if first square, mark bottom wall as there
        walls[2] = True
    return walls

# marks a given node green that it has been visited (usually takes cur_position, but can take any position)
def mark_visited_api(pos=None):
    if pos is None:
        pos = cur_position
    API.setColor(pos[0], pos[1], "G")
    API.setText(pos[0], pos[1], "Salvo")  # drop string containing info on square

# marks a given node blue that it is part of the solution path (usually takes cur_position)
def mark_solution_api(pos=None):
    if pos is None:
        pos = cur_position
    API.setColor(pos[0], pos[1], "B")
    API.setText(pos[0], pos[1], "DFS")

# for printing to mms console
def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

# take all actions to move forward and update belief state
def move_forward():
    API.moveForward()  # move forward in maze
    update_position(+1)  # update current position

# take all actions to turn left and update belief state
def turn_left():
    API.turnLeft()
    update_direction(-1)  # we are turning left

# take all actions to turn right and update belief state
def turn_right():
    API.turnRight()
    update_direction(+1)  # we are turning right

# take all actions to turn around
def turn_around():
    turn_right()
    turn_right()

# change direction to specific direction
def set_dir(_dir):
    if _dir == cur_direction:  # if already facing correct direction
        return
    if _dir == (cur_direction + 1) % 4:  # if need to turn right once
        turn_right()
        return
    if _dir == (cur_direction + 2) % 4:  # if need to turn around
        turn_right()
        turn_right()
        return
    turn_left()  # if need to turn left once
    return

# turn toward an adjacent location object
def turn_toward(loc):
    _dir = cur_direction
    # find direction of adjacent location
    if cur_position[0] == loc.position[0]:  # if two locations have the same x coordinate
        if cur_position[1] - loc.position[1] == 1:  # if i am above next location, turn south
            _dir = 2
        else:  # otherwise i must be below next location
            _dir = 0
    else:  # two directions have the same y coordinate
        if cur_position[0] - loc.position[0] == 1:  # if i am to the right of location, turn west
            _dir = 3
        else:  # i must be to the left of the location
            _dir = 1
    set_dir(_dir)

# maps maze in depth first search using loc_stack
def dfs_map_maze():
    cur_loc = maze[cur_position[0]][cur_position[1]]  # create new ref to current location object for easier reference
    global directions_to_center
    if not cur_loc.visited:  # if current location has not been visited
        cur_loc.set_visited(True)  # mark location as visited
        cur_loc.set_walls(get_walls())  # set wall locations
        mark_visited_api(cur_position)  # mark current position in API

        # Verifica se a posição atual é o centro do labirinto
        if cur_position == [8, 8]:
            # Se chegou ao centro, armazena todas as direções que levaram até lá
            directions_to_center = list(dir_stack.queue)

        # if i have no north wall and north location is not visited, put it on loc_stack to explore later
        if not cur_loc.walls[0] and not maze[cur_position[0]][cur_position[1] + 1].visited:
            loc_stack.put(maze[cur_position[0]][cur_position[1] + 1])

        # if i have no east wall and east location is not visited, put it on loc_stack to explore later
        if not cur_loc.walls[1] and not maze[cur_position[0] + 1][cur_position[1]].visited:
            loc_stack.put(maze[cur_position[0] + 1][cur_position[1]])

        # if i have no south wall and south location is not visited, put it on loc_stack to explore later
        if not cur_loc.walls[2] and not maze[cur_position[0]][cur_position[1] - 1].visited:
            loc_stack.put(maze[cur_position[0]][cur_position[1] - 1])

        # if i have no west wall and west location is not visited, put it on loc_stack to explore later
        if not cur_loc.walls[3] and not maze[cur_position[0] - 1][cur_position[1]].visited:
            loc_stack.put(maze[cur_position[0] - 1][cur_position[1]])

    while True:  # do while loop to get next available position if it exists and has not been visited already
        if loc_stack.empty():  # if loc_stack is empty, backtrack to initial position then return
            if not cur_position == [0, 0]:
                set_dir((dir_stack.get() + 2) % 4)  # turn around
                move_forward()
                dfs_map_maze()  # try to move again
            return
        next_loc = loc_stack.get()  # otherwise, take locations off of the loc_stack until we get an unvisited one
        if not next_loc.visited:
            break

    # if I can move to that location from where I am, turn toward new location, save that direction, and move forward
    if cur_loc.can_move_to(next_loc):
        turn_toward(next_loc)
        dir_stack.put(cur_direction)  # save current direction for backtracking on the direction stack
        move_forward()
    else:  # put the target location back on the loc_stack, back up one square, then try again
        loc_stack.put(next_loc)
        set_dir((dir_stack.get() + 2) % 4)  # turn toward last position
        move_forward()
    dfs_map_maze()  # try to move again

def main():
    log("Running...")
    start_time = time.time()  # Inicia o cronômetro para a geração do mapa
    dfs_map_maze()  # start facing north at initial position and end back at initial position after maze has been mapped
    set_dir(0)  # reset heading to north
    end_time = time.time()  # Para o cronômetro após encontrar a solução
    log("Tempo total para gerar o mapa usando DFS: {:.2f} segundos".format(end_time - start_time))
    start_time = time.time()  # Inicia o cronômetro para execução do caminho
    execute_directions_to_center(directions_to_center)
    end_time = time.time()  # Para o cronômetro
    log("Tempo para executar o caminho do DFS: {:.2f} segundos".format(end_time - start_time))
    log("Done!")
def execute_directions_to_center(directions):
    for direction in directions:
        if direction == 0:
            next_position = maze[cur_position[0]][cur_position[1] + 1]
            mark_solution_api(cur_position)
            turn_toward(next_position)
            move_forward()
        elif direction == 1:
            next_position = maze[cur_position[0]+1][cur_position[1]]
            mark_solution_api(cur_position)
            turn_toward(next_position)
            move_forward()
        elif direction == 2:
            next_position = maze[cur_position[0]][cur_position[1] - 1]
            mark_solution_api(cur_position)
            turn_toward(next_position)
            move_forward()
        elif direction == 3:
            next_position = maze[cur_position[0]-1][cur_position[1]]
            mark_solution_api(cur_position)
            turn_toward(next_position)
            move_forward()
        
if __name__ == "__main__":
    main()
    