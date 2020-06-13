import gym
from sim_1d_env import OneDHeat

import time

env = OneDHeat()
observation = env.reset()

action = env.action_space.sample()
for i in range(1000):
  for _ in range(1000):
    # your agent here (this takes random actions)
    action = int(input("Enter action >> "))
    observation, reward, done, info = env.step(action)
    s = env.render()
    if done == 1:
      env.reset()
      break
