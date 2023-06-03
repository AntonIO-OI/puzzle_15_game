import customtkinter as ctk
import os
import pickle

from ai import PuzzleSolver
from config import aiMoves_dict
from model import Puzzle
from ui_elements.button import IButtonNav
from ui_elements.puzzle_initializer import PuzzleInitializer
from ui_elements.tile import Tile
from ui_elements.win_window import WinWindow
from ui_elements.window import Window


class UI(ctk.CTk):
    instance = None

    def __init__(self, level: int = 14) -> None:
        super().__init__()
        self.__level = level
        self.__ai_moves = []
        self.__ai_move_index = 0
        self.__moves_counter = 0
        self.__after_id = None
        self.__animation_running = False

        # Initializers
        Window(self).initialize_window()
        self.__puzzle = PuzzleInitializer(level).initialize_puzzle()
        self.__ai = PuzzleSolver(self.__puzzle.boardSize)

        # Information Frames
        self.__tile_frame = ctk.CTkFrame(self, fg_color="#91D6CD")
        self.__label_frame = ctk.CTkFrame(self, fg_color="#FFF2D0", border_width=3, border_color="#2A9D8F")
        self.__navigation_frame = ctk.CTkFrame(self, fg_color="#FFF2D0", border_width=3, border_color="#2A9D8F")

        # Navigation Buttons
        self.__reset_button = IButtonNav(self.__navigation_frame, text="Reset", command=self.reset)
        self.__move_button = IButtonNav(self.__navigation_frame, text="Move", command=self.make_correct_move)
        self.__solve_button = IButtonNav(self.__navigation_frame, text="Solve", command=self.solve_animation)
        self.__shuffle_button = IButtonNav(self.__navigation_frame, text="Shuffle", command=self.shuffle)

        # Information Labels
        self.__moves_label = ctk.CTkLabel(self.__label_frame, text=f"Moves:", font=("Martel Sans", 20),
                                          text_color="#000")
        self.__moves_value = ctk.CTkLabel(self.__label_frame, text=str(self.__moves_counter), font=("Martel Sans", 20),
                                          text_color="#E76F51", width=30)
        self.__next_move_label = ctk.CTkLabel(self.__label_frame, text="Next move:", font=("Martel Sans", 20),
                                              text_color="#000")
        self.__next_move_value = ctk.CTkLabel(self.__label_frame, text="", font=("Martel Sans", 20),
                                              text_color="#E76F51", width=80)

        self.initialize_ui_elements()
        self.draw_game_field(self.__puzzle)
        self.draw_label_field()
        self.draw_navigation()

        UI.instance = self
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def initialize_ui_elements(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.__tile_frame.grid(row=0, column=0, padx=0, pady=(20, 10), sticky="")
        self.__label_frame.grid(row=1, column=0, padx=0, pady=10, sticky="")
        self.__navigation_frame.grid(row=2, column=0, padx=0, pady=30, sticky="")

    def draw_navigation(self) -> None:
        self.__reset_button.grid(row=0, column=0, padx=35, pady=20)
        self.__move_button.grid(row=0, column=1, padx=35, pady=20)
        self.__solve_button.grid(row=0, column=2, padx=35, pady=20)
        self.__shuffle_button.grid(row=0, column=3, padx=35, pady=20)

    def draw_game_field(self, puzzle: Puzzle) -> None:
        for i in range(puzzle.boardSize):
            for j in range(puzzle.boardSize):
                button_text = str(puzzle[i][j]) if puzzle[i][j] != 0 else ""
                button = Tile(
                    self.__tile_frame,
                    text=button_text,
                    command=lambda row=i, col=j: self.make_move(puzzle, (row, col)),
                )
                button.grid(row=i, column=j, padx=2, pady=2)

    def update_game_field(self, puzzle: Puzzle) -> None:
        for i in range(puzzle.boardSize):
            for j in range(puzzle.boardSize):
                button = self.__tile_frame.grid_slaves(row=i, column=j)[0]
                button_text = str(puzzle[i][j]) if puzzle[i][j] != 0 else ""
                button.configure_text(button_text)

    def draw_label_field(self) -> None:
        self.__moves_label.grid(row=0, column=0, padx=(75, 0), pady=10)
        self.__moves_value.grid(row=0, column=1, padx=(0, 75), pady=10)

        self.__next_move_label.grid(row=0, column=2, padx=(75, 5), pady=10)
        self.__next_move_value.grid(row=0, column=3, padx=(0, 75), pady=10)

    def make_move(self, puzzle: Puzzle, pos: tuple) -> None:
        local_moves = self.__moves_counter
        text = str(puzzle[pos[0]][pos[1]])
        direction = (pos[0] - puzzle.blankPos[0], pos[1] - puzzle.blankPos[1])

        if direction == self.__ai_moves[self.__ai_move_index] if self.__ai_move_index < len(self.__ai_moves) else False:
            if direction in [puzzle.RIGHT, puzzle.LEFT, puzzle.UP, puzzle.DOWN]:
                puzzle.move(direction)
                self.__moves_counter += 1
                self.__ai_move_index += 1

            if self.__ai_move_index < len(self.__ai_moves):
                next_move = aiMoves_dict[self.__ai_moves[self.__ai_move_index]]
            else:
                self.__ai_move_index = 0
                self.__ai_moves = []
                next_move = ""
            self.update_next_move(next_move)
        else:
            if direction in [puzzle.RIGHT, puzzle.LEFT, puzzle.UP, puzzle.DOWN]:
                self.__ai_move_index = 0
                self.__ai_moves = []
                puzzle.move(direction)
                self.__moves_counter += 1
                next_move = " "
                self.update_next_move(next_move)

        self.update_moves_counter(self.__moves_counter)

        if pos == puzzle.blankPos:
            button = self.__tile_frame.grid_slaves(row=pos[0], column=pos[1])[0]
            button.configure_text(text="")

            button = self.__tile_frame.grid_slaves(row=pos[0] - direction[0], column=pos[1] - direction[1])[0]
            button.configure_text(text=text if text != "0" else "")

        if puzzle.check_win() and local_moves != self.__moves_counter:
            if self.__after_id:
                self.after_cancel(self.__after_id)
                self.__after_id = None
            WinWindow.create_window(self.__moves_counter)

    def update(self) -> None:
        self.update_game_field(self.__puzzle)

        self.__moves_counter = 0
        self.update_moves_counter(self.__moves_counter)
        self.update_next_move("")

        self.__ai_move_index = 0
        self.__ai_moves = []

    def shuffle(self) -> None:
        self.__puzzle.level_shuffle(self.__level)
        self.update()

    def reset(self) -> None:
        self.__puzzle.__init__(shuffle=False)
        self.update()

    def solve(self) -> None:
        if self.__puzzle.is_solvable():
            self.__ai_moves = self.__ai.ida_star(self.__puzzle)
            self.__ai_move_index = 0
        else:
            print("Puzzle is impossible to solve")

    def make_correct_move(self) -> None:
        if len(self.__ai_moves) == 0:
            self.solve()

        self.perform_next_move()

    def solve_animation(self) -> None:
        if len(self.__ai_moves) == 0:
            self.solve()

        self.__animation_running = True

        def make_correct_move_animation() -> None:
            if len(self.__ai_moves) == 0:
                self.solve()

            self.perform_next_move()
            if self.__animation_running and self.__ai_move_index < len(self.__ai_moves):
                self.__after_id = self.after(500, make_correct_move_animation)

        self.__after_id = self.after(500, make_correct_move_animation)

    def perform_next_move(self) -> None:
        if len(self.__ai_moves) != 0 and self.__ai_move_index < len(self.__ai_moves):
            pos = (
                self.__ai_moves[self.__ai_move_index][0] + self.__puzzle.blankPos[0],
                self.__ai_moves[self.__ai_move_index][1] + self.__puzzle.blankPos[1],
            )
            self.make_move(self.__puzzle, pos)

    def update_moves_counter(self, counter: int) -> None:
        self.__moves_value.configure(text=counter)

    def update_next_move(self, next_move: str) -> None:
        self.__next_move_value.configure(text=next_move)

    def on_window_close(self) -> None:
        self.__animation_running = False
        if self.__after_id:
            self.after_cancel(self.__after_id)
        if WinWindow.instance:
            WinWindow.instance.on_window_close()
        UI.instance = None
        self.destroy()
