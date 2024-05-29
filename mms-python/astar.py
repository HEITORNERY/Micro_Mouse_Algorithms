import heapq
import sys
import API 
import Main

cells = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

cur_direction = 0
cur_position = [0, 0]
def update_position(move_direction=1):
    global cur_position
    if cur_direction == 0:    # face norte
        cur_position[1] = cur_position[1] + move_direction
    if cur_direction == 1:  # face
        cur_position[0] = cur_position[0] + move_direction
    if cur_direction == 2:  # facing south
        cur_position[1] = cur_position[1] - move_direction
    if cur_direction == 3:  # facing west
        cur_position[0] = cur_position[0] - move_direction

def update_direction(turn_direction):
    global cur_direction  #aqui atualiza a orientação do micromouse
    cur_direction = (cur_direction + turn_direction) % 4

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def updateWalls(x,y,orient,L,R,F):
    if(L and R and F):
        if (orient==0): 
            cells[y][x]= 13
        elif (orient==1): 
            cells[y][x]= 12
        elif (orient==2): 
            cells[y][x]= 11
        elif (orient==3): 
            cells[y][x]= 14

    elif (L and R and not F):
        if (orient==0 or orient== 2): 
            cells[y][x]= 9
        elif (orient==1 or orient==3): 
            cells[y][x]= 10

    elif (L and F and not R):
        if (orient==0): 
            cells[y][x]= 8
        elif (orient==1): 
            cells[y][x]= 7
        elif (orient==2): 
            cells[y][x]= 6
        elif (orient==3): 
            cells[y][x]= 5

    elif (R and F and not L):
        if (orient==0): 
            cells[y][x]= 7
        elif (orient==1): 
            cells[y][x]= 6
        elif (orient==2): 
            cells[y][x]= 5
        elif (orient==3): 
            cells[y][x]= 8

    elif(F):
        if (orient==0): 
            cells[y][x]= 2
        elif (orient==1): 
            cells[y][x]= 3
        elif (orient==2): 
            cells[y][x]= 4
        elif (orient==3): 
            cells[y][x]= 1

    elif(L):
        if (orient==0): 
            cells[y][x]= 1
        elif (orient==1): 
            cells[y][x]= 2
        elif (orient==2): 
            cells[y][x]= 3
        elif (orient==3): 
            cells[y][x]= 4

    elif(R):
        if (orient==0): 
            cells[y][x]= 3
        elif (orient==1): 
            cells[y][x]= 4
        elif (orient==2): 
            cells[y][x]= 1
        elif (orient==3): 
            cells[y][x]= 2

    else:
        cells[y][x]= 15

# Função de heurística (distância de Manhattan)
def heuristic(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

# Função para encontrar o caminho utilizando A*
def astar(maze, start, end):
    # Inicialização
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        # Pega o nó com menor custo total (f_score)
        current_cost, current_node = heapq.heappop(open_set)
        
        if current_node == end:
            # Reconstrói o caminho
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            return path[::-1]  # Retorna o caminho invertido
       
        # Explora os vizinhos
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = current_node[0] + dx, current_node[1] + dy
            # Verifica se o vizinho está dentro dos limites do labirinto
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]):
                # Verifica se o vizinho não é uma parede
                if maze[neighbor[0]][neighbor[1]] == 0:
                    # Calcula o custo do movimento
                    tentative_g_score = g_score[current_node] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        # Atualiza o custo do movimento
                        g_score[neighbor] = tentative_g_score
                        # Calcula o custo total (f_score)
                        f_score = tentative_g_score + heuristic(neighbor, end)
                        # Adiciona o vizinho ao conjunto aberto
                        heapq.heappush(open_set, (f_score, neighbor))
                        # Registra o nó pai
                        came_from[neighbor] = current_node
    
    # Se não foi encontrado um caminho válido
    return None
def caminho(self):
    if not frente:
        API.moveForward()
        frente = API.wallFront()
        esquerda = API.wallLeft()
        direita = API.wallRight()
        Main.update_position(+1)
    if not esquerda:
        API.turnLeft()
        frente = API.wallFront()
        esquerda = API.wallLeft()
        direita = API.wallRight()
        Main.update_direction(-1)
    if not direita:
        API.turnRight()
        frente = API.wallFront()
        esquerda = API.wallLeft()
        direita = API.wallRight()
        Main.update_direction(+1)
    if frente and esquerda and direita == True:
        API.turnLeft()
        API.turnLeft()
        frente = API.wallFront()
        esquerda = API.wallLeft()
        direita = API.wallRight()
        if cur_direction == 2:
            Main.update_direction(2)
        if cur_direction == 0:
            Main.update_direction(2)


# Exemplo de uso
maze =      [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 1, 1, 1, 0]]
start_position = (0, 0)
end_position = (6, 6)
path = astar(maze, start_position, end_position)

if path:
    print("Caminho encontrado:", path)
else:
    print("Não há caminho possível.")