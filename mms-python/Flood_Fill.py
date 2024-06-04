import API
import sys
import time

# Variáveis globais para a posição atual do robô.
# 0,0 sendo o canto superior esquerdo, 15,15 sendo o canto inferior direito
curr_row = 15
curr_col = 0

# Array 2D global de inteiros que representa o algoritmo de flood fill
path = [[0 for _ in range(16)] for _ in range(16)]

# Array 2D global de caracteres que representa as paredes
walls = [[0 for _ in range(16)] for _ in range(16)]

# Largura e altura máximas do labirinto
MAX_X = 16
MAX_Y = 16

# Valores de sensores simulados. Verdadeiro ou falso
wall_left = False
wall_right = False
wall_front = False

# Valores para determinar a direção que o robô está enfrentando
# e para qual direção ele precisa virar.
# 0 para cima, 1 para direita, 2 para baixo, 3 para esquerda
go_to = 0
facing = 1

# for printing to mms console
def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def init_path():
    """
    Esta função é usada para inicializar o array path
    com -1 para indicar que o algoritmo do labirinto não foi
    executado.
    
    Também é chamada após cada movimento para reexecutar o algoritmo de flood fill.
    """
    # Define cada célula com o valor -1
    for x in range(16):
        for y in range(16):
            path[x][y] = -1

def flood(pos_row, pos_col, distance):
    """
    Função recursiva para executar o algoritmo de flood fill
    e considerar as paredes do labirinto.
    """

    # Verifica se a linha e coluna atuais estão fora dos limites.
    # Se estiverem, não faça nada e retorne
    if pos_row > MAX_X - 1 or pos_row < 0:
        return
    if pos_col > MAX_Y - 1 or pos_col < 0:
        return

    # Verifica se a célula atual tem um valor de distância menor que a chamada atual.
    # Se sim, não há necessidade de mudar o valor, retorne.
    if path[pos_row][pos_col] < distance and path[pos_row][pos_col] != -1:
        return

    # Define a célula atual igual à distância atual do centro.
    path[pos_row][pos_col] = distance

    # Chamada recursiva na célula à direita da célula atual.
    # Se não houver uma parede à direita, chama flood, caso contrário, não faça nada.
    if not (walls[pos_row][pos_col] & 0b0100):
        flood(pos_row, pos_col + 1, distance + 1)

    # Chamada recursiva na célula à esquerda. Verifica se a coluna atual
    # está na borda esquerda ou se há uma parede à esquerda.
    # Se houver, não faça nada, caso contrário, chama flood.
    if pos_col == 0 or not (walls[pos_row][pos_col - 1] & 0b0100):
        flood(pos_row, pos_col - 1, distance + 1)

    # Chamada recursiva na célula abaixo da célula atual.
    # Se não houver uma parede abaixo, chama flood, caso contrário, não faça nada.
    if not (walls[pos_row][pos_col] & 0b0010):
        flood(pos_row + 1, pos_col, distance + 1)

    # Chamada recursiva na célula acima. Verifica se a linha atual
    # está na borda superior ou se há uma parede acima.
    # Se houver, não faça nada, caso contrário, chama flood.
    if pos_row == 0 or not (walls[pos_row - 1][pos_col] & 0b0010):
        flood(pos_row - 1, pos_col, distance + 1)
    
def print_flood_fill():
    """
    Função para exibir o algoritmo de flood fill no simulador MicroMouse.
    """

    for row in range(16):
        for col in range(16):
            path_num = path[15 - col][row]
            text = str(path_num)
            API.setText(row, col, text)

def get_sensors():
    """
    Função simulada para determinar se há uma parede à esquerda, 
    na frente ou à direita do mouse.
    """

    global wall_left, wall_front, wall_right

    wall_left = API.wallLeft()
    wall_front = API.wallFront()
    wall_right = API.wallRight()

def update_walls():
    """
    Função para atualizar o array walls se o mouse encontrar novas paredes.
    """
    global walls, curr_row, curr_col, facing, wall_left, wall_right, wall_front

    if facing == 0:  # Se o mouse está voltado para cima
        if wall_left and curr_col != 0:
            walls[curr_row][curr_col - 1] |= 0b0100
            API.setWall(curr_col, 15 - curr_row, 'w')
        
        if wall_right:
            walls[curr_row][curr_col] |= 0b0100
            API.setWall(curr_col, 15 - curr_row, 'e')
        
        if wall_front and curr_row != 0:
            walls[curr_row - 1][curr_col] |= 0b0010
            API.setWall(curr_col, 15 - curr_row, 'n')

    elif facing == 1:  # Se o mouse está voltado para a direita
        if wall_left and curr_row != 0:
            walls[curr_row - 1][curr_col] |= 0b0010
            API.setWall(curr_col, 15 - curr_row, 'n')
        
        if wall_right:
            walls[curr_row][curr_col] |= 0b0010
            API.setWall(curr_col, 15 - curr_row, 's')
        
        if wall_front:
            walls[curr_row][curr_col] |= 0b0100
            API.setWall(curr_col, 15 - curr_row, 'e')

    elif facing == 2:  # Se o mouse está voltado para baixo
        if wall_left:
            walls[curr_row][curr_col] |= 0b0100
            API.setWall(curr_col, 15 - curr_row, 'e')
        
        if wall_right and curr_col != 0:
            walls[curr_row][curr_col - 1] |= 0b0100
            API.setWall(curr_col, 15 - curr_row, 'w')
        
        if wall_front:
            walls[curr_row][curr_col] |= 0b0010
            API.setWall(curr_col, 15 - curr_row, 's')

    elif facing == 3:  # Se o mouse está voltado para a esquerda
        if wall_left:
            walls[curr_row][curr_col] |= 0b0010
            API.setWall(curr_col, 15 - curr_row, 's')
        
        if wall_right and curr_row != 0:
            walls[curr_row - 1][curr_col] |= 0b0010
            API.setWall(curr_col, 15 - curr_row, 'n')
        
        if wall_front and curr_col != 0:
            walls[curr_row][curr_col - 1] |= 0b0100
            API.setWall(curr_col, 15 - curr_row, 'w')

def find_move():
    """
    Função para encontrar o melhor movimento para o mouse.
    """
    global left, right, down, up, goTo

    # Verifica se o robô está em uma linha ou coluna de borda.
    # Se sim, sabemos que o robô não pode sair dos limites.
    left = path[curr_row][curr_col - 1] if curr_col != 0 else 99
    right = path[curr_row][curr_col + 1] if curr_col != 15 else 99
    up = path[curr_row - 1][curr_col] if curr_row != 0 else 99
    down = path[curr_row + 1][curr_col] if curr_row != 15 else 99

    # Verifica se há uma parede perto do robô, se houver,
    # sabemos que não podemos ir por aquele caminho.
    if walls[curr_row - 1][curr_col] & 0b0010:
        up = 99

    if walls[curr_row][curr_col - 1] & 0b0100:
        left = 99

    if walls[curr_row][curr_col] & 0b0100:
        right = 99

    if walls[curr_row][curr_col] & 0b0010:
        down = 99

    # Verificações para encontrar o menor número de movimentos
    # para o centro. Uma vez encontrado, determina a direção
    # para a qual o robô deve se orientar.

    if up <= right and up <= down and up <= left:
        goTo = 0
        return

    if left <= right and left <= down and left <= up:
        goTo = 3
        return

    if right <= left and right <= down and right <= up:
        goTo = 1
        return

    if down <= right and down <= left and down <= up:
        goTo = 2
        return
    
def turn_robot():
    """
    Função para virar o mouse para a orientação correta e atualizar a direção atual.
    """
    global facing

    if facing == 0:  # Se o robô está voltado para cima
        if goTo == 0:  # Se a direção desejada é para cima
            return  # Não precisa fazer nada
        elif goTo == 1:  # Se a direção desejada é para a direita
            API.turnRight()  # Vira para a direita
            facing = 1  # Atualiza a direção atual
            return
        elif goTo == 2:  # Se a direção desejada é para baixo
            facing = 2  # Atualiza a direção atual
            API.turnRight()  # Vira para a direita
            API.turnRight()  # Vira para a direita novamente
            return
        elif goTo == 3:  # Se a direção desejada é para a esquerda
            facing = 3  # Atualiza a direção atual
            API.turnLeft()  # Vira para a esquerda
            return
    elif facing == 1:  # Se o robô está voltado para a direita
        if goTo == 0:
            facing = 0
            API.turnLeft()
            return
        elif goTo == 1:
            return
        elif goTo == 2:
            facing = 2
            API.turnRight()
            return
        elif goTo == 3:
            facing = 3
            API.turnRight()
            API.turnRight()
            return
    elif facing == 2:  # Se o robô está voltado para baixo
        if goTo == 0:
            facing = 0
            API.turnRight()
            API.turnRight()
            return
        elif goTo == 1:
            facing = 1
            API.turnLeft()
            return
        elif goTo == 2:
            return
        elif goTo == 3:
            facing = 3
            API.turnRight()
            return
    elif facing == 3:  # Se o robô está voltado para a esquerda
        if goTo == 0:
            facing = 0
            API.turnRight()
            return
        elif goTo == 1:
            facing = 1
            API.turnRight()
            API.turnRight()
            return
        elif goTo == 2:
            facing = 2
            API.turnLeft()
            return
        elif goTo == 3:
            return
        
def move_robot():
    """
    Função para mover o robô e atualizar a posição atual.
    """
    global curr_row, curr_col

    # Verifica se não há uma parede na frente
    if wall_front:
        return

    # Atualiza a linha e a coluna atual dependendo da direção
    # em que o mouse está voltado e atualiza de acordo
    if facing == 0:  # Se o robô está voltado para cima
        curr_row -= 1
        API.moveForward()
    elif facing == 1:  # Se o robô está voltado para a direita
        curr_col += 1
        API.moveForward()
    elif facing == 2:  # Se o robô está voltado para baixo
        curr_row += 1
        API.moveForward()
    elif facing == 3:  # Se o robô está voltado para a esquerda
        curr_col -= 1
        API.moveForward()

def print_pos():
    """
    Função para depuração e determinação dos valores atuais de facing, goTo, currCol e curr_row.
    """
    text = [''] * 1  # Preparando uma lista vazia de strings
    num = curr_row
    text[0] = str(num)  # Convertendo o valor de curr_row para string
    API.setText(0, 16, text[0])  # Configurando o texto na posição (0, 16)
    
    num = curr_col
    text[0] = str(num)  # Convertendo o valor de currCol para string
    API.setText(1, 16, text[0])  # Configurando o texto na posição (1, 16)
    
    num = facing
    text[0] = str(num)  # Convertendo o valor de facing para string
    API.setText(2, 16, text[0])  # Configurando o texto na posição (2, 16)
    
    num = goTo
    text[0] = str(num)  # Convertendo o valor de goTo para string
    API.setText(3, 16, text[0])  # Configurando o texto na posição (3, 16)

def main():
    """
    Função principal para executar o código.
    """
    log("Running...")

    # Inicializa o labirinto para estar vazio
    init_path()

    # Orienta o mouse para estar voltado para a direita
    API.turnRight()

    # Preenche o labirinto inicialmente
    flood(8, 8, 0)

    # Define a posição atual
    global curr_row, curr_col
    curr_row = 15
    curr_col = 0

    # FIM DA INICIALIZAÇÃO

    # Executa enquanto o robô não estiver no centro
    while True:
        start_time = time.time()  # Inicia o cronômetro para solucionar o labirinto
        init_path()  # Limpa o array de caminho
        get_sensors()  # Verifica paredes
        update_walls()  # Atualiza o array de paredes com base nas informações
        flood(8, 8, 0)  # Atualiza o algoritmo
        print_flood_fill()  # Atualiza o simulador para exibir valores
        find_move()  # Determina o próximo movimento
        turn_robot()  # Vira o robô para a direção correta
        print_pos()  # Impressão de depuração
        move_robot()  # Move o robô para frente

        # Quebra o loop quando o labirinto é resolvido
        if curr_row == 8 and curr_col == 8:
            end_time = time.time()  # Para o cronômetro após encontrar a solução
            log("Tempo para solucionar o labirinto com o flood fill: {:.2f} segundos".format(end_time - start_time))
            break

if __name__ == "__main__":
    main()