from collections import deque
import random
import torch
import numpy as np
from snake_game import SnakeGame, Direction, Point
import constants as c
from model import LinearQNet
from trainer import QTrainer
from plot import plot


class Agent:
    def __init__(self):
        self.n_games: int = 0
        self.epsilon: float = 0  # randomness
        self.memory = deque(maxlen=c.MAX_MEMORY)
        # TODO: implement model and trainer
        self.model = LinearQNet(c.INPUT_SIZE, c.HIDDEN_SIZE, c.OUTPUT_SIZE)
        self.trainer = QTrainer(self.model, lr=c.LEARNING_RATE, gamma=c.GAMMA)

    @staticmethod
    def get_state(game):
        # the state space consists of 11 states
        state: list = [
            game.is_danger_straight(), game.is_danger_right(), game.is_danger_left(),
            game.direction == Direction.LEFT,
            game.direction == Direction.RIGHT,
            game.direction == Direction.UP,
            game.direction == Direction.DOWN,
            game.food.x < game.head.x,  # food: at left
            game.food.x > game.head.x,  # food: at right
            game.food.y < game.head.x,  # food: at up
            game.food.y > game.head.x,  # food: at down
        ]
        return np.array(state, dtype=int)  # bool -> binary

    def remember(self, state, action, reward, next_state, game_status):
        self.memory.append((state, action, reward, next_state, game_status))
        # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        sample = random.sample(self.memory, c.BATCH_SIZE) \
            if len(self.memory) > c.BATCH_SIZE \
            else self.memory
        self.trainer.train_step(*zip(*sample))

    def train_short_memory(self, state, action, reward, next_state, game_status):
        self.trainer.train_step(state, action, reward, next_state, game_status)
        self.remember(state, action, reward, next_state, game_status)

    def get_action(self, state):
        # epsilon-greedy random moves: exploration-exploitation tradeoff
        self.epsilon = 80 - self.n_games
        action: list = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            state_current = torch.tensor(state, dtype=torch.float)
            # self.model(state) calls the forward method with the state arg
            prediction = self.model(state_current)  # -> e.g. [5.0, 2.7, 1.0]
            move = torch.argmax(prediction).item()  # -> 0
        action[move] = 1
        return action


def train():
    plot_scores: list = []
    plot_mean_scores: list = []
    total_score: int = 0
    best_score: int = 0
    agent: Agent = Agent()
    game: SnakeGame = SnakeGame()
    while True:
        # get current state
        state_current = agent.get_state(game)
        # get move based on the current state
        action = agent.get_action(state_current)
        # perform move and get new state
        reward, status, score = game.play_step(action)
        # get the next state
        state_new = agent.get_state(game)
        # train short memory of the agent
        agent.train_short_memory(state_current, action, reward, state_new, status)
        if status:
            # train long memory of the agent and plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            best_score = max(best_score, score)
            print(f"Game {agent.n_games}: \tScore: {score} \t Best: {best_score}")
            agent.model.save()
            plot_scores.append(best_score)
            total_score += best_score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    train()
