import random
import numpy as np
import gym
from gym import error, spaces, utils
from gym import envs
from gym.utils import seeding

from martian_rover_game import RoverGame


class MartianRoverEnv(gym.Env):
    def __init__(self):
        self.game = RoverGame()
        self.state = self.game.reset()
        self.action_space = spaces.Discrete(3) # Left, Right, Nothing
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(6,))

    def step(self, action):
        self.game.update(action)
        self.state = np.array(self.game.get_state())

        reward = -0.1
        done = False
        if self.game.success:
            reward = 100
            done = True

        info = {}
        return self.state, reward, done, info

    def reset(self):
        self.state = self.game.reset()

    def render(self):
        return self.game.draw()
        

env = MartianRoverEnv()
time_steps = 400
for _ in range(time_steps):
    s, r, d, _ = env.step(random.randint(0, 2))
    print(f'state: {s}')
    print(f'reward: {r}')
    env.render()