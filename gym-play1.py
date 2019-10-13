import argparse
import sys
import pdb
import gym
import time
import math
from gym import wrappers, logger



shipRGB = [214,214,214]
#todo: ships bullet colors
scoreRGB = [180, 50, 50]
emptyRGB = [0, 0, 0]

class Agent(object):
    starting_x = 56           # starting (x,y) coor of center of spaceship
    starting_y = 155          # starting (x,y) coor of center of spaceship
    starting_angle = 90       # starting angle from vertical x-axis
    rotation_degree = 90/4    # each rotation action is 90 degrees divded by 4
    lastAction = 0
 
    fire = 1
    clockwise = 3
    counterclockwise = 4
    clockwiseFire = 9


    def __init__(self, action_space):
        self.action_space = action_space
        self.x = self.starting_x
        self.y = self.starting_y
        self.angle = self.starting_angle
        self.far = 30

    # You should modify this function
    def act(self, observation, reward, done):
        nearestA, minDist = self.findNearestAsteroid(observation)
        ax = nearestA[0] - self.x  # spaceship at origin
        print("ax", ax)
        ay = nearestA[1] - self.y  # spaceship at origin
        print("ay", ay)
        if(ay == 0): return self.fire  #TODO: we have to deal with ay = 0 correctly
        a_angle = (180 * math.atan(ax/ay)) / math.pi 
        dist = math.sqrt(ax**2 + ay**2)
        print("dist", dist)
        if(dist > self.far):           #if closest asteroid is far away we just spinshoot
            a = self.lastAction
            if a == self.clockwiseFire or a == self.fire:
                a = self.clockwise
            else:
                a = self.clockwiseFire
            self.lastAction = a
            return a
        else:
            if (ax > 0 and ay > 0):  # the first quadrant
                print("first")
                pass
            elif (ax < 0 and ay > 0):
                print("second")
                a_angle = (a_angle * -1) + 90
            elif (ax < 0 and ay < 0):
                print("third")
                a_angle = a_angle + 180
            elif (ax > 0 and ay < 0):
                print("fourth")
                a_angle = (a_angle * -1) + 270
    
            print("ast angle", a_angle)
            print("ship angle", self.angle)
            if (math.fabs((a_angle - self.angle)) < self.rotation_degree):
                print("fire")
                if self.lastAction == self.fire:
                    self.lastAction = 0
                    return 0
                self.lastAction = self.fire
                return self.fire  # fire when we have to turn less than rotation angle to get a "perfect shot"
            else:
                if ((self.angle - a_angle) < 0):
                    # move counterclockwise
                    print("counterclockwise")
                    self.angle += self.rotation_degree
                    self.lastAction = self.counterclockwise
                    return self.counterclockwise
                else:
                    print("clockwise")
                    self.angle -= self.rotation_degree
                    self.lastAction = self.clockwise
                    return self.clockwise

   
    def findNearestAsteroid(self, ob):
        minDist = triangularDistance(160, 210)
        shipx = self.x
        shipy = self.y
        ax = None
        ay = None

        for y in range(0, len(ob[0])):
            for x in range(0, len(ob[1])):
                pixel = ob[y][x]
                if isAsteroid(pixel):
                    dist = triangularDistance(self.x-x, self.y-y) 
                    if dist < minDist:
                       minDist = dist
                       ax = x
                       ay = y 
        return (ax, ay), minDist




    # return angle from x-axis of the ship, and return (x,y) of either the center or the node
    def findShip(self, ob):
       for x in range(0, len(ob)):
           x = ob[x]
           for y in range(0, len(x)):
               pixel = x[y]
               if compageRGB(shipRBG, pixel):
                   pass




def triangularDistance(x_distance, y_distance):
    return math.sqrt(x_distance**2 + y_distance**2)


def isAsteroid(pixel):
    return (not compareRGB(shipRGB, pixel)) and (not compareRGB(scoreRGB, pixel)) and (not compareRGB(emptyRGB, pixel)) #TODO: add blue bullet 



def compareRGB(pixel1, pixel2):
    return pixel1[0] == pixel2[0] and pixel1[1] == pixel2[1] and pixel1[2] == pixel2[2]


## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Asteroids-v0', help='Select the environment to run')
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
    print(env.action_space)
    agent = Agent(env.action_space)

    episode_count = 100
    reward = 0
    done = False
    score = 0
    special_data = {}
    special_data['ale.lives'] = 3
    ob = env.reset()
    while not done:
        
        action = agent.act(ob, reward, done)
        ob, reward, done, x = env.step(action)
        #pdb.set_trace()
        #time.sleep(.5)
        score += reward
        env.render()
     
    # Close the env and write monitor result info to disk
    print("Your score: %d" % score)
    env.close()
