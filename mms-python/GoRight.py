import API
import sys

while True:
    if not API.wallRight():
        API.turnRight()
    else:
        while API.wallFront():
            API.turnLeft()
    API.moveForward()