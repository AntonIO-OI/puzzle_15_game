import customtkinter as ctk


class IButtonNav(ctk.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            font=("Arial", 20, "bold"),
            fg_color="#F4A261",
            text_color="#000",
            border_width=3,
            border_color="#2A9D8F",
            hover_color="#E76F51",
        )
