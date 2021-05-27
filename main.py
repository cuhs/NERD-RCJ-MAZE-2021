import BFS
import display
import numpy as np
import time
import mazeToText
from BFS import util
from util import packet
from util import options
import everythingDetect

BFS.init()
print("BFS START")

# display setup
display.imgSetup()

# packet setup
if options.inputMode == 1:
    mazeToText.generateMaze()
    ret = packet.setupInput(options.inputMode)
    if ret is not None:  # maze in file is generated maze, values must be stored
        packet.inputData = np.zeros((util.mazeSize * util.mazeSize, 5), dtype=np.int8)
        for x in range(util.mazeSize * util.mazeSize):
            cTile = ret[x]
            for y in range(4):
                packet.inputData[x][y] = cTile[y]
                packet.inputData[x][4] = -1
else:
    packet.setupInput(options.inputMode)

print("\nrunning...")

# set start tile walls
util.maze[util.tile][util.visited] = 1
util.setWalls()
print("here")

# time calculation
ot = 0
start = time.time()

# calculate next tile
nextTile = BFS.nextTile(util.tile)

while nextTile is not None:
    if options.debug is True:
        print("\tCurrent Tile:\t" + str(util.tile) + "\n\tNext Tile:\t" + str(nextTile))
    # calculate path to target tile
    BFS.pathToTile(util.tile, nextTile)
    if options.debug is True:
        print("\tTiles To Target Tile: " + str(len(util.path)))

    # display the maze
    if options.displayMode == 1:
        display.show(nextTile, util.maze, options.displayRate)

    print(util.path)
    tPath = util.path
    while util.path:
        # calculate driving instructions from path to next tile
        if options.debug is True:
            print("\tPath: " + str(util.path))
        util.direction = BFS.turnToTile(util.path.pop(), util.direction)
        util.tile = util.forwardTile(util.tile)

    # print out path to only the next tile
    motorMessage = 'm'
    if options.inputMode == 2:
        packet.ser.write(bytes(motorMessage.encode("ascii", "ignore"))) # send 'm' to do motor control
    packet.sendData(options.inputMode, util.pathLen)
    if options.debug is True:
        print("\tPath To Tile: " + str(packet.sData[util.pathLen:]))
        print()
    util.pathLen = len(packet.sData)
    
    # victim checking
    startMessage = 'v'
    send_message1 = ""
    send_message2 = ""
    
    if options.inputMode == 2:
        
        print("victim started")
            
        msg = None
        while not packet.ser.inWaiting():
            packet.time.sleep(0.01)
            everythingDetect.PIcap.read()
            everythingDetect.USBcap.read()
        
        print("msg received")
        
        msg = packet.ser.read()
        if msg == b'd':
            print("b, movement over")
        
        if util.maze[util.tile][util.visited] != 2:
            print("doing victim")
            for x in range(3):
                right,packageR,left,packageL = everythingDetect.detectAll()
            print("HERE:",left,packageL,right,packageR)

            if(left is True or right is True):
                #print("START MESSAGE")
                util.maze[util.tile][util.visited] = 2
                packet.ser.write(bytes(startMessage.encode("ascii", "ignore")))

                if (left is True):
                    send_message1 = "L" + str(packageL)
                    print(send_message1)
                    packet.ser.write(bytes(send_message1.encode("ascii", "ignore")))
            
                if (right is True):
                    send_message2 = "R" + str(packageR)
                    print(send_message2)
                    packet.ser.write(bytes(send_message2.encode("ascii", "ignore")))
                    

    print("victim ended")
    # set tile new tile to visited, clear parent array
    util.maze[util.tile][util.visited] = 1
    util.parent.fill(-1)

    # get sensor/wall values and calculate next tile
    util.setWalls()

    # calculate next tile
    nextTile = BFS.nextTile(util.tile)

    if options.debug is True:
        print("BFS START")

# print out entire path the robot took traversing the maze and how long the algorithm took
end = time.time()
print("\nTotal Path: " + str(packet.sData) + "\nBFS Done! All tiles visited in: " + format((end-start)*1000, '.4f') + "ms ")
display.show(-1, util.maze, 0)
packet.s.close()
packet.r.close()
