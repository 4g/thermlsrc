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
        self.num_coolers = 1
        self.num_sensors = 10
        self.action_space = spaces.Discrete(self.num_coolers)
        self.observation_space = spaces.MultiDiscrete([10 for i in range(self.num_sensors)])

    def setup(self):
        """Geometry"""
        l = 0.1  # m

        """Spatial grid"""
        self.n = 10  # nodes
        self.dx = l / self.n  # m
        x = np.linspace(self.dx / 2, l - self.dx / 2, self.n)

        """Temporal"""
        t_final = 40  # s
        self.dt = 0.5  # s
        self.t = np.arange(0, t_final, self.dt)

        """Material properties for Al"""
        rho = 2700  # kg/m3
        cp = 897  # J/Kg.K
        k = 247  # W/m.K
        self.alpha = k / (rho * cp)

        """Initial condition"""
        self.T0 = 293.15  # 30deg

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

        if self.t >= self.ntc:
            self.T[5] = self.T_cold

        done = 0
        if self.t >= 200:
            done = 1

        reward = 0

        return self.T, reward, done, None

    def reset(self):
        self.setup()

