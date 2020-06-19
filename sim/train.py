import tensorflow as tf
tf.compat.v1.disable_eager_execution()


import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from sim_1d_env import OneDHeat

# Get the environment and extract the number of actions.
ENV_NAME = "OneDHeat"
env = OneDHeat()
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.n

# Next, we build a very simple model.
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
               target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

weights_name = 'dqn_initial_weights.h5f'
intermediate_weights = 'dqn_{step}_weights.h5f'

from rl.callbacks import ModelIntervalCheckpoint

test = False
train = True

if train:
    save_weights = ModelIntervalCheckpoint(intermediate_weights, 10000, verbose=0)
    callbacks = [save_weights]
    dqn.fit(env, nb_steps=200000, visualize=False, verbose=1, callbacks=callbacks)
    dqn.save_weights(weights_name, overwrite=True)

if test:
    import time
    # time.sleep(5)
    # dqn.load_weights(weights_name)

    for i in range(1,21):
        print ("Iteration", i)
        dqn.load_weights(intermediate_weights.format(step=i*10000))
        dqn.test(env, nb_episodes=1, visualize=True)