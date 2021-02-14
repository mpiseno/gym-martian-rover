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
        # pass def heuristic(env, s): s is state which is x, y, xvel, yvel, goalx, goaly?
            # if you're moving left away from goal, move right
            # if you're moving right toward goal, keep moving right
            # if you're moving left toward goal, keep moving left
            # if you're moving right away from goal, move left
        # based on if left or right is returned,
        self.game.update(action)
        # position
        #velocity
        # goal position
        state = np.array([[self.game.rover.pos[0], self.game.rover.pos[1]],
                 [self.game.rover.vel[0], self.game.rover.vel[1]],
                 [self.game.goal.position[0], self.game.goal.position[1]]])

        # every time step is small neg reward, and when it gets to goal location give 10
        reward = 0
        done= False
        if not self.game.success:
            reward = -1
        else:
            reward = 10
            done = True
        return state, reward, done, {}

    def reset(self):
        self.state = np.array([[0, 1],
                 [0, 1],
                 [self.game.goal.position[0], self.game.goal.position[1]]])
        self.game.success = False

    def render(self, mode='human'):
        return np.flipud(np.rot90(self.game.pygame.surfarray.array3d(self.game.pygame.display.get_surface())))

    def close(self):
        pass

env = MartianRoverEnv()
rewards = 0;
s, r, d, i = env.step(0)
rewards += r
print(rewards)
s, r, d, i = env.step(0)
rewards += r
print(rewards)
s, r, d, i = env.step(1)
rewards += r
print(rewards)

# print(envs.registry.all())