from random import choice
from copy import deepcopy


class Puzzle:
    UP = (1, 0)
    DOWN = (-1, 0)
    LEFT = (0, 1)
    RIGHT = (0, -1)

    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, board_size: int = 4, shuffle: bool = True, level: int = 14) -> None:
        self.boardSize = board_size
        self.board = [[0] * board_size for _ in range(board_size)]
        self.blankPos = (board_size - 1, board_size - 1)

        for i in range(board_size):
            for j in range(board_size):
                self.board[i][j] = i * board_size + j + 1

        # 0 represents blank square, init in bottom right corner of board
        self.board[self.blankPos[0]][self.blankPos[1]] = 0

        if shuffle:
            self.level_shuffle(level)

    def __str__(self) -> str:
        out_string = ""
        for i in self.board:
            out_string += "\t".join(map(str, i))
            out_string += "\n"
        return out_string

    def __getitem__(self, key: int) -> list:
        return self.board[key]

    def check_level(self) -> int:
        level_counter = 0
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if (
                        self.board[i][j] != i * self.boardSize + j + 1
                        and self.board[i][j] != 0
                ):
                    level_counter += 1
        return level_counter

    def level_shuffle(self, level: int = 14) -> None:
        self.__init__(shuffle=False)

        while self.check_level() != level:
            direction = choice(self.DIRECTIONS)
            self.move(direction)

    def move(self, direction: tuple) -> bool:
        new_blank_pos = (self.blankPos[0] + direction[0], self.blankPos[1] + direction[1])

        if (
                new_blank_pos[0] < 0
                or new_blank_pos[0] >= self.boardSize
                or new_blank_pos[1] < 0
                or new_blank_pos[1] >= self.boardSize
        ):
            return False

        self.board[self.blankPos[0]][self.blankPos[1]] = self.board[new_blank_pos[0]][
            new_blank_pos[1]
        ]
        self.board[new_blank_pos[0]][new_blank_pos[1]] = 0
        self.blankPos = new_blank_pos
        return True

    def check_win(self) -> bool:
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if (
                        self.board[i][j] != i * self.boardSize + j + 1
                        and self.board[i][j] != 0
                ):
                    return False

        print("You win")
        return True

    def is_solvable(self) -> bool:
        # Flatten the board into a single list
        flat_board = [number for row in self.board for number in row]

        inversions = 0
        for i in range(len(flat_board)):
            for j in range(i + 1, len(flat_board)):
                # Count the number of inversions
                if flat_board[i] > flat_board[j] != 0:
                    inversions += 1

        # Check if the puzzle size is even
        if self.boardSize % 2 == 0:
            # If the blank is on an even row counting from the bottom and inversions are odd,
            # or if the blank is on an odd row counting from the bottom and inversions are even,
            # the puzzle is solvable
            if (
                    (self.blankPos[0] % 2 == 0 and inversions % 2 != 0) or
                    (self.blankPos[0] % 2 != 0 and inversions % 2 == 0)
            ):
                print("Solvable")
                return True
        else:
            # If the number of inversions is even, the puzzle is solvable
            if inversions % 2 == 0:
                print("Solvable")
                return True

        print("Not Solvable")
        return False

    def hash(self, group: dict = None) -> str:
        if group is None:
            group = {}
        if not group:
            group = {s for s in range(self.boardSize ** 2)}

        hash_string = ["0"] * 2 * (self.boardSize ** 2)

        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self[i][j] in group:
                    hash_string[2 * self[i][j]] = str(i)
                    hash_string[2 * self[i][j] + 1] = str(j)
                else:
                    hash_string[2 * self[i][j]] = "x"
                    hash_string[2 * self[i][j] + 1] = "x"

        return "".join(hash_string).replace("x", "")

    def simulate_move(self, direction: tuple) -> tuple:
        sim_puzzle = deepcopy(self)

        return sim_puzzle.move(direction), sim_puzzle
