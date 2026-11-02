
class RewardCalc:

    def __init__(
        self,
        kill_reward=2.0,
        xp_reward=0.5,
        damage_penalty=0.1,
        death_penalty=10.0
    ):
        self.kill_reward = kill_reward
        self.xp_reward = xp_reward
        self.damage_penalty = damage_penalty
        self.death_penalty = death_penalty

        self.reset()

    def reset(self, player, game):
        self.previous_kills = game.enemies_killed
        self.previous_xp = player.total_xp_collected
        self.previous_damage = player.total_damage_taken

    def calculate(self, game, player, terminated):
        reward = 0.0

        kills = game.enemies_killed - self.previous_kills
        xp = player.xp_collected - self.previous_xp
        damage = player.dmg_taken - self.previous_damage

        reward_kill = kills * self.kill_reward
        reward_xp = xp * self.xp_reward
        reward_dmg = -damage * self.damage_penalty
        reward_death = -self.death_penalty if terminated else 0.0

        self.previous_kills = game.enemies_killed
        self.previous_xp = player.xp_collected
        self.previous_damage = player.dmg_taken

        total_reward = (
            reward_kill
            + reward_xp
            + reward_dmg
            + reward_death
        )

        info = {
            "reward_kill": reward_kill,
            "reward_xp": reward_xp,
            "reward_damage": reward_dmg,
            "reward_death": reward_death,
            "reward_total": total_reward
        }

        return total_reward, info

