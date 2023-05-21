import customtkinter as ctk


class Tile(ctk.CTkButton):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(
            font=("Arial", 32, "bold"),
            fg_color="#F4A261",
            text_color="#000",
            hover=False,
            width=90,
            height=90,
        )

    def configure_text(self, text: str) -> None:
        self.configure(text=text)
