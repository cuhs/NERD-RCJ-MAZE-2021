# options file, as some settings might want to be
# changed while debugging or on different systems/computers

mazeSideLen = 10  # must be even
inputMode = 2  # 0 -> manual, 1 -> input or gen from file, 2 -> serial
recursionLimit = (mazeSideLen * mazeSideLen) + 10  # buffer of 10

displayMode = 0  # 0 no display, 1 is display
displayRate = 0  # in milliseconds, 0 for until click
displaySize = 70  # in pixels, displaySize * mazeSideLen < your screen height

port = "/dev/ttyS0"  # serial port

debug = False  # print statements

# fp -> file path
fpALL = "../BFS/"
fpKNN = fpALL + "KNN/"
fpTXT = fpALL + "IO/"
fpIMG = fpALL + "IO/"
