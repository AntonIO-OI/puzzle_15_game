class Window:
    def __init__(self, ui):
        self.ui = ui

    def initialize_window(self):
        self.ui.geometry("900x600")
        self.ui.resizable(False, False)
        self.ui.configure(fg_color="#91D6CD")
        self.ui.title("15 Puzzle")
        self.ui.iconbitmap("./static/puzzle_icon.ico")
