
import numpy as np

prev_observation = [2,2]
observation = [0,0]
action = 1
reward = 1


transition = np.hstack((prev_observation, [action, reward], observation))

print(transition)


a = np.arange(24).reshape(6,4)
print(a)

a = a.max(1).reshape(6,1)
print(a)