from matplotlib import pyplot as plt
import sys
import datetime
from gym import wrappers,logger
import gym
import argparse
import random
import pickle 



class Agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    # You should modify this function
    def act(self, observation, reward, done):
        return self.action_space.sample()


def runAgent(seed, Agent):
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


    env.seed(seed)
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
        score += reward
        env.render()


    return score 


def saveResultsToFile(results):
    ts = int(datetime.datetime.now().timestamp())
    f = open(str(ts), "wb")
    pickle.dump(results, f) 
    f.close()


def xTrials(n):
    resultsDict = {}
    results = []
    agent = Agent
    for i in range(0, n):
        score = runAgent(random.randint(0, 1000), agent) 
        results += [score]
        if score not in resultsDict:
            resultsDict[str(score)] = 1
        else:
            resultsDict[str(score)] += 1 
 
    tup = (results, resultsDict)
    saveResultsToFile(tup)
    return results


def histogram(x, bins):
    plt.hist(x, bins)    



def unpickle(filename):
    f = open(filename, "rb")
    results = pickle.load(f)
    return results  

x = [1, 1, 2, 3 , 4, 4, 4, 5, 6, 10, 15, 15, 15, 20]

#histogram(x, 10)
#plt.show()

#print(xTrials(100))
results = unpickle("1571367060")
results = results[0]
resultsDict = results[1]
results += [22250 for i in range (0, 21)]
results += [4770 for i in range (0, 21)]
results += [6640 for i in range (0, 21)]
#histogram(results, 130)

fig, ax = plt.subplots()
N, bins, patches = ax.hist(results, 130, edgecolor='white', linewidth=1)


for i in range(0, len(patches)):
    print(i, patches[i])


patches[-1].set_facecolor('black')
patches[37].set_facecolor('green')
patches[26].set_facecolor('red')

plt.title("Score distribution for agents")
plt.xlabel("Score")
plt.ylabel('Frequency')
plt.rcParams.update({'font.size': 50})
plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20)
#plt.rc('font', size=100)          # controls default text sizes
plt.show()



