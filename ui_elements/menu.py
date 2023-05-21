import customtkinter as ctk

from ui_elements.win_window import WinWindow
from ui_elements.ui import UI

level_dict = {f"Level #{i}": i for i in range(1, 15)}


class Menu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x500")
        self.title("15 Puzzle")
        self.iconbitmap("./static/puzzle_icon.ico")
        self.choice = 14

        self.navigation_frame = ctk.CTkFrame(self)
        self.navigation_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.start_button = ctk.CTkButton(
            self.navigation_frame,
            text="START",
            font=("Arial", 20, "bold"),
            fg_color="#F4A261",
            text_color="#000",
            command=self.start,
            border_width=3,
            border_color="#2A9D8F",
            hover_color="#E76F51",
        )
        self.start_button.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        self.combox = ctk.CTkOptionMenu(
            self.navigation_frame,
            font=("Arial", 12, "bold"),
            values=list(level_dict.keys()),
            command=self.option_menu,
            fg_color="#F4A261",
            text_color="#000",
            button_color="#F4A261",
            button_hover_color="#2A9D8F",
        )
        self.combox.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def option_menu(self, choice):
        self.choice = level_dict[choice]

    def start(self):
        if not UI.instance:
            UI(self.choice).mainloop()

    def on_window_close(self):
        if UI.instance:
            UI.destroy(UI.instance)
        if WinWindow.instance:
            WinWindow.destroy(WinWindow.instance)
        self.destroy()
