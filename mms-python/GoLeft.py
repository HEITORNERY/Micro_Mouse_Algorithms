import API
import sys

while True:
    if not API.wallLeft():
        API.turnLeft()
    else:
        while API.wallFront():
            API.turnRight()
    API.moveForward()