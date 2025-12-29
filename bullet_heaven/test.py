from envs.bullet_heaven_env import BulletHeavenEnv

env = BulletHeavenEnv(render_mode="human")
obs, _ = env.reset()

for i in range(5000):
    action = env.action_space.sample()
    obs, reward, term, trunc, _ = env.step(action)
    env.render()
    if term or trunc:
        break

env.close()
