import gymnasium as gym
from gymnasium import spaces
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from render.renderer import Renderer
from game.game import Game
from game.player import Player

class BulletHeavenEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        self.dt = 1/60
        self.state = None
        #moving, shooting and choosing an upgrade
        self.action_space = spaces.MultiDiscrete([9, 32, 4])
        #Observations:
        #player: x, y, speed, dmg, hp, shoot_cooldown - 5
        #enemies: x, y, hp x15 - 45
        self.observation_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(50,),
            dtype=np.float32
        )

        self.player = Player(640, 360, True)
        self.game = Game(self.player, self.dt)

    def __get_observation(self):
        obs = np.zeros(50, dtype=np.float32)
        px, py = self.player.get_position()
        obs[0:2] = px / 1280, py / 720
        obs[2] = self.player.move_speed
        obs[3] = self.player.dmg
        obs[4] = self.player.hp / self.player.max_hp

        for i, enemy in enumerate(self.game.enemies[:15]):
            idx = 5 + i * 3
            obs[idx]     = enemy.position.x / 1280
            obs[idx + 1] = enemy.position.y / 720
            obs[idx + 2] = enemy.hp / enemy.max_hp

        return obs

    def reset(self, *, seed = None, options = None):
        super().reset(seed=seed, options=options)
        self.player = Player(640, 360, True)
        self.game = Game(self.player, self.dt, seed=seed)
        self.state = np.zeros(self.observation_space.shape, dtype=np.float32)
        info = {}
        return self.state, info
    
    def step(self, action):
        self.player.apply_action(action[:2])
        self.game.update(self.dt)
        self.state = self.__get_observation()
        reward = 0.0
        terminated = self.player.hp <=0
        truncated = False
        return self.state, reward, terminated, truncated, {}
    

    def get_render_info(self):
        return self.player.player_pos, self.player.bullets, self.game.enemies

    def render(self):
        if not hasattr(self, "renderer"):
            self.renderer = Renderer()
        
        player_pos, bullets, enemies = self.get_render_info()
        mins, secs = self.game.get_time()
        self.renderer.render(player_pos, bullets, enemies, mins, secs)

    def close(self):
        if hasattr(self, "renderer"):
            self.renderer.close()


