from model import Puzzle


class PuzzleInitializer:
    def __init__(self, level: int = 14):
        self.level = level

    def initialize_puzzle(self):
        return Puzzle(shuffle=True, level=self.level)
