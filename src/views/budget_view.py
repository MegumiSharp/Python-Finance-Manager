
import customtkinter as ctk
from src.views.base_view import BaseView

class BudgetView(BaseView):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        # Configure HomeView grid to expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Make table frame stretch vertically
    
        self.setup_ui()

    def setup_ui(self):
        self.navigation_frame_label = ctk.CTkLabel(self, text="Budget",)
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
