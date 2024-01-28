import os
import sys
sys.path.append(os.path.join(os.getcwd()))

from pylib.basic.pp import *

import gym_helper

import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np

import os

class Net(nn.Module):
    def __init__(self, shape_states, n_action):
        # Define the network structure, a very simple fully connected network
        super(Net, self).__init__()
        hidden_layer=256
        # Define the structure of fully connected network
        self.fc1 = nn.Linear(shape_states, hidden_layer)  # layer 1
        self.fc1.weight.data.normal_(0, 0.1) # in-place initilization of weights of fc1
        self.out = nn.Linear(hidden_layer, n_action) # layer 2
        self.out.weight.data.normal_(0, 0.1) # in-place initilization of weights of fc2
        
        
    def forward(self, x):
        # Define how the input data pass inside the network
        x = self.fc1(x)
        x = F.relu(x)
        actions_value = self.out(x)
        return actions_value



class Agent(gym_helper.AgentWrapper):


    def __init__(self):
        super().__init__()

    def init(self, filename):
        self.N_ACTIONS = self.env.action_space.n  # N actions
        self.SHAPE_STATES = self.env.observation_space.shape[0] # N states shape
        self.SHAPE_ACTIONS = 0 if isinstance(self.env.action_space.sample(), np.int64) else self.env.action_space.sample().shape
        self.MEMORY_CAPACITY = 100000
        self.LR = 0.0001
        self.GAMMA = 0.99
        self.TAU = 0.01
        self.BATCH_SIZE = 128
        self.EPSILON = 0.9
        self.TARGET_NETWORK_REPLACE_FREQ = 100

        self.epsilon = 0.0
        self.steps = 0

        # -----------Define 2 networks (target and training)------#
        self.eval_net, self.target_net = Net(self.SHAPE_STATES, self.N_ACTIONS), Net(self.SHAPE_STATES, self.N_ACTIONS)

        self.load(filename)
        
        # Define counter, memory size and loss function
        self.learn_step_counter = 0 # count the steps of learning process
        self.memory_counter = 0 # counter used for experience replay buffer
        
        # ----Define the memory (or the buffer), allocate some space to it. The number 
        # of columns depends on 4 elements, s, a, r, s_, the total is N_STATES*2 + 2---#
        self.memory = np.zeros((self.MEMORY_CAPACITY, self.SHAPE_STATES * 2 + 2)) 
        
        #------- Define the optimizer------#
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=self.LR)
        
        # ------Define the loss function-----#
        self.loss_func = nn.MSELoss()

    def action(self, observation):

        # This function is used to make decision based upon epsilon greedy
        self.epsilon = self.steps / (self.steps + 1000)

        observation = torch.unsqueeze(torch.FloatTensor(observation), 0) # add 1 dimension to input state x
        # input only one sample
        if np.random.uniform() < self.epsilon:   # greedy
            # use epsilon-greedy approach to take action
            actions_value = self.eval_net.forward(observation)
            #print(torch.max(actions_value, 1)) 
            # torch.max() returns a tensor composed of max value along the axis=dim and corresponding index
            # what we need is the index in this function, representing the action of cart.
            action = torch.max(actions_value, 1)[1].data.numpy()
            action = action[0] if self.SHAPE_ACTIONS == 0 else action.reshape(self.SHAPE_ACTIONS)  # return the argmax index
        else:   # random
            action = np.random.randint(0, self.N_ACTIONS)
            action = action if self.SHAPE_ACTIONS == 0 else action.reshape(self.SHAPE_ACTIONS)
        return action
    
    def store_transition(self, step, prev_observation, action, reward, observation):
        self.steps +=1

        if self.SHAPE_STATES == 4:
            x, x_dot, theta, theta_dot = observation
            r1 = (self.env.unwrapped.x_threshold - abs(x)) / self.env.unwrapped.x_threshold - 0.8
            r2 = (self.env.unwrapped.theta_threshold_radians - abs(theta)) / self.env.unwrapped.theta_threshold_radians - 0.5
            reward = r1 + r2
        elif self.SHAPE_STATES == 8:
            x, y, vx, vy, a, va, _, _ = observation
            r1 = (1 - abs(x)) / 1 - 1
            r2 = (3 - abs(a)) / 3 - 1
            r3 = 0 # (1.5 - abs(y)) / 1.5 - 0
            r4 = ((2 - abs(vy + 0.2)) / 2 - 0.95) * 2
            # reward = r1 + r2 + r3 + r4
            # print(reward)
        else:
            pass

        # This function acts as experience replay buffer        
        transition = np.hstack((prev_observation, [action, reward], observation)) # horizontally stack these vectors
        # if the capacity is full, then use index to replace the old memory with new one
        index = self.memory_counter % self.MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.memory_counter += 1

        return reward

    def learn(self, terminated, truncated):

        if (terminated or truncated) and self.memory_counter > self.MEMORY_CAPACITY:
            # Define how the whole DQN works including sampling batch of experiences,
            # when and how to update parameters of target network, and how to implement
            # backward propagation.
            for _ in range(100):
                # update the target network every fixed steps
                if self.learn_step_counter % self.TARGET_NETWORK_REPLACE_FREQ == 0:
                    # Assign the parameters of eval_net to target_net
                    self.target_net.load_state_dict(self.eval_net.state_dict())
                self.learn_step_counter += 1
                
                # Determine the index of Sampled batch from buffer
                sample_index = np.random.choice(self.MEMORY_CAPACITY, self.BATCH_SIZE) # randomly select some data from buffer
                # extract experiences of batch size from buffer.
                b_memory = self.memory[sample_index, :]
                # extract vectors or matrices s,a,r,s_ from batch memory and convert these to torch Variables
                # that are convenient to back propagation
                b_s = Variable(torch.FloatTensor(b_memory[:, :self.SHAPE_STATES]))
                # convert long int type to tensor
                b_a = Variable(torch.LongTensor(b_memory[:, self.SHAPE_STATES:self.SHAPE_STATES+1].astype(int)))
                b_r = Variable(torch.FloatTensor(b_memory[:, self.SHAPE_STATES+1:self.SHAPE_STATES+2]))
                b_s_ = Variable(torch.FloatTensor(b_memory[:, -self.SHAPE_STATES:]))
                
                # calculate the Q value of state-action pair
                q_eval = self.eval_net(b_s).gather(1, b_a) # (batch_size, 1)
                #print(q_eval)
                # calculate the q value of next state
                q_next = self.target_net(b_s_).detach() # detach from computational graph, don't back propagate
                # select the maximum q value
                #print(q_next)
                # q_next.max(1) returns the max value along the axis=1 and its corresponding index
                q_target = b_r + self.GAMMA * q_next.max(1)[0].view(self.BATCH_SIZE, 1) # (batch_size, 1)
                loss = self.loss_func(q_eval, q_target)
                
                self.optimizer.zero_grad() # reset the gradient to zero
                loss.backward()
                self.optimizer.step() # execute back propagation for one step
                # print('learn')
    
    def save(self, filename):
        filename = filename + '.pth'
        torch.save(self.eval_net.state_dict(), filename)

    def load(self, filename):
        filename = filename + '.pth'
        if os.path.exists(filename):
            print('load model: ' + filename)
            self.eval_net.load_state_dict(torch.load(filename))
            self.target_net.load_state_dict(torch.load(filename))


if __name__ == "__main__":
    # env = gym_helper.Env("CartPole-v1", Agent())
    env = gym_helper.Env("LunarLander-v2", Agent())
    env.loops()
    env.close()