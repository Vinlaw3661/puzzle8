from engine.EightPuzzleEngine import EightPuzzleEngine
import sys
def main():
    if len(sys.argv) < 2:
        raise Exception("At least one command required")
    else:
        game = EightPuzzleEngine()
        game.cmd(sys.argv[1:])

if __name__ == "__main__":
    main()