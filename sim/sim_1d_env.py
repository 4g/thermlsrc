import numpy as np
import gym
from gym import spaces

class OneDHeat(gym.Env):
    """1D heat equation to be solved
    dT/dt = (k/(rho*cp)) * laplacian (T)
    Initial condition T=30 deg
    Boundary condition:
        T(x=0,l,t=0)=T_hot
        T(cooling points,t=0 or >t_cool)=T_cold
    """
    def __init__(self):
        super(OneDHeat, self).__init__()
        self.cooler_indices = [-1, 0, 1, 2, 4, 5, 6, 8, 9]
        self.num_coolers = len(self.cooler_indices)
        self.num_sensors = 10
        self.action_space = spaces.Discrete(self.num_coolers)
        self.observation_space = spaces.MultiDiscrete([10 for i in range(self.num_sensors)])
        self.energy = 1

    def setup(self):
        """Geometry"""
        l = 0.1  # m

        """Spatial grid"""
        self.n = self.num_sensors  # nodes
        self.dx = l / self.n  # m
        x = np.linspace(self.dx / 2, l - self.dx / 2, self.n)

        """Temporal"""
        self.dt = 0.5  # s
        self.t = 0

        """Material properties for Al"""
        rho = 2700  # kg/m3
        cp = 897  # J/Kg.K
        k = 247  # W/m.K
        self.alpha = k / (rho * cp)

        """Initial condition"""
        self.T0 = 313.15  # 40deg

        """Heat source"""
        self.T_hot = 313.15  # 40deg

        """Cooling source"""
        self.T_cold = 293.15  # 20deg
        self.t_cool = 10  # time to start cooling in s
        self.ntc = self.t_cool / self.dt

        """Initialisation"""
        self.T = np.ones(self.n) * self.T0
        self.dTdt = np.empty(self.n)
        self.t = 1

    def step(self, action):
        self.t += 1
        for i in range(1, self.n - 1):
            self.dTdt[i] = self.alpha * ((self.T[i + 1] - 2 * self.T[i] + self.T[i - 1]) / self.dx ** 2)

        self.dTdt[0] = self.alpha * ((self.T[1] - 2 * self.T[0] + self.T_hot) / self.dx ** 2)
        self.dTdt[self.n - 1] = self.alpha * ((self.T_hot - 2 * self.T[self.n - 1] + self.T[self.n - 2]) / self.dx ** 2)

        self.T = self.T + self.dTdt * self.dt

        if action == 0:
            pass
        else:
            self.energy += 1.0
            self.T[self.cooler_indices[action]] = self.T_cold

        self.obs = self.compute_observation()
        self.reward, done = self.compute_reward()
        self.action = action
        # if done:
        #     self.reset()

        return self.obs, self.reward, done, {}

    def compute_observation(self):
        obs = 10 * ((self.T - self.T_cold) / (self.T_hot - self.T_cold))
        obs = np.asarray(obs, np.uint8)
        return obs

    def compute_reward(self):
        temperature_reward = 100 if (max(self.T[3], self.T[7])) < (self.T_cold + self.T0)/2 else 0
        energy_reward = 30 / (self.energy + 1)
        time_reward = 100 / self.t
        total_reward = 0
        done = False
        if temperature_reward > 0:
            # print(self.T)
            total_reward = temperature_reward + energy_reward + time_reward
            done = True
        return total_reward, done

    def render(self, mode='human'):
        print(self.obs, self.action, self.cooler_indices[self.action], self.reward)
        return True

    def reset(self):
        self.setup()
        return self.compute_observation()


