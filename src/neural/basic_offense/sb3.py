from pathlib import Path
from random import randint
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import (
    CallbackList,
    CheckpointCallback,
    ProgressBarCallback,
    EvalCallback,
)
from stable_baselines3.common.monitor import Monitor
from neural.save import suffix_for
from neural.basic_offense import environment

Algo = PPO

seed = randint(0, 10**8)


def learn(epochs, checkpoint_interval, output_folder: Path):
    env = environment.makegym()
    eval_env = Monitor(environment.makegym())
    env.reset()
    model = Algo(
        "MlpPolicy",
        env,
        tensorboard_log=output_folder.joinpath(f"logs_{seed}"),
        seed=seed,
    )
    checkpoint_callback = CheckpointCallback(
        save_freq=checkpoint_interval, save_path=output_folder, name_prefix="model"
    )
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=output_folder.joinpath("best"),
        deterministic=True,
        render=False,
        eval_freq=checkpoint_interval // 4,
    )
    callback_list = CallbackList(
        [checkpoint_callback, eval_callback, ProgressBarCallback()]
    )
    model.learn(epochs, reset_num_timesteps=True, callback=callback_list)
    model.save(output_folder.joinpath("model"))


def load(episodes, visualize, input_folder: Path, epoch=None):
    input_path = input_folder.joinpath(
        f"model{suffix_for(epoch)}{'_steps' if epoch else ''}"
    )

    env = environment.Environment(visualize)
    env.reset()
    model = Algo.load(input_path, env=env)

    acc_reward = 0.0
    succeed = 0
    for _ in range(episodes):
        observation = env.reset()
        done = False
        steps = 0
        episode_reward = 0.0
        while not done:
            if visualize:
                env.render()
            action, _ = model.predict(observation)
            observation, reward, done, _ = env.step(action)
            episode_reward += reward
            if done:
                print("last reward", reward)
            steps += 1
        if episode_reward > 0.0:
            succeed += 1
        print("episode reward", episode_reward)
        episode_average_reward = episode_reward / steps
        print("episode average reward", episode_average_reward)
        acc_reward += episode_average_reward
    env.close()
    print()
    average_reward = acc_reward / episodes
    print(f"{round(average_reward, 3)} [{succeed} / {episodes}]")
