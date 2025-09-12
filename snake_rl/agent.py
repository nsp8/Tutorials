from collections import deque
import random
import torch
import numpy as np
from snake_game import SnakeGame, Direction, Point
import constants as c
from snake_rl.constants import MAX_MEMORY


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=c.MAX_MEMORY)
        # TODO: add model and trainer

    def get_state(self, game):
        ...

    def remember(self, state, action, reward, next_state, status):
        ...

    def train_long_memory(self):
        ...

    def train_short_memory(self):
        ...

    def get_action(self, state):
        ...


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()
    while True:
        state_old = agent.get_state(game)


def main():
    train()
