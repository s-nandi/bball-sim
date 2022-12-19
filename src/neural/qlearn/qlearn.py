from pathlib import Path
from tqdm import tqdm
import gym
import numpy as np
from neural.qlearn import parse


def makeenv(render_mode=None):
    return gym.make("FrozenLake-v1", render_mode=render_mode, is_slippery=True)


def updated_q(Q, state, action, new_state, learning_rate, reward, discount_factor):
    assert len(Q.shape) == 2
    nactions = Q.shape[1]
    future_value = -float("inf")
    for new_action in range(nactions):
        future_value = max(future_value, Q[new_state, new_action])
    return Q[state, action] + learning_rate * (
        reward + discount_factor * future_value - Q[state, action]
    )


def learn(
    steps, learning_rate, discount_factor, epsilon_decay, min_epsilon, output_path
):
    env = makeenv()

    epsilon = 1.0
    Q = np.zeros((env.observation_space.n, env.action_space.n))
    state, _ = env.reset()
    for step_idx in tqdm(range(steps)):
        if step_idx % (steps // 10) == 0:
            tqdm.write(f"step: {step_idx}")

        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state])

        new_state, reward, terminated, truncated, _ = env.step(action)
        Q[state, action] = updated_q(
            Q,
            state,
            action,
            new_state,
            learning_rate,
            reward,
            discount_factor,
        )
        state = new_state
        epsilon = max(min_epsilon, epsilon - epsilon_decay)

        if terminated or truncated:
            state, _ = env.reset()
    env.close()
    with open(output_path, "w") as f:
        np.savetxt(f, Q)


def load(episodes, max_steps, visualize, input_path):
    with open(input_path, "r") as f:
        Q = np.loadtxt(f)

    print(Q)
    env = makeenv("human" if visualize else None)
    succeed = 0
    for _ in tqdm(range(episodes)):
        observation, _ = env.reset()
        nactions = Q.shape[1]

        lim = max_steps
        reached = False
        for _ in range(lim):
            best_action = 0
            for action in range(nactions):
                if Q[observation, action] > Q[observation, best_action]:
                    best_action = action
            observation, reward, terminated, truncated, _ = env.step(best_action)
            if visualize:
                env.render()
            if terminated or truncated:
                reached = reward == 1
                if visualize:
                    tqdm.write(f"done, reached: {reached}")
                break
        if reached:
            succeed += 1
    print(f"{round(succeed / episodes, 3)} [{succeed} / {episodes}]")


def main(args=None):
    args = parse.parse(args)
    if args.type == parse.LEARN:
        learn(
            args.steps,
            args.learning_rate,
            args.discount_factor,
            args.epsilon_decay,
            args.min_epsilon,
            Path(args.output_path),
        )
    else:
        assert args.type == parse.LOAD
        load(args.episodes, args.max_steps, args.visualize, Path(args.input_path))
