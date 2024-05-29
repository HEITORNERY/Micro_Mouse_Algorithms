import API
import sys
x = 0
y = 0
orient = 0
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
            [10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def main():
    log("Running...")
    API.setColor(0, 0, "G")
    API.setText(0, 0, "abc")
    while True:
        frente = API.wallFront()
        esquerda = API.wallLeft()
        direita = API.wallRight()
        if not frente:
            API.moveForward()
            frente = API.wallFront()
            esquerda = API.wallLeft()
            direita = API.wallRight()
        if not esquerda:
            API.turnLeft()
            API.moveForward()
            frente = API.wallFront()
            esquerda = API.wallLeft()
            direita = API.wallRight()
        if not direita:
            API.turnRight()
            API.moveForward()
            frente = API.wallFront()
            esquerda = API.wallLeft()
            direita = API.wallRight()
        if frente and esquerda and direita == True:
            API.turnLeft()
            API.turnLeft()
            frente = API.wallFront()
            esquerda = API.wallLeft()
            direita = API.wallRight()
        if esquerda and direita == True:
            API.moveForward()
            frente = API.wallFront()
            esquerda = API.wallLeft()
            direita = API.wallRight()
        log(cells)



        # if not API.wallLeft():
        #     API.turnLeft()
        # while API.wallFront():
        #     API.turnRight()
        # API.moveForward()
if __name__ == "__main__":
    main()
