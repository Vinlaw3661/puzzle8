import unittest
from engine.EightPuzzleEngine import EightPuzzleEngine, Moves, Commands

class EightPuzzleTest(unittest.TestCase):
    def setUp(self):
        # Initialize the EightPuzzleEngine for each test
        self.game = EightPuzzleEngine()

    def test_parse_command(self):
        # Test valid setState command
        state_command = "setState 1 2 3 4 5 6 7 8 0".split()
        result, command_type = self.game.parse_command(state_command)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 0])
        self.assertEqual(command_type, Commands.SET)

        # Test invalid setState command
        with self.assertRaises(Exception):
            self.game.parse_command("setState 1 2 3 4 5 6 7 8".split())

        # Test valid move command
        move_command = "move down".split()
        self.game.state = [1, 2, 3, 4, 5, 6, 0, 7, 8]  # Set a valid state
        self.game.valid_moves = self.game.get_valid_moves()
        result, command_type = self.game.parse_command(move_command)
        self.assertEqual(result, Moves.DOWN)
        self.assertEqual(command_type, Commands.MOVE)

        # Test invalid move command
        with self.assertRaises(Exception):
            self.game.parse_command("move right".split())  # Not a valid move in this state

        # Test printState command
        print_command = "printState".split()
        result, command_type = self.game.parse_command(print_command)
        self.assertEqual(result, self.game.state)
        self.assertEqual(command_type, Commands.PRINT)

    def test_move(self):
        # Test valid move (tile moves into blank)
        self.game.state = [1, 2, 3, 4, 5, 6, 0, 7, 8]  # Blank at position 6
        self.game.valid_moves = self.game.get_valid_moves()
        self.game.move(Moves.DOWN)  # Tile 3 moves into position 6
        self.assertEqual(self.game.state, [1, 2, 3, 0, 5, 6, 4, 7, 8])

        # Test move validity
        self.game.state = [1, 2, 3, 4, 5, 6, 0, 7, 8]  # Reset state
        self.game.valid_moves = self.game.get_valid_moves()
        with self.assertRaises(Exception):
            self.game.move(Moves.RIGHT)  # Invalid move (no tile to move into blank from right)


    def test_cmd(self):
        # Test setState command
        set_state_command = "setState 1 2 3 4 5 6 7 8 0".split()
        self.game.cmd(set_state_command)
        self.assertEqual(self.game.state, [1, 2, 3, 4, 5, 6, 7, 8, 0])

        # Test move command
        self.game.state = [1, 2, 3, 4, 5, 6, 0, 7, 8]
        move_command = "move down".split()
        self.game.cmd(move_command)
        self.assertEqual(self.game.state, [1, 2, 3, 0, 5, 6, 4, 7, 8])

        # Test invalid move command
        invalid_move_command = "move right".split()
        with self.assertRaises(Exception):
            self.game.cmd(invalid_move_command)

        # Test printState command
        print_state_command = "printState".split()
        self.game.cmd(print_state_command)  # Should print the state, no assertion needed

        # Test scramble command
        scramble_command = "scramble 10 seed 42".split()
        self.game.cmd(scramble_command)
        self.assertNotEqual(self.game.state, self.game.goal_state)  # Ensure state changes

    def test_cmdfile(self):
        # Create a temporary test file with commands
        test_file = "test_commands.txt"
        with open(test_file, 'w') as file:
            file.write("setState 1 2 3 4 5 6 7 8 0\n")
            file.write("\n")
            file.write("printState\n")
            file.write("move up\n")
            file.write("# This is a comment\n")
            file.write("scramble 10 seed 42\n")

        self.game.cmdfile(test_file)

        # Validate the final state is scrambled
        self.assertNotEqual(self.game.state, self.game.goal_state)

if __name__ == "__main__":
    unittest.main()
