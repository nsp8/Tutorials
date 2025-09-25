# Snake game 
using DQN and PyGame

---
## Play
1. Clone the repository
2. Install all the requirements
3. If you want to play the snake game:
```commandline
python3 snake_game.py
```
But if you want the agent to play the snake game:
```commandline
python3 agent.py
```

---
## Overview
An agent works with the game environment, and the learning model to play the game. 
The choice of model being used is Deep Q Network, which extends reinforcement learning to predict actions using a deep neural network.
> The `Q value` designates the quality of the action taken. 

The game is written in PyGame, which has a core method, `play_step(action)` that executes a step in the game, producing a reward, game_over and score tuple.
This is how the Q learning training loop would look like:
1. `state = get_state(game)`
2. `action = get_move(state)  # call model.predict() which is the `
3. `reward, game_over, score = play_step(action)`
4. `new_state = get_state(game)`
5. \<remember\>
6. `model.train()`

The deep learning aspect of the game is a feed forward neural network implemented in PyTorch, that predicts the next plausible action.

---
## Reward system
When the agent:
1. eats the food: `+10`
2. encounters game over: `-10`
3. everything else: `0`
---
## Action space
To eliminate the possibility of the agent hitting itself:
1. `(1, 0, 0)` represents going in the same direction as the current one
2. `(0, 1, 0)` represents going right
3. `(0, 0, 1)` represents going left
---
## State space
Each state has these 11 (boolean) values:
`(
    danger_straight, danger_right, danger_left, 
    direction_left, direction_right, direction_up, direction_down, 
    food_left, food_right, food_up, food_down
)`

Examples:
1. the agent, somewhere towards the center of the screen, moving in the right direction, with the food placed somewhere to its southeast direction, will have this state value:
   `(0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1)`
2. the agent moving up along the right edge of the screen, with the food placed in the top left corner, will have this state value:
   `(0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0)`
---
## Deep Learning (Feed Forward NN)
- input: 11 boolean values from the state
- \<hidden layer\>: 256
- output (with an activation function like `max`) : 3 (action)
