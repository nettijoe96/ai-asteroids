import math


#colors
shipRGB = [[240,128,128]]
bulletColors = [[117, 181, 239]]
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



"""
the internal state for sophisticated agents
"""


class AgentState:
    starting_x = 85  # starting (x,y) coor of center of spaceship
    starting_y = 105  # starting (x,y) coor of center of spaceship
    starting_angle = 90  # starting angle from vertical x-axis
    rotation_degree = 22.5  # each rotation action is 90 degrees divded by 4
    lastAction = 0
    shipScreen = False
    round = 0
    prevNearestA = None
    prevMinDist = None
    deadShip = False

    def __init__(self):
        self.resetShip()

    """
    * when we start and after ship dies we reset it to its initial position
    """

    def resetShip(self):
        self.x = self.starting_x
        self.y = self.starting_y
        self.angle = self.starting_angle

    """
    * decide on an action finding the nearest asteroid
    * 
    * @param ob: observations
    * @return action
    """

    def findAimDecide(self, ob, func):
        nearestA, minDist = self.findNearestAsteroid(self.x, self.y, ob)
        if nearestA[0] != None:
            action = func(nearestA, minDist)
            self.prevMinDist = minDist
            self.prevNearestA = nearestA
        else:
            action = func(self.prevNearestA, self.prevMinDist)

        if action == self.lastAction:
            action = noop
        elif action == clockwise or action == clockwiseFire:
            self.angle = self.adjustAngle(self.angle, -1 * self.rotation_degree)
        elif action == counterclockwise or action == counterclockwiseFire:
            self.angle = self.adjustAngle(self.angle, self.rotation_degree)

        return action

    """
    * adjust angle
    * 
    * @param ob: observations
    * @return new angle
    """

    def adjustAngle(self, angle, adjustment):
        angle += adjustment
        if angle < 0:
            angle += 360
        elif angle >= 360:
            angle = angle % 360

        return angle

    """
    * find coordinate of nearest asteroid
    * 
    * @param ob: observations
    * @return action
    """

    def findNearestAsteroid(self, shipx, shipy, ob):
        minDist = triangularDistance(160, 210)
        ax = None
        ay = None

        for y in range(underBanner, len(ob[0])):  # we start searching below score banner
            rowMin = None
            for x in range(0, len(ob[1])):
                pixel = ob[y][x]
                if isAsteroid(pixel):
                    dist = triangularDistance(shipx - x, shipy - y)
                    if dist < minDist:
                        minDist = dist
                        ax = x
                        ay = y

                        # an optimization where if the dist begins to rise on the row, we break
                    if rowMin == None or dist < rowMin:
                        rowMin = dist
                    elif rowMin == dist:
                        pass
                    else:
                        break

        return (ax, ay), minDist

    """
    find difference between the ship angle and asteroid angle. 

    :param ship: ship angle
    :param ast: asteroid angle
    :return angle between ship and asteroid. negative is clockwise turn. positive is counterclockwise turn
    """

    def findAngleDiff(self, ship, ast):
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

    """
    find angle from pos x axis and point (ax, ay)

    :param ax: x
    :param ay: y
    :return angle 
    """

    def findAngle(self, ax, ay):
        if (ax > 0 and ay > 0):  # the first quadrant
            a_angle = (180 * math.atan(ay / ax)) / math.pi
        elif (ax < 0 and ay > 0):
            a_angle = ((-180 * math.atan(ax / ay)) / math.pi) + 90
        elif (ax < 0 and ay < 0):
            a_angle = ((180 * math.atan(ay / ax)) / math.pi) + 180
        elif (ax > 0 and ay < 0):
            a_angle = ((-180 * math.atan(ax / ay)) / math.pi) + 270
        elif (ax > 0 and ay == 0):
            a_angle = 0
        elif (ax == 0 and ay > 0):
            a_angle = 90
        elif (ax < 0 and ay == 0):
            a_angle = 180
        elif (ax == 0 and ay < 0):
            a_angle = 270
        elif (ax == 0 and ay == 0):
            a_angle = 0
        else:
            raise Exception("bug in findAngle function")

        return a_angle




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
        x = round(sumx / n)
        y = round(sumy / n)
        return (x, y)



def triangularDistance(x_distance, y_distance):
    return math.sqrt((x_distance**2) + (y_distance**2))


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
