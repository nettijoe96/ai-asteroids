"""
A module that counts the number of astroid pixels on screen
"""

import argparse
import sys
import pdb
import gym
import time
gymplay = __import__("gym-play1")
from gym import wrappers, logger


shipRGB = [214,214,214]
#todo: ships bullet colors
scoreRGB = [180, 50, 50]
emptyRGB = [0, 0, 0]

class Agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    # You should modify this function
    def act(self, observation, reward, done):
        #return self.action_space.sample()
        print(self.countAsteroidPixels(observation))
        return 0
        
    def countAsteroidPixels(self, ob):
        asteroid_pixel_count = 0;
        for x in range(0, len(ob)):
            col = ob[x]
            for y in range(0, len(col)):
                pixel = col[y]
                if gymplay.isAsteroid(pixel):
                    asteroid_pixel_count += 1
        
        return asteroid_pixel_count
        

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
    
    actlist = [3, 9]
    i = 0

    while not done:
        
        action = agent.act(ob, reward, done)
        ob, reward, done, x = env.step(action)
        i+=1
        i = i % len(actlist) 
        #pdb.set_trace()
        #time.sleep(0.1)
        score += reward
        env.render()
     
    # Close the env and write monitor result info to disk
    print ("Your score: %d" % score)
    env.close()