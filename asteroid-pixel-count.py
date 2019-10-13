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

class Agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space
        self.frame_count = 0

    # You should modify this function
    def act(self, observation, reward, done):
        self.frame_count += 1
        
        count, pixels, locations = self.countAsteroidPixels(observation)
        
        self.save_count_to_file(count, pixels, locations)
        
        return 0
        
    def countAsteroidPixels(self, ob):
        asteroid_pixel_count = 0;
        asteroid_pixels = list()
        asteroid_pixel_locations = list()
        for x in range(0, len(ob)):
            col = ob[x]
            for y in range(0, len(col)):
                pixel = col[y]
                if gymplay.isAsteroid(pixel):
                    asteroid_pixel_count += 1
                    asteroid_pixels.append(pixel)
                    asteroid_pixel_locations.append((x,y))
        
        return asteroid_pixel_count, asteroid_pixels, asteroid_pixel_locations
        
    def save_count_to_file(self, count):
        with open("frame_pixel_count.txt", "a") as count_file:
            count_file.write("frame: {:3} count: {}\n".format(self.frame_count, count))
            
    def save_count_to_file(self, count, pixels, locations):
        
        full_pixel_list = list()
        
        for i in range(0,len(locations)):
            x = locations[i][0]
            y = locations[i][1]
            r = pixels[i][0]
            g = pixels[i][1]
            b = pixels[i][2]
            
            current_pixel = Pixel(x,y,r,g,b)
            
            full_pixel_list.append(current_pixel)
        
        with open("frame_pixel_count.txt", "a") as count_file:
            count_file.write("frame: {:3} count: {}\n".format(self.frame_count, count))
            for pixel in full_pixel_list:
                count_file.write("\t{}\n".format(pixel.str()))
      
      
class Pixel:
    
    def __init__(self, x, y, r, g, b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g 
        self.b = b
        
    def str(self):
        return "Location: ({:3},{:3})\tRGB: ({:3},{:3},{:3})".format(self.x,self.y,self.r,self.g,self.b)


## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='AsteroidsNoFrameskip-v4', help='Select the environment to run')
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