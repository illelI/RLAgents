import gymnasium as gym
from gymnasium import spaces
import numpy as np

class BulletHeavenEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        self.dt = 1/60

        self.action_space = spaces.MultiDiscrete([9, 32, 4])
        self.observation_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(52,),
            dtype=np.float32
        )

        self.game = None
