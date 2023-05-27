from model import Puzzle


class PuzzleInitializer:
    def __init__(self, level: int = 14):
        self.__level = level

    def initialize_puzzle(self):
        return Puzzle(shuffle=True, level=self.__level)
