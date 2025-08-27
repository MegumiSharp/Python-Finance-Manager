from abc import ABC, abstractmethod
import customtkinter as ctk

# Base class for all views in the application. It provides a common interface and basic functionality for all views    
class BaseView(ctk.CTkFrame, ABC):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        # Setup the main frame 0x0 a normal window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    @abstractmethod
    def setup_ui(self):
        pass
    
    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()