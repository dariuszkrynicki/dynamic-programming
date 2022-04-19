from __future__ import print_function, division
from builtins import range
import numpy as np
from typing import Dict, Tuple

class Grid:
    def __init__(self, width, height, start):
        # i verical, j horizontal
        self.width = width
        self.height = height
        self.i = start[0]
        self.j = start[1]

    def set(self, rewards: Dict[Tuple(int, int): int], actions: Dict[Tuple(int, int): int], obey_prob): 
        # Dict[Tuple(int, int): int] = Dict[Tuple(row, col): int] = Dict[Tuple(i,j): reward]
        # Dict[Tuple(int, int): int] = Dict[Tuple(row, col): int] = Dict[Tuple(i,j): action]
        self.rewards = rewards
        self.actions = actions
        self.obey_prob = obey_prob

    def non_terminal_states(self):
        return self.actions.keys()

    def set_state(self, s):
        self.i = s[0]
        self.j = s[1]

    def current_state(self):
        return (self.i, self.j)

    def is_terminal(self, s):
        return s not in self.actions

    def check_move(self, action):
        i = self.i
        j = self.j

        # check if legal move first
        if action in self.actions[(self.i, self.j)]:
            if action == 'U':
                i -= 1
            elif action == 'D':
                i += 1
            elif action == 'R':
                j += 1
            elif action == 'L':
                j -= 1
        reward = self.rewards.get((i,j), 0)
        return ((i, j), reward)

    def get_transition_probs(self, action):
        probs = []
        state, reward = self.check_move(action)
        probs.append((self.obey_prob, reward, state))
        disobey_prob = 1 - self.obey_prob

        if not (disobey_prob > 0.0):
            return probs
        if action == 'U' or action == 'D':
            state, reward  = self.check_move('L')
            probs.append((disobey_prob / 2, reward, state))
            state, reward = self.check_move('R')
            probs.append((disobey_prob / 2, reward, state)
        if action == 'L' or action == 'R':
            state, reward  = self.check_move('U')
            probs.append((disobey_prob / 2, reward, state))
            state, reward = self.check_move('D')
            probs.append((disobey_prob / 2, reward, state)
        return probs

    def game_over(self):
        # true = game over
        # true if we are in a state where no actions are possible
        return (self.i, self.j) not in self.actions

    def all_states(self):
        return set(self.action.keys()) | set(self.rewards.keys())

def standard_grid(obey_prob=1.0, step_cost=None):
      # .  .  .  1
      # .  x  . -1
      # s  .  .  .

      # obey_brob (float): the probability of obeying the command
      # step_cost (float): a penalty applied each step to minimize the number of moves (-0.1)

      g = Grid(3, 4, (2,0))
      rewards = {(0,3): 1, (1,3): -1}

      actions = {
        (0, 0): ('D', 'R'),
        (0, 1): ('L', 'R'),
        (0, 2): ('L', 'D', 'R'),
        (1, 0): ('U', 'D'),
        (1, 2): ('U', 'D', 'R'),
        (2, 0): ('U', 'R'),
        (2, 1): ('L', 'R'),
        (2, 2): ('L', 'R', 'U'),
        (2, 3): ('L', 'U'),
      }

      g.set(rewards, actions, obey_prob)

      if step_cost is not None:
        g.rewards.update({
        (0, 0): step_cost,
        (0, 1): step_cost,
        (0, 2): step_cost,
        (1, 0): step_cost,
        (1, 2): step_cost,
        (2, 0): step_cost,
        (2, 1): step_cost,
        (2, 2): step_cost,
        (2, 3): step_cost,
        })
    return g
