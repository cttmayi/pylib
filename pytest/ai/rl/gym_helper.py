
from pylib.basic.pp import *


import gymnasium as gym

import termios
import tty
import sys
import select

import numpy as np

from collections import deque


class AgentWrapper:
    def __init__(self):
        pass

    def set_env(self, env):
        self.env:gym.Env = env.env
        self.init(env.id_)


    def init(self):
        pass

    def store_transition(self, step, prev_observation, action, reward, observation):
        return reward

    def learn(self):
        pass

    def action(self, observation):
        return self.env.action_space.sample()
    
    def save(self, filename):
        pass


class Env:
    def __init__(self, id_, agent:AgentWrapper=None):
        self.id_ = id_
        self.env_t = gym.make(id_)
        self.env_h = gym.make(id_, render_mode="human")
        self.env = self.env_t
        self.agent:AgentWrapper = agent
        if agent is None:
            self.agent = AgentWrapper()
        self.agent.set_env(self)

        self.log = False


        self.tty_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, tty_settings)


    def _getch(self):
        ch = None
        if select.select([sys.stdin], [], [], 0.0) == ([sys.stdin], [], []):
            ch = sys.stdin.read(1)
            sys.stdin.flush()
        return ch

    def _loop(self):
        prev_observation, info = self.env.reset()

        rewards = 0
        rewards_learn = 0
        step = 0
        while(True):
            action = self.agent.action(prev_observation)

            observation, reward, terminated, truncated, info = self.env.step(action)
            rewards += reward
            # self.env.render()
            rewards_learn += self.agent.store_transition(step, prev_observation, action, reward, observation)

            prev_observation = observation  


            self.agent.learn(terminated, truncated)
            if terminated or truncated:
                break
                
        return rewards, rewards_learn
    
    def loops(self):
        windows = 100
        rewards_window = deque(maxlen=windows)
        rewards_learn_window = deque(maxlen=windows)
        rewards_max = 0

        i_episode = 0
        while(True):
            i_episode += 1

            ch = self._getch()
            if ch == 'q': 
                break
            elif ch == 't': 
                self.env = self.env_t
            elif ch == 'h': 
                self.env = self.env_h
            elif ch == 'l':
                self.log = not self.log
            elif ch == 's':
                self.agent.save(self.id_)
                print('save')
            
            reward, reward_learn = self._loop()

            rewards_window.append(reward)
            rewards_learn_window.append(reward_learn)


            if i_episode > 99:    
                rewards_ = round(np.mean(rewards_window), 1)
                rewards_learn_ = round(np.mean(rewards_learn_window), 1)

                # n = np.sum(np.array(scores_window)>=1)
                if  rewards_ > rewards_max:
                    rewards_max = rewards_
                    self.agent.save(self.id_)
                    print('Save model', rewards_max)
                
                rprint(f"Episode {i_episode} | Reward: {rewards_}, {rewards_learn_}")



    # agent policy that uses the observation and info
    def set_agent(self, agent:AgentWrapper): 
        self.agent = agent

    def close(self):
        self.env.close()

if __name__ == "__main__":
    #env = Env("CartPole-v1")
    #env.loops()
    #env.close()
    pass

