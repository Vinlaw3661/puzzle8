from enum import Enum
from typing import Union
import random
import json

class CommandParsingError(Exception):
    pass

class Moves(Enum):
    UP = "move up"
    DOWN = "move down"
    LEFT = "move left"
    RIGHT = "move right"

class Commands(Enum):
    MOVE = "move command"
    SET = "set state command"
    PRINT = "print state command"
    SEED = "set random seed"
    SCRAMBLE = "scramble state"
    COMMENT = "print comments"
    CMDFILE = "file commands"

moves = {
    "move up": Moves.UP,
    "move down": Moves.DOWN,
    "move left": Moves.LEFT,
    "move right": Moves.RIGHT
}

class EightPuzzleEngine:
    def __init__(self, save_file='SaveState.json'):
        self.save_file = save_file
        self.goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.state = []
        self.valid_moves = []
        self.load_state()

    def load_state(self):
        with open(self.save_file, 'r') as file:
            save_data = json.load(file)
            self.state = save_data["state"]
            self.valid_moves = [moves[m] for m in save_data["valid_moves"]]

    def save_state(self):
        with open(self.save_file, 'w') as file:
            json.dump({
                "state": self.state,
                "valid_moves": [m.value for m in self.valid_moves]
            }, file)

    def get_valid_moves(self) -> list:
        free_position = self.state.index(0)
        if free_position == 0:
            return [Moves.UP, Moves.LEFT]
        if free_position == 1:
            return [Moves.UP, Moves.LEFT, Moves.RIGHT]
        if free_position == 2:
            return [Moves.UP, Moves.RIGHT]
        if free_position == 3:
            return [Moves.LEFT, Moves.DOWN, Moves.UP]
        if free_position == 4:
            return [Moves.LEFT, Moves.DOWN, Moves.RIGHT, Moves.UP]
        if free_position == 5:
            return [Moves.DOWN, Moves.RIGHT, Moves.UP]
        if free_position == 6:
            return [Moves.DOWN, Moves.LEFT]
        if free_position == 7:
            return [Moves.DOWN, Moves.LEFT, Moves.RIGHT]
        if free_position == 8:
            return [Moves.DOWN, Moves.RIGHT]
