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

 
    fire = 1
    thrust = 2
    clockwise = 3
    counterclockwise = 4


    def __init__(self, action_space):
        self.action_space = action_space
        self.x = self.starting_x
        self.y = self.starting_y
        self.angle = self.starting_angle

    # You should modify this function
    def act(self, observation, reward, done):
        nearestA = self.findNearestAsteroid(observation)
        ax = nearestA[0] - self.x  # spaceship at origin
        print("ax", ax)
        ay = nearestA[1] - self.y  # spaceship at origin
        print("ay", ay)
        if(ay == 0): return self.fire  #TODO: we have to deal with ay = 0 correctly
        a_angle = (180 * math.atan(ax/ay)) / math.pi 

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
        
  
        if(triangulardDistance(ax, ay) > 5): 
          shootNearestAstroid()
        else:
          
  
    """
    Returns the x and y coordinates of the nearest edge of an asteroid 
    (where diagonal traversal of a pixel is equal to cardinal traversal 
    of a pixel)
    """
    def findNearestAsteroid(self, ob):   #if there are no asteroids this will stall. run the while for dist from center + center to diagonal
        sideL = 1
        x = self.x
        y = self.y
        while True:
            isA = False
            
            tempx = x
            tempy = y
            for i in range(0, sideL):   #upper left corner; move right
                tempx += 1
                if tempx > 159 or tempy > 209 or tempx < 0 or tempy < 0:
                    break
                isA = isAsteroid(ob[tempy][tempx])
                if isA:
                    return (tempx, tempy)
         
            tempx = x
            tempy = y
            for i in range(0, sideL):   #upper left corner; move down
                tempy += 1
                if tempx > 159 or tempy > 209 or tempx < 0 or tempy < 0:
                    break
                isA = isAsteroid(ob[tempy][tempx])
                if isA:
                    return (tempx, tempy)

            tempx = x + sideL
            tempy = y + sideL
      
            for i in range(0, sideL):   #lower right corner; move left
                tempx -= 1
                if tempx > 159 or tempy > 209 or tempx < 0 or tempy < 0:
                    break
                isA = isAsteroid(ob[tempy][tempx])
                if isA:
                    return (tempx, tempy)
           
            tempx = x + sideL
            tempy = y + sideL
            for i in range(0, sideL):   #lower right corner; move up
                tempy -= 1
                if tempx > 159 or tempy > 209 or tempx < 0 or tempy < 0:
                    break
                isA = isAsteroid(ob[tempy][tempx])
                if isA:
                    return (tempx, tempy)
             
            if x > 0:
                x -= 1
            if y > 0:
                y -= 1

            sideL += 2
 


    # return angle from x-axis of the ship, and return (x,y) of either the center or the node
    def findShip(self, ob):
       for x in range(0, len(ob)):
           x = ob[x]
           for y in range(0, len(x)):
               pixel = x[y]
               if compageRGB(shipRBG, pixel):
                   pass
                   
    """
    If the ship is aligned with the astroid, fire. If the ship is not 
    aligned with astroid, rotate the ship towards the astroid.
    """
    def shootNearestAstroid():
      if (math.fabs((a_angle - self.angle)) < self.rotation_degree):
            return self.fire  # fire when we have to turn less than rotation angle to get a "perfect shot"
        else:
            if ((self.angle - a_angle) < 0):
                # move counterclockwise
                self.angle += self.rotation_degree
                return self.counterclockwise
            else:
                self.angle -= self.rotation_degree
                return self.clockwise
                
    def escape():
      if(a_angle <= 90):
        shootNearestAstroid()
      else:
        return self.thrust
      

def isAsteroid(pixel):
    return (not compareRGB(shipRGB, pixel)) and (not compareRGB(scoreRGB, pixel)) and (not compareRGB(emptyRGB, pixel)) #TODO: add blue bullet 



def compareRGB(pixel1, pixel2):
    return pixel1[0] == pixel2[0] and pixel1[1] == pixel2[1] and pixel1[2] == pixel2[2]
    

def triangulardDistance(x_distance, y_distance)
    return math.sqrt(x_distance**2 + y_distance**2)


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
