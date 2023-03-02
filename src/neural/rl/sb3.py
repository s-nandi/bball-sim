from pathlib import Path
from tqdm import tqdm
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import (
    CallbackList,
    CheckpointCallback,
    ProgressBarCallback,
    EvalCallback,
)
from neural.rl import frozen
from neural.save import suffix_for

Algo = PPO


def learn(epochs, checkpoint_interval, output_folder: Path):
    env = frozen.makegym()
    eval_env = frozen.makegym()
    env.reset()
    model = Algo("MlpPolicy", env)
    checkpoint_callback = CheckpointCallback(
        save_freq=checkpoint_interval, save_path=output_folder, name_prefix="model"
    )
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=output_folder.joinpath("best"),
        deterministic=True,
        render=False,
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

    env = frozen.Frozen(frozen.makegymnasium("human" if visualize else None))
    env.reset()
    model = Algo.load(input_path, env=env)

    succeed = 0
    for _ in range(episodes):
        obs = env.reset()
        done = False
        while not done:
            if visualize:
                env.render()
            action, _ = model.predict(obs)
            obs, reward, done, _ = env.step(action.item())
            if reward == 1:
                succeed += 1
    print(f"{round(succeed / episodes, 3)} [{succeed} / {episodes}]")
