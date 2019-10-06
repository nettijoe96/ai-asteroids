import argparse
import sys
import pdb
import gym
import time
from gym import wrappers, logger

class Agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    # You should modify this function
    def act(self, observation, reward, done):
        #return self.action_space.sample()
        return 1

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
        ob, reward, done, x = env.step(actlist[i])
        i+=1
        i = i % len(actlist) 
        #pdb.set_trace()
        #time.sleep(0.1)
        score += reward
        env.render()
     
    # Close the env and write monitor result info to disk
    print ("Your score: %d" % score)
    env.close()
