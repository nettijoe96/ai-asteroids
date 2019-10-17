import math


#colors
shipRGB = [[240,128,128]]
bulletCollors = [[117, 181, 239]]
scoreRGB1 = [184, 50, 50]
scoreRGB2 = [180, 50, 50]
underBanner = 15
scoreColors = list()
scoreColors.append(scoreRGB1)
scoreColors.append(scoreRGB2)
emptyRGB = [0, 0, 0]


#actions
noop = 0
fire = 1
dodge = 2
clockwise = 3
counterclockwise = 4
clockwiseFire = 9
counterclockwiseFire = 10
fireList = [fire, clockwiseFire, counterclockwiseFire]



def findAngleDiff(ship, ast):
    if ship > ast:
        clockwiseAngle = ship - ast
        counterclockwiseAngle = 360 - clockwiseAngle
    elif ship < ast:
        counterclockwiseAngle = ast - ship
        clockwiseAngle = 360 - counterclockwiseAngle
    else:
        counterclockwiseAngle = 0
        clockwiseAngle = 0

    if clockwiseAngle < counterclockwiseAngle:
        return -1 * clockwiseAngle
    elif clockwiseAngle > counterclockwiseAngle:
        return counterclockwiseAngle
    elif clockwiseAngle == counterclockwiseAngle:
        return 0


def testAngle():
    s = 45
    a = 300
    print(findAngleDiff(s, a))  # supposed to be -105
    s = 180
    a = 180
    print(findAngleDiff(s, a))  # 0
    s = 300
    a = 45
    print(findAngleDiff(s, a))  # 105
    s = 300
    a = 270
    print(findAngleDiff(s, a))  # -30
    s = 0
    a = 90
    print(findAngleDiff(s, a))  # 90




def printAction(action):
    if action == noop:
        print("noop")
    elif action == fire:
        print("fire")
    elif action == clockwise:
        print("clockwise")
    elif action == clockwiseFire:
        print("clockwiseFire")
    elif action == counterclockwise:
        print("counterclockwise")



def isShipDead(ob):
    if findShip(ob) == (None, None):
        return True
    else:
        return False



def findShip(ob):
    sumx = 0
    sumy = 0
    n = 0
    for y in range(15, len(ob[0])):
        for x in range(0, len(ob[1])):
            if isSpaceShip(ob[y][x]):
                sumy += y
                sumx += x
                n += 1
    if n <= 2:  # died
        return (None, None)
    else:
        x = round(sumx /n)
        y = round(sumy /n)
        return (x, y)


def findAngle(ax, ay):
    if (ax > 0 and ay > 0):  # the first quadrant
        a_angle = (180 * math.atan(ay /ax)) / math.pi
    elif (ax < 0 and ay > 0):
        a_angle = ((-180 * math.atan(ax /ay)) / math.pi ) + 90
    elif (ax < 0 and ay < 0):
        a_angle = ((180 * math.atan(ay /ax)) / math.pi ) + 180
    elif (ax > 0 and ay < 0):
        a_angle = ((-180 * math.atan(ax /ay)) / math.pi ) + 270
    elif (ax > 0 and ay == 0):
        a_angle = 0
    elif (ax == 0 and ay > 0):
        a_angle = 90
    elif (ax < 0 and ay == 0):
        a_angle = 180
    elif (ax == 0 and ay < 0):
        a_angle = 270
    elif (ax == 0 and ay == 0):
        print("NOTHING!!!!!!!!!\n\n")
        a_angle = 0
    else:
        raise Exception("bug in findAngle function")

    return a_angle


def triangularDistance(x_distance, y_distance):
    return math.sqrt((x_distance*2) + (y_distance**2))


def isAsteroid(pixel):
    # return (not containsRGB(shipRGB, pixel)) and (not containsRGB(scoreColors, pixel)) and (not compareRGB(emptyRGB, pixel))
    return (not containsRGB(shipRGB, pixel)) and (not compareRGB(emptyRGB, pixel))



def isSpaceShip(pixel):
    return containsRGB(shipRGB, pixel)  # includes the red bullet because same color as spaceship


def compareRGB(pixel1, pixel2):
    return pixel1[0] == pixel2[0] and pixel1[1] == pixel2[1] and pixel1[2] == pixel2[2]


def containsRGB(pixel_list, pixel1):
    for pixel in pixel_list:
        if(compareRGB(pixel1, pixel)):
            return True

    return False


def aNum(ob):
    aCount = 0
    lst = []
    for y in range(0, len(ob[0])):
        for x in range(0, len(ob[1])):
            if isAsteroid(ob[y][x]):
                aCount += 1
                lst += [(x, y, ob[y][x])]
    if aCount == 2:
        print(lst)
    return aCount
