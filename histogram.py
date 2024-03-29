from matplotlib import pyplot as plt
import sys
import datetime
import argparse
import random
import pickle 


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
results = unpickle("hundred_trial_data")
results = results[0]
resultsDict = results[1]
results += [22250 for i in range (0, 21)]
results += [4770 for i in range (0, 21)]
results += [6640 for i in range (0, 21)]
#histogram(results, 130)

fig, ax = plt.subplots()
N, bins, patches = ax.hist(results, 130, edgecolor='white', label="Random Agent", linewidth=1)


for i in range(0, len(patches)):
    print(i, patches[i])


patches[-1].set_facecolor('black')
patches[37].set_facecolor('green')
patches[26].set_facecolor('red')

patches[-1].set_label('SpinAim Agent')
patches[37].set_label('SpinAimDodge Agent')
patches[26].set_label('Spin Agent')

ax.legend()

plt.title("Score distribution for agents")
plt.xlabel("Score")
plt.ylabel('Frequency')
plt.rcParams.update({'font.size': 50})
plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20)
#plt.rc('font', size=100)          # controls default text sizes
plt.show()



