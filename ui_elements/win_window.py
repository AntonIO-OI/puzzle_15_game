import customtkinter as ctk


class WinWindow(ctk.CTk):
    instance = None  # Class variable to store the instance

    def __init__(self, moves: int = 0):
        super().__init__()

        self.geometry("500x300")
        self.title("15 Puzzle")
        self.iconbitmap("./static/puzzle_icon.ico")

        self.label_frame = ctk.CTkFrame(self, width=350)
        self.label_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.win_label = ctk.CTkLabel(self.label_frame, text="YOU WON!", font=("Arial", 32, "bold"),
                                      text_color="#E76F51")
        self.win_label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        self.inform_label = ctk.CTkLabel(self.label_frame, text="With moves:", font=("Arial", 32, "bold"),
                                         text_color="#fff")
        self.inform_label.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)

        self.moves_label = ctk.CTkLabel(self.label_frame, text=str(moves), font=("Arial", 32, "bold"),
                                        text_color="#E76F51")
        self.moves_label.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

        self.after_id = self.after(5000, self.close)
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)
        WinWindow.instance = self

    def close(self):
        if WinWindow.instance:
            WinWindow.instance = None
            self.destroy()

    def on_window_close(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.close()

    @staticmethod
    def create_window(moves: int = 0):
        if WinWindow.instance is None:
            WinWindow(moves).mainloop()
        else:
            WinWindow.instance.focus()
