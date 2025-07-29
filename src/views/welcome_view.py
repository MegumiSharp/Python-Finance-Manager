import customtkinter as ctk


class WelcomeView(ctk.CTkFrame):
    
    def __init__(self, parent, controller=None):
        super().__init__(parent, controller, corner_radius=0, fg_color="transparent")


    def create_welcome_frame(self):
        pass