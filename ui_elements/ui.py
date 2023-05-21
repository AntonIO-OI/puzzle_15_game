import customtkinter as ctk

import ai
from model import Puzzle
from ui_elements.button import IButtonNav
from ui_elements.puzzle_initializer import PuzzleInitializer
from ui_elements.tile import Tile
from ui_elements.win_window import WinWindow
from ui_elements.window import Window


aiMoves_dict = {(1, 0): "UP   ", (-1, 0): "DOWN ", (0, 1): "LEFT ", (0, -1): "RIGHT"}
level_dict = {f"Level #{i}": i for i in range(1, 15)}


class UI(ctk.CTk):
    instance = None

    def __init__(self, level: int = 14):
        super().__init__()
        self.level = level
        self.ai_moves = []
        self.ai_move_index = 0
        self.moves_counter = 0
        self.after_id = None
        self.animation_running = False

        # Initializers
        self.window_initializer = Window(self)
        self.window_initializer.initialize_window()
        self.puzzle = PuzzleInitializer(level).initialize_puzzle()

        # Information Frames
        self.tile_frame = ctk.CTkFrame(self, fg_color="#91D6CD")
        self.label_frame = ctk.CTkFrame(self, fg_color="#FFF2D0", border_width=3, border_color="#2A9D8F")
        self.navigation_frame = ctk.CTkFrame(self, fg_color="#FFF2D0", border_width=3, border_color="#2A9D8F")

        # Navigation Buttons
        self.reset_button = IButtonNav(self.navigation_frame, text="Reset", command=self.reset)
        self.move_button = IButtonNav(self.navigation_frame, text="Move", command=self.make_correct_move)
        self.solve_button = IButtonNav(self.navigation_frame, text="Solve", command=self.solve_animation)
        self.shuffle_button = IButtonNav(self.navigation_frame, text="Shuffle", command=self.shuffle)

        # Information Labels
        self.moves_label = ctk.CTkLabel(self.label_frame, text=f"Moves:", font=("Martel Sans", 20), text_color="#000")
        self.moves_value = ctk.CTkLabel(self.label_frame, text=str(self.moves_counter), font=("Martel Sans", 20),
                                        text_color="#E76F51", width=30)
        self.next_move_label = ctk.CTkLabel(self.label_frame, text="Next move:", font=("Martel Sans", 20),
                                            text_color="#000")
        self.next_move_value = ctk.CTkLabel(self.label_frame, text="", font=("Martel Sans", 20), text_color="#E76F51",
                                            width=80)

        ai.init(self.puzzle.boardSize)
        self.initialize_ui_elements()
        self.draw_game_field(self.puzzle)
        self.draw_label_field()
        self.draw_navigation()

        UI.instance = self
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def initialize_ui_elements(self):
        self.grid_columnconfigure(0, weight=1)
        self.tile_frame.grid(row=0, column=0, padx=0, pady=(20, 10), sticky="")
        self.label_frame.grid(row=1, column=0, padx=0, pady=10, sticky="")
        self.navigation_frame.grid(row=2, column=0, padx=0, pady=30, sticky="")

    def draw_navigation(self) -> None:
        self.reset_button.grid(row=0, column=0, padx=35, pady=20)
        self.move_button.grid(row=0, column=1, padx=35, pady=20)
        self.solve_button.grid(row=0, column=2, padx=35, pady=20)
        self.shuffle_button.grid(row=0, column=3, padx=35, pady=20)

    def draw_game_field(self, puzzle: Puzzle) -> None:
        for i in range(puzzle.boardSize):
            for j in range(puzzle.boardSize):
                button_text = str(puzzle[i][j]) if puzzle[i][j] != 0 else ""
                button = Tile(
                    self.tile_frame,
                    text=button_text,
                    command=lambda row=i, col=j: self.make_move(puzzle, (row, col)),
                )
                button.grid(row=i, column=j, padx=2, pady=2)

    def update_game_field(self, puzzle: Puzzle) -> None:
        for i in range(puzzle.boardSize):
            for j in range(puzzle.boardSize):
                button = self.tile_frame.grid_slaves(row=i, column=j)[0]
                button_text = str(puzzle[i][j]) if puzzle[i][j] != 0 else ""
                button.configure_text(button_text)

    def draw_label_field(self) -> None:
        self.moves_label.grid(row=0, column=0, padx=(75, 0), pady=10)
        self.moves_value.grid(row=0, column=1, padx=(0, 75), pady=10)

        self.next_move_label.grid(row=0, column=2, padx=(75, 5), pady=10)
        self.next_move_value.grid(row=0, column=3, padx=(0, 75), pady=10)

    def make_move(self, puzzle: Puzzle, pos: tuple) -> None:
        text = str(puzzle[pos[0]][pos[1]])
        direction = (pos[0] - puzzle.blankPos[0], pos[1] - puzzle.blankPos[1])

        if direction == self.ai_moves[self.ai_move_index] if self.ai_move_index < len(self.ai_moves) else False:
            if direction in [puzzle.RIGHT, puzzle.LEFT, puzzle.UP, puzzle.DOWN]:
                puzzle.move(direction)
                self.moves_counter += 1
                self.ai_move_index += 1

            if self.ai_move_index < len(self.ai_moves):
                next_move = aiMoves_dict[self.ai_moves[self.ai_move_index]]
            else:
                self.ai_move_index = 0
                self.ai_moves = []
                next_move = ""
            self.update_next_move(next_move)
        else:
            if direction in [puzzle.RIGHT, puzzle.LEFT, puzzle.UP, puzzle.DOWN]:
                self.ai_move_index = 0
                self.ai_moves = []
                puzzle.move(direction)
                self.moves_counter += 1
                next_move = " "
                self.update_next_move(next_move)

        self.update_moves_counter(self.moves_counter)

        if pos == puzzle.blankPos:
            button = self.tile_frame.grid_slaves(row=pos[0], column=pos[1])[0]
            button.configure_text(text="")

            button = self.tile_frame.grid_slaves(row=pos[0] - direction[0], column=pos[1] - direction[1])[0]
            button.configure_text(text=text if text != "0" else "")

        if puzzle.checkWin():
            WinWindow.create_window(self.moves_counter)

    def update(self):
        self.update_game_field(self.puzzle)

        self.moves_counter = 0
        self.update_moves_counter(self.moves_counter)
        self.update_next_move("")

        self.ai_move_index = 0
        self.ai_moves = []

    def shuffle(self) -> None:
        self.puzzle.level_shuffle(self.level)
        self.update()

    def reset(self) -> None:
        self.puzzle.__init__(shuffle=False)
        self.update()

    def solve(self) -> None:
        self.ai_moves = ai.idaStar(self.puzzle)
        self.ai_move_index = 0

    def make_correct_move(self) -> None:
        if len(self.ai_moves) == 0:
            self.solve()

        self.perform_next_move()

    def solve_animation(self):
        if len(self.ai_moves) == 0:
            self.solve()

        self.animation_running = True

        def make_correct_move_animation():
            if len(self.ai_moves) == 0:
                self.solve()

            self.perform_next_move()
            if self.animation_running and self.ai_move_index < len(self.ai_moves):
                self.after_id = self.after(500, make_correct_move_animation)

        self.after_id = self.after(500, make_correct_move_animation)

    def perform_next_move(self):
        if len(self.ai_moves) != 0 and self.ai_move_index < len(self.ai_moves):
            pos = (
                self.ai_moves[self.ai_move_index][0] + self.puzzle.blankPos[0],
                self.ai_moves[self.ai_move_index][1] + self.puzzle.blankPos[1],
            )
            self.make_move(self.puzzle, pos)
            if self.ai_move_index < len(self.ai_moves) - 1:
                self.update_next_move(aiMoves_dict[self.ai_moves[self.ai_move_index]])

    def update_moves_counter(self, counter: int) -> None:
        self.moves_value.configure(text=counter)

    def update_next_move(self, next_move: str) -> None:
        self.next_move_value.configure(text=next_move)

    def on_window_close(self):
        self.animation_running = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
        if WinWindow.instance:
            WinWindow.instance.on_window_close()
        UI.instance = None
        self.destroy()
