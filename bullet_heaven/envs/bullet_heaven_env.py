import gymnasium as gym
from gymnasium import spaces
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bullet_heaven.envs.logger import Logger
from bullet_heaven.envs.reward import RewardCalc
from render.renderer import Renderer
from game.game import Game
from game.player import Player

class BulletHeavenEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, algorithm, seed, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        self.dt = 1/60
        self.state = None
        #moving, shooting and choosing an upgrade
        self.action_space = spaces.MultiDiscrete([9, 32, 8])
        #player: x, y, speed, dmg, dmg_cooldown, hp, shoot_cooldown, regen, xp multiplier, stat_points - 10
        #enemies: x, y, hp x15 - 45
        #xp: x, y x15 - 30
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(83,),
            dtype=np.float32
        )

        self.reward_calc = RewardCalc()
        self.logger = Logger(algorithm, seed=seed)

        self.player = Player(640, 360, True)
        self.game = Game(self.player, self.dt)

    def __get_observation(self):
        obs = np.zeros(83, dtype=np.float32)
        px, py = self.player.get_position()
        obs[0:2] = px / 1280, py / 720
        obs[2] = np.clip(self.player.move_speed / 600, 0, 1)
        obs[3] = np.clip(self.player.dmg / 200, 0, 1)
        obs[4] = 1 - np.clip(self.player.dmg_cooldown, 0, 1)
        obs[5] = self.player.hp / self.player.max_hp
        obs[6] = 1 - np.clip(self.player.shoot_cooldown, 0, 1)
        obs[7] = np.clip(self.player.stat_points, 0, 1)

        enemies = sorted(
            self.game.enemies,
            key=lambda e: self.player.position.distance_to(e.position)
            )[:15]
        for i, enemy in enumerate(enemies):
            idx = 10 + i * 3
            obs[idx] = enemy.position.x / 1280
            obs[idx + 1] = enemy.position.y / 720
            obs[idx + 2] = enemy.hp / enemy.max_hp

        xps = sorted(
            self.game.xp,
            key=lambda e: self.player.position.distance_to(e.position)
        )[:15]
        for i, xp in enumerate(xps):
            idx = 55 + i * 2
            obs[idx] = xp.position.x / 1280
            obs[idx + 1] = xp.position.y / 720

        return obs

    def reset(self, *, seed = None, options = None):
        super().reset(seed=seed, options=options)
        self.player = Player(640, 360, True)
        self.game = Game(self.player, self.dt, seed=seed)
        self.state = self.__get_observation()
        #self.state = np.zeros(self.observation_space.shape, dtype=np.float32)
        info = {}
        self.reward_calc.reset(self.player, self.game)
        return self.state, info
    
    def step(self, action):
        self.player.apply_action(action[:2])
        self.game.update(self.dt)
        self.state = self.__get_observation()
        terminated = self.player.hp <=0
        truncated = False
        reward, info = self.reward_calc.calculate(
            self.player,
            self.game,
            terminated)
        return self.state, reward, terminated, truncated, info
    

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


