import gym
from sim_1d_env import OneDHeat

import time

env = OneDHeat()
observation = env.reset()

action = env.action_space.sample()
positions = {str(e):i for i,e in enumerate(env.cooler_indices)}
for i in range(1000):
  print("Episode ", i, " ...................")
  for _ in range(1000):
    # your agent here (this takes random actions)
    position = input("Enter cooling position >> ")
    if position in positions:
      action = positions[position]

    else:
      print("Invalid location")
      action = 0

    observation, reward, done, info = env.step(action)
    s = env.render()
    if done == 1:
      env.reset()
      break
