import customtkinter as ctk

WINDOW_TITLE = "Finance Manager"
WINDOW_X = 1280
WINDOW_Y = 720

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_X}x{WINDOW_Y}")




app = App()
app.mainloop()
