class Window:
    def __init__(self, ui):
        self.__ui = ui

    def initialize_window(self):
        self.__ui.geometry("900x600")
        self.__ui.resizable(False, False)
        self.__ui.configure(fg_color="#91D6CD")
        self.__ui.title("15 Puzzle")
        self.__ui.iconbitmap("./static/puzzle_icon.ico")
