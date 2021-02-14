import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding

from martian_rover_game import RoverGame

class MartianRoverEnv(gym.Env):
    def __init__(self):
        game = RoverGame()
        self.state = game.reset()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Dict({
            'position': spaces.Box(
                low=np.array([0, 0]),
                high=np.array([800, 400]),
                shape=(2,)
            ),
            'velocity': spaces.Box(-np.inf, np.inf, shape=(2,)),
            'goal': spaces.Box(
                low=np.array([0, 0]),
                high=np.array([800, 400]),
                shape=(2,))
        })

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass


env = MartianRoverEnv()