#!/usr/bin/env python3
# Note: The script has been cloned and tweaked from:
# https://github.com/patrickloeber/python-fun/tree/master/snake-pygame

from collections import namedtuple
from enum import Enum
import numpy as np
import random
import pygame
import constants as c

pygame.init()
font = pygame.font.Font(f"arial.ttf", c.DEFAULT_FONT_SIZE)
#font = pygame.font.SysFont("arial", 25)
Point = namedtuple("Point", "x, y")


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class PlayerMode(Enum):
    HUMAN = 1
    AI = 2


class SnakeGame:
    def __init__(
        self,
        w: int = c.GAME_WIDTH,
        h: int = c.GAME_HEIGHT,
        mode: PlayerMode = PlayerMode.HUMAN,
    ):
        self.w = w
        self.h = h
        self.mode = mode
        self.direction = self.head = self.snake = self.score = self.food = self.frame_iteration = None
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.reset()
        
    def _place_food(self):
        x = random.randint(0, (self.w - c.BLOCK_SIZE) // c.BLOCK_SIZE) * c.BLOCK_SIZE
        y = random.randint(0, (self.h - c.BLOCK_SIZE) // c.BLOCK_SIZE) * c.BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - c.BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * c.BLOCK_SIZE), self.head.y)
        ]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def handle_user_inputs(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                self.direction = Direction.RIGHT
            elif event.key == pygame.K_UP:
                self.direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                self.direction = Direction.DOWN

    def play_step(self, action: list | np.ndarray = None):
        self.frame_iteration += 1

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if self.mode == PlayerMode.HUMAN:
                self.handle_user_inputs(event)

        # 2. move
        if self.mode == PlayerMode.AI:
            self._move(action)  # update the head
        else:
            self._move()
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        is_game_over = False
        if self._is_collision() or self.frame_iteration > 100 * len(self.snake):
            is_game_over = True
            reward = -10
            return reward, is_game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(c.SPEED)
        # 6. return game over and score
        return reward, is_game_over, self.score
    
    def _is_collision(self, point: Point = None):
        if not point:
            point = self.head
        # hits boundary
        if (
            point.x > self.w - c.BLOCK_SIZE or
            point.x < 0 or
            point.y > self.h - c.BLOCK_SIZE or
            point.y < 0
        ):
            return True
        # hits itself
        if point in self.snake[1:]:
            return True
        return False
        
    def _update_ui(self):
        self.display.fill(c.BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(
                self.display, c.BLUE1, pygame.Rect(
                    pt.x, pt.y, c.BLOCK_SIZE, c.BLOCK_SIZE
                )
            )
            pygame.draw.rect(self.display, c.BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(
            self.display, c.RED, pygame.Rect(
                self.food.x, self.food.y, c.BLOCK_SIZE, c.BLOCK_SIZE
            )
        )
        
        text = font.render(f"Score: {self.score}", True, c.WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action: list | np.ndarray = None):
        if self.mode == PlayerMode.AI:
            # [straight, right, left]
            clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
            current_direction_index = clockwise.index(self.direction)
            if np.array_equal(action, [1, 0, 0]):
                new_direction = clockwise[current_direction_index]
            elif np.array_equal(action, [0, 1, 0]):
                new_direction = clockwise[(current_direction_index + 1) % 4]
            else:  # [0, 0, 1]
                new_direction = clockwise[(current_direction_index - 1) % 4]

            self.direction = new_direction
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += c.BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= c.BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += c.BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= c.BLOCK_SIZE
        self.head = Point(x, y)


def play_human():
    game = SnakeGame()
    # game loop
    while True:
        _, game_over, score = game.play_step(action=None)
        if game_over:
            break
    print(f"Final Score: {score}")
    pygame.quit()


if __name__ == "__main__":
    play_human()
