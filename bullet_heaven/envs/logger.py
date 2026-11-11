import csv
import os
from collections import deque

class Logger:

    def __init__(
        self,
        algorithm,
        log_interval=100,
        window_size=100,
        seed=None
    ):
        log_dir = "./" + algorithm
        os.makedirs(log_dir, exist_ok=True)

        self.algorithm = algorithm
        self.seed = seed

        self.log_interval = log_interval
        self.window_size = window_size

        self.total_steps = 0
        self.episode_count = 0
        self.next_log_step = log_interval

        self.episode_reward = 0.0
        self.episode_length = 0

        self.reward_kill = 0.0
        self.reward_xp = 0.0
        self.reward_damage = 0.0
        self.reward_death = 0.0

        self.recent_rewards = deque(maxlen=window_size)
        self.recent_lengths = deque(maxlen=window_size)
        self.recent_survival = deque(maxlen=window_size)
        self.recent_kills = deque(maxlen=window_size)
        self.recent_xp = deque(maxlen=window_size)
        self.recent_damage = deque(maxlen=window_size)

        self.episodes_file = open(
            os.path.join(log_dir, "episodes.csv"),
            "w",
            newline="",
            buffering=1
        )

        self.training_file = open(
            os.path.join(log_dir, "training.csv"),
            "w",
            newline="",
            buffering=1
        )

        self.episodes_writer = csv.writer(self.episodes_file)
        self.training_writer = csv.writer(self.training_file)

        self._init_files()

    def _init_files(self):

        self.episodes_writer.writerow([
            "algorithm", "seed", "episode", "total_steps", "pox_x", "pox_y",
            "episode_reward", "episode_length", "survival_time",
            "kills", "xp_collected", "hits_taken",
            "final_hp", "max_hp",
            "damage", "move_speed", "shoot_cooldown",
            "hp_regen", "xp_multiplier", "stat_points",
            "reward_kill", "reward_xp",
            "reward_damage", "reward_death",
            "terminated", "truncated"
        ])

        self.training_writer.writerow([
            "algorithm", "seed", "total_steps", "episodes",
            "mean_reward", "mean_length", "mean_survival_time",
            "mean_kills", "mean_xp", "mean_hits_taken",
            "mean_reward_per_step"
        ])

    def step(self, reward, info):

        self.total_steps += 1
        self.episode_length += 1
        self.episode_reward += reward

        self.reward_kill += info.get("reward_kill", 0.0)
        self.reward_xp += info.get("reward_xp", 0.0)
        self.reward_damage += info.get("reward_damage", 0.0)
        self.reward_death += info.get("reward_death", 0.0)

        if self.total_steps >= self.next_log_step:
            self.log_training()
            self.next_log_step += self.log_interval

    def end_episode(self, info, terminated, truncated):

        self.episode_count += 1

        survival = info.get("survival_time", 0.0)
        kills = info.get("total_kills", 0)
        xp = info.get("total_xp", 0)
        hits = info.get("total_hits_taken", 0)

        self.episodes_writer.writerow([
            self.algorithm,
            self.seed,
            self.episode_count,
            self.total_steps,

            self.episode_reward,
            self.episode_length,
            survival,

            kills,
            xp,
            hits,

            info.get("final_hp", 0),
            info.get("max_hp", 0),

            info.get("damage", 0),
            info.get("move_speed", 0),
            info.get("shoot_cooldown", 0),
            info.get("hp_regen", 0),
            info.get("xp_multiplier", 0),
            info.get("stat_points", 0),

            self.reward_kill,
            self.reward_xp,
            self.reward_damage,
            self.reward_death,

            terminated,
            truncated
        ])

        self.recent_rewards.append(self.episode_reward)
        self.recent_lengths.append(self.episode_length)
        self.recent_survival.append(survival)
        self.recent_kills.append(kills)
        self.recent_xp.append(xp)
        self.recent_damage.append(hits)

        self._reset_episode()

        self.episodes_file.flush()

    def log_training(self, player):

        if not self.recent_rewards:
            return

        count = len(self.recent_rewards)

        mean_reward = sum(self.recent_rewards) / count
        mean_length = sum(self.recent_lengths) / count
        mean_survival = sum(self.recent_survival) / count

        mean_kills = sum(self.recent_kills) / count
        mean_xp = sum(self.recent_xp) / count
        mean_hits = sum(self.recent_damage) / count

        mean_reward_per_step = (
            mean_reward / mean_length
            if mean_length > 0 else 0
        )

        self.training_writer.writerow([
            self.algorithm,
            self.seed,
            self.total_steps,
            self.episode_count,

            player.position.x,
            player.position.y,

            mean_reward,
            mean_length,
            mean_survival,

            mean_kills,
            mean_xp,
            mean_hits,

            mean_reward_per_step
        ])

        self.training_file.flush()

    def _reset_episode(self):

        self.episode_reward = 0.0
        self.episode_length = 0

        self.reward_kill = 0.0
        self.reward_xp = 0.0
        self.reward_damage = 0.0
        self.reward_death = 0.0

    def close(self):

        if not self.episodes_file.closed:
            self.episodes_file.flush()
            self.episodes_file.close()

        if not self.training_file.closed:
            self.training_file.flush()
            self.training_file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
