from sim_1d_env import OneDHeat
import time

env = OneDHeat()
observation = env.reset()
time.sleep(0)

action = env.action_space.sample()
for i in range(1000):
  for _ in range(1000):
    # your agent here (this takes random actions)
    action = _ % 11
    observation, reward, done, info = env.step(action)
    print(observation)
    if done == 1:
      env.reset()
      break
    # time.sleep(1)
    print (reward, observation, action)
