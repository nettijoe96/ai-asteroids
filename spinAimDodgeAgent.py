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
    spinDist = 100            # when nearest asteroid is farther than this we spin shoot
    dodgeDist = 10            # when nearest asteroid is closer than this we run

    def __init__(self, action_space):
        self.state = AgentState()

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
        if self.state.round == 0:            #there are 2 astroid-only frames in a row when game begins
            action = noop
        elif self.state.round % 4 == 0 or self.state.round % 4 == 2:
            if isShipDead(ob):         #if there is no ship, reset angle to starting.      
                self.state.resetShip()
                self.state.deadShip = True
            else:
                coor = findShip(ob)          # find ship because it can move around
                self.state.x = coor[0]
                self.state.y = coor[1]
                self.state.deadShip = False

            action = noop
            time.sleep(.1)
        elif self.state.round % 4 == 1:
            if self.state.deadShip:          #if ship is dead, we cannot make an action
                action = noop
            else:
                action = self.state.findAimDecide(ob, self.spinAimDodge)
                #printAction(action) 
            self.state.lastAction = action
        elif self.state.round % 4 == 3:      # we do a noop here to ensure no actions are missed. 
            action = noop
        else:
            raise Exception("a case is not covered in act function")


        self.state.round += 1
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
    def spinAimDodge(self, nearestA, minDist):
        ax = nearestA[0] - self.state.x  # spaceship at origin
        ay = -1 * (nearestA[1] - self.state.y)  # spaceship at origin. -1 is needed otherwise asteroid is mirrored across x axis
        if ay == 0: return fire
        if (minDist > self.spinDist):  # if closest asteroid is far away we just spinshoot
            if self.state.lastAction != clockwiseFire and self.state.lastAction != fire:
                return clockwiseFire
            else:
                return clockwise
        else:
            a_angle = self.state.findAngle(ax, ay)
            diff = self.state.findAngleDiff(self.state.angle, a_angle)
            if (math.fabs(diff) < self.state.rotation_degree):
                return fire  # fire when we have to turn less than rotation angle to get a "perfect shot"
            else:
                if diff < 0:
                    return clockwise
                elif minDist < self.dodgeDist:
                    return dodge
                else:
                    return counterclockwise



   



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
