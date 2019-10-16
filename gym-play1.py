import argparse
import sys
import pdb
import gym
import time
import math
from gym import wrappers, logger



# shipRGB = [240,128,128]
# shipRGB = [214, 214, 214]
shipRGB = [[240,128,128]]
bulletCollors = [[117, 181, 239]]

#todo: ships bullet colors
scoreRGB1 = [184, 50, 50]
scoreRGB2 = [180, 50, 50]
scoreColors = list()
scoreColors.append(scoreRGB1)
scoreColors.append(scoreRGB2)
emptyRGB = [0, 0, 0]

class Agent(object):
    starting_x = 85           # starting (x,y) coor of center of spaceship
    starting_y = 105          # starting (x,y) coor of center of spaceship
    starting_angle = 90       # starting angle from vertical x-axis
    rotation_degree = 22.5    # each rotation action is 90 degrees divded by 4
    lastAction = 0
    shipScreen = False
    round = 0
    prevNearestA = None
    prevMinDist = None
    

    far = 100
    fire = 1
    clockwise = 3
    counterclockwise = 4
    clockwiseFire = 9
    fireList = [1, 9, 10]

    def __init__(self, action_space):
        self.action_space = action_space
        self.x = self.starting_x
        self.y = self.starting_y
        self.angle = self.starting_angle
        self.stepsAwayFromRecharged = 0


    # def act(self, ob, reward, done):
    #     #if self.round % 3 == 0 or self.round % 3 == 1:
    #     if self.round % 4 == 0:
    #         decision = 0
    #     elif self.round % 4 == 1:
    #         decision = 3
    #         self.adjustAngle(-1 * self.rotation_degree)
    #     elif self.round % 4 == 2:
    #         decision = 0
    #     elif self.round % 4 == 3:
    #         decision = 0
    #
    #     self.round += 1
    #     time.sleep(1)
    #     print(self.angle)
    #     return decision


    # You should modify this function
    def act(self, observation, reward, done):
        #print("is empty:", self.isEmpty(observation))
        #print(self.angle)
        # nAst = aNum(ob)
        #print("asteroids", nAst)
        #print("ship angle", self.angle)
        if self.round % 4 == 0: #skip first round
            decision = 0
            time.sleep(.1)
        elif self.round % 4 == 1:
            decision = self.findAimDecide(observation)

        elif self.round % 4 == 2:
            decision = 0

        elif self.round % 4 == 3:   #TODO: have an action here that is NOT the same as in 1
            decision = self.findAimDecide(observation)
             
        if decision in self.fireList:
            self.noCharge()
        else: 
            self.charge() 

        self.round += 1
        self.lastAction = decision
        return decision


    def findAimDecide(self, ob):
        nearestA, minDist = self.findNearestAsteroid(ob)
        if nearestA[0] != None:
            decision = self.makeDecision(nearestA, minDist)
            self.prevMinDist = minDist
            self.prevNearestA = nearestA
        else:
            decision = self.makeDecision(self.prevNearestA, self.prevMinDist)
       
        if decision == self.lastAction:
            decision = 0

        return decision 


    def spaceShipLocation(ob):
        sumx = 0
        sumy = 0
        n = 0
        for y in range(0, len(ob[0])):
            for x in range(0, len(ob[1])):
                if isSpaceShip(ob[y][x]):  #TODO: get rid of same color bullet
                    sumy += 1
                    sumx += 1
                    n += 1
        return (sumx/n,sumy/n)                




    def isEmpty(self, ob):
        for y in range(0, len(ob[0])):
            for x in range(0, len(ob[1])):
                if ob[y][x][0] != 0 or ob[y][x][1] != 0 or ob[y][x][2] != 0:
                    return False
        return True

    def isRecharged(self):
        if self.stepsAwayFromRecharged == 0:
            return True
        else: 
            return False

   
    def noCharge(self):
        self.stepsAwayFromRecharged = 2



    def charge(self):
        if self.stepsAwayFromRecharged > 0:
            self.stepsAwayFromRecharged -= 1




    def makeDecision(self, nearestA, minDist):
        ax = nearestA[0] - self.x  # spaceship at origin
        ay = nearestA[1] - self.y  # spaceship at origin
        if(ay == 0): return self.fire  #TODO: we have to deal with ay = 0 correctly
        if(minDist > self.far):           #if closest asteroid is far away we just spinshoot
            if self.isRecharged():
                self.adjustAngle(-1 * self.rotation_degree)
                return self.clockwiseFire
            else:
                self.adjustAngle(-1 * self.rotation_degree)
                return self.clockwise
        else:
            a_angle = findAngle(ax, ay)
            print("angle:", a_angle)
    
            if (math.fabs((a_angle - self.angle)) < self.rotation_degree):
                if self.isRecharged():
                    return self.fire  # fire when we have to turn less than rotation angle to get a "perfect shot"
                else:
                    return 0
            else:
                if ((self.angle - a_angle) < 0):
                    self.adjustAngle(1 * self.rotation_degree)
            #        print("counterclockwise")
                    return self.counterclockwise
                else:
                    self.adjustAngle(-1 * self.rotation_degree)
            #        print("clockwise")
                    return self.clockwise


    def adjustAngle(self, adjustment):
        angle = self.angle
        angle += adjustment
        if angle < 0:
            angle += 360
        if angle > 360:
            angle = angle % 360
        self.angle = angle

    
    def findNearestAsteroid(self, ob):
        minDist = triangularDistance(160, 210)
        ax = None
        ay = None

        for y in range(0, len(ob[0])):
            rowMin = None
            for x in range(0, len(ob[1])):
                pixel = ob[y][x]
                if isAsteroid(pixel):
                    dist = triangularDistance(self.x-x, self.y-y) 
                    if dist < minDist:
                        minDist = dist
                        ax = x
                        ay = y 
                    
                    #an optimization where if the dist begins to rise on the row, we break
                    if rowMin == None or dist < rowMin:
                        rowMin = dist
                    elif rowMin == dist: 
                        pass
                    else: 
                        break 
                   
        return (ax, ay), minDist


def findAngle(ax, ay):
    print("ax, ay", ax, ay)
    if (ax > 0 and ay > 0):  # the first quadrant
        a_angle = (180 * math.atan(ay/ax)) / math.pi
    elif (ax < 0 and ay > 0):
        a_angle = ((-180 * math.atan(ax/ay)) / math.pi ) + 90
    elif (ax < 0 and ay < 0):
        a_angle = ((180 * math.atan(ay/ax)) / math.pi ) + 180
    elif (ax > 0 and ay < 0):
        a_angle = ((-180 * math.atan(ax/ay)) / math.pi ) + 270
    elif (ax > 0 and ay == 0):
        a_angle = 0
    elif (ax == 0 and ay > 0):
        a_angle = 90
    elif (ax < 0 and ay == 0):
        a_angle = 180
    elif (ax == 0 and ay < 0):
        a_angle = 270
    else:
        raise Exception("bug in findAngle function")

    return a_angle


def triangularDistance(x_distance, y_distance):
    return math.sqrt(x_distance**2 + y_distance**2)


def isAsteroid(pixel):
    return (not containsRGB(shipRGB, pixel)) and (not containsRGB(scoreColors, pixel)) and (not compareRGB(emptyRGB, pixel)) #TODO: add blue bullet



def isSpaceShip(pixel):
    return containsRGB(pixel, shipRGB)   #includes the red bullet because same color as spaceship


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

## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    #parser.add_argument('--env_id', nargs='?', default='Asteroids-v0', help='Select the environment to run')
    parser.add_argument('--env_id', nargs='?', default='AsteroidsNoFrameskip-v4', help='Select the environment to run')
    #parser.add_argument('--env_id', nargs='?', default='AsteroidsNoFrameskip-v0', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = 'random-agent-results'


    env.seed(50)
    agent = Agent(env.action_space)

    episode_count = 100
    reward = 0
    done = False
    score = 0
    special_data = {}
    special_data['ale.lives'] = 3
    ob = env.reset()
    #l = [3,9]
    #i = 0
    while not done:
        action = agent.act(ob, reward, done)
        ob, reward, done, x = env.step(action)
        #ob, reward, done, x = env.step(l[i])
        #i = (i + 1) % len(l)
        #pdb.set_trace()
        #time.sleep(2)
        score += reward
        env.render()
     
    # Close the env and write monitor result info to disk
    print("Your score: %d" % score)
    env.close()
           
