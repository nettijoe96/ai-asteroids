"""
*  Spin-Aim-Dodge agent for playing asteroids
*
*  Authors:
*  Joe Netti    
*  Eric Tiano   
"""




from common import *
import argparse
import sys
import pdb
import gym
import time
from gym import wrappers, logger



class Agent(object):
    starting_x = 85           # starting (x,y) coor of center of spaceship
    starting_y = 105          # starting (x,y) coor of center of spaceship
    starting_angle = 90       # starting angle from vertical x-axis
    rotation_degree = 22.5    # each rotation action is 90 degrees divded by 4
    lastAction = noop         # last action
    round = 0                 # we need to know what round it is for determining the right frame
    prevNearestA = None       
    prevMinDist = None
    deadShip = False

    spinDist = 100            # when nearest asteroid is farther than this we spin shoot
    dodgeDist = 10            # when nearest asteroid is closer than this we run

    def __init__(self, action_space):
        self.resetShip()


    """
    * main function for agent
    * first round we skip. After that we make 1 action every 4 rounds. 
    * 
    * @param ob observation
    * @param reward
    * @param done
    * @param action
    """
    def act(self, ob, reward, done):
        if self.round == 0:            #there are 2 astroid-only frames in a row when game begins
            action = noop
        elif self.round % 4 == 0 or self.round % 4 == 2:      
            if isShipDead(ob):         #if there is no ship, reset angle to starting.      
                self.resetShip()
                self.deadShip = True
            else:
                coor = findShip(ob)
                self.x = coor[0]
                self.y = coor[1]
                self.deadShip = False

            action = noop
            time.sleep(.1)
        elif self.round % 4 == 1:
            if self.deadShip:          #if ship is dead, we cannot make an action
                action = noop
            else:
                action = self.findAimDecide(ob)
                #printAction(action) 
            self.lastAction = action
        elif self.round % 4 == 3:      # we do a noop here to ensure no actions are missed. 
            action = noop
        else:
            raise Exception("a case is not covered in act function")


        self.round += 1
        return action



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
    def findAimDecide(self, ob):
        nearestA, minDist = self.findNearestAsteroid(ob)
        if nearestA[0] != None:
            action = self.makeDecision(nearestA, minDist)
            self.prevMinDist = minDist
            self.prevNearestA = nearestA
        else:
            action = self.makeDecision(self.prevNearestA, self.prevMinDist)
       
        if action == self.lastAction:
            action = noop
        elif action == clockwise or action == clockwiseFire:
            self.adjustAngle(-1 * self.rotation_degree)
        elif action == counterclockwise or action == counterclockwiseFire:
            self.adjustAngle(self.rotation_degree)

        return action 


    """
    * make decision
    * there are 3 cases: 
    *     1. nearest asteroid is far away: we spinshoot
    *     2. nearest asteroid is normal range: we aim and shoot
    *     3. nearest asteroid is close: we run away
    * 
    * @param nearestA: coordinates of nearest asteroid
    * @param minDist: the distance that asteroid is away from spaceship
    * @return action
    """
    def makeDecision(self, nearestA, minDist):
        ax = nearestA[0] - self.x  # spaceship at origin
        ay = -1 * (nearestA[1] - self.y)  # spaceship at origin
        if(minDist > self.spinDist):           #if closest asteroid is far away we just spinshoot
            if self.lastAction != clockwiseFire and self.lastAction != fire:
                return clockwiseFire
            else:
                return clockwise
        else:
            a_angle = findAngle(ax, ay)
            diff = findAngleDiff(self.angle, a_angle)
            if (math.fabs(diff) < self.rotation_degree):
                    return fire  # fire when we have to turn less than rotation angle to get a "perfect shot"
            elif minDist < self.dodgeDist:
                return dodge
            else:
                if diff < 0:
                    return clockwise
                else:
                    return counterclockwise



    """
    * decide on an action finding the nearest asteroid
    * 
    * @param ob: observations
    * @return action
    """
    def adjustAngle(self, adjustment):
        angle = self.angle
        angle += adjustment
        if angle < 0:
            angle += 360
        elif angle >= 360:
            angle = angle % 360

        self.angle = angle

   

    """
    * find coordinate of nearest asteroid
    * 
    * @param ob: observations
    * @return action
    """
    def findNearestAsteroid(self, ob):
        minDist = triangularDistance(160, 210)
        ax = None
        ay = None

        for y in range(underBanner, len(ob[0])):   # we start searching below score banner
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




## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    #parser.add_argument('--env_id', nargs='?', default='Asteroids-v0', help='Select the environment to run')
    parser.add_argument('--env_id', nargs='?', default='AsteroidsNoFrameskip-v4', help='Select the environment to run')  # We choose to use no frameskip rom. The other rom doesn't work
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


    env.seed(1)
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
        #time.sleep(2)
        score += reward
        env.render()
     
    # Close the env and write monitor result info to disk
    print("Your score: %d" % score)
    env.close()
           
