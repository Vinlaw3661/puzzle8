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
    def __init__(self, save_file='../data/SaveState.json'):
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
        
    
    def scramble(self, n: int, seed: int = None):
        random_generator = random.Random(seed) if seed is not None else random
        for _ in range(n):
            valid_move = random_generator.choice(self.valid_moves)
            self.move(valid_move)
    
    def print_state(self,state: list):
        state_format = "\n".join(" ".join(str(state[i + j]) if state[i + j] != 0 else " " for j in range(3)) for i in range(0, 9, 3))
        print(state_format)

    def parse_command(self, command_string: str) -> Union[str, Commands] | Union[list, Commands]:

        if not command_string:
            raise CommandParsingError("Error: at least one command is required")

        try:
            # Validate the move command
            if "move" in command_string:
                assert len(command_string) == 2 \
                    and command_string[0] == "move" \
                    and command_string[1] in ["up", "down", "left", "right"] \
                    and " ".join(command_string) in [m.value for m in self.valid_moves], \
                    f"Error: invalid move: {' '.join(command_string)}"
                command = moves[" ".join(command_string)]
                print(" ".join(command_string))
                return command, Commands.MOVE

            # Validate the setState command
            if "setState" in command_string:
                try:
                    state = [int(value) for value in command_string[1:]]
                except Exception as e:
                    raise Exception(f"Error: invalid puzzle state: {e}")

                assert len(command_string) == 10 \
                    and command_string[0] == "setState" \
                    and set(state) == set(range(9)), \
                    f"Error: invalid puzzle state: {' '.join(command_string)}"
                print(" ".join(command_string))
                return state, Commands.SET

            # Validate the printState command
            if "printState" in command_string:
                assert len(command_string) == 1 \
                    and command_string[0] == "printState", \
                    f"Invalid printState command: {' '.join(command_string)}"
                state = self.state
                print(" ".join(command_string)) 
                return state, Commands.PRINT

            # Validate the comment command
            if "#" in command_string or "//" in command_string:
                assert command_string[0] in ["#", "//"], \
                    f"Invalid comment command: {' '.join(command_string)}"
                symbol = command_string[0]
                comment = " ".join(command_string[1:])
                print(" ".join(command_string))
                return comment, Commands.COMMENT

            # Validate the scramble command
            if "scramble" in command_string:
                if "seed" in command_string:
                    assert len(command_string) == 4 \
                        and command_string[0] == "scramble" \
                        and command_string[1].isnumeric() \
                        and command_string[2] == "seed" \
                        and command_string[3].isnumeric(), \
                        f"Invalid scramble command: {' '.join(command_string)}"
                    seed = int(command_string[3])
                    n = int(command_string[1])
                    print(" ".join(command_string))
                    return (n, seed), Commands.SEED
                else:
                    assert len(command_string) == 2 \
                        and command_string[0] == "scramble" \
                        and command_string[1].isnumeric(), \
                        f"Invalid scramble command: {' '.join(command_string)}"
                    n = int(command_string[1])
                    print(" ".join(command_string))
                    return n, Commands.SCRAMBLE

            # Validate the file command
            if ".txt" in command_string[0]:
                assert len(command_string) == 1, \
                    f"Invalid file command: {' '.join(command_string)}"
                filename = command_string[0]
                print(" ".join(command_string))
                return filename, Commands.CMDFILE

            else:
                raise CommandParsingError(f"Invalid command: {' '.join(command_string)}")
            

        except AssertionError as e:
            raise CommandParsingError(e)

        except Exception as e:
            raise Exception(f"Invalid command: {' '.join(command_string)}")
        
    def set_state(self, state: list):
        self.state = state
        self.valid_moves = self.get_valid_moves()
        self.save_state()

    def cmd(self, command_string: str):
        try:
            result, command_type = self.parse_command(command_string)

            if command_type == Commands.SET:
                self.set_state(result)
                print(self.state)

            if command_type == Commands.PRINT:
                self.print_state(result)

            if command_type == Commands.MOVE:
                self.move(result)
                print(self.state)

            if command_type == Commands.COMMENT:
                print(result)

            if command_type == Commands.CMDFILE:
                self.cmdfile(result)

            if command_type == Commands.SCRAMBLE:
                self.scramble(result)
                print(self.state)

            if command_type == Commands.SEED:
                self.scramble(result[0], result[1])
                print(self.state)

        except AssertionError as e:
            print(e)

        except CommandParsingError as e:
            print(e)

        except Exception as e:
            print(e)

    def move(self, move: Moves) -> list:

        # This condition is used for testing purposes,
        # All command validation is handled in the parse_command method
        if move not in self.valid_moves:
            raise Exception(f"Invalid move: {move}")

        free_position = self.state.index(0)

        if move == Moves.UP:
            target_position = free_position + 3
        if move == Moves.DOWN:
            target_position = free_position - 3
        if move == Moves.LEFT:
            target_position = free_position + 1
        if move == Moves.RIGHT:
            target_position = free_position - 1

        self.state[free_position], self.state[target_position] = \
            self.state[target_position], self.state[free_position]
        self.valid_moves = self.get_valid_moves()
        self.save_state()

    def cmdfile(self, filename: str):
        with open(filename, 'r') as file:
            for line in file:
                line = line.rstrip()  

                if not line.strip():  
                    print(line) 
                else:
                    try:
                        self.cmd(line.strip().split())  
                    except Exception as e:
                        print(line)
     

