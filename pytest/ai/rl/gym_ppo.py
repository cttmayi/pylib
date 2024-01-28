#import gym
import gymnasium as gym


from stable_baselines3 import PPO, DQN
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy



env_name = "LunarLander-v2"
env = gym.make(env_name)          # 导入注册器中的环境

env = DummyVecEnv([lambda : env])

model_ppo = PPO(
    "MlpPolicy", 
    env=env,
    #verbose=1,

    policy_kwargs=dict(net_arch=[256, 256]),
    learning_rate=5e-4,
    batch_size=128,
    gamma=0.99,
)

model_dqn= DQN(
    "MlpPolicy", 
    env=env, 
    learning_rate=5e-4,
    batch_size=128,
    buffer_size=50000,
    learning_starts=0,
    target_update_interval=250,
    policy_kwargs={"net_arch" : [256, 256]},
    verbose=1,
    tensorboard_log="./tensorboard/LunarLander-v2/"
)

#model = DQN.load("./model/LunarLander3.pkl")
model = model_ppo
model.learn(total_timesteps=1e6)
env.close()

input("Press any key to continue...")
env = gym.make(env_name, render_mode="human")
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, render=False)
env.close()
print(f"MEAN: {mean_reward:.2f}, STD: {std_reward:.2f}")

# input("Press any key to save model...")
# model.save("./model/LunarLander3.pkl")