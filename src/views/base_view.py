from abc import ABC, abstractmethod
from turtle import width
import customtkinter as ctk

from config.settings import WINDOW_HEIGHT, WINDOW_WIDTH

class BaseView(ctk.CTkFrame, ABC):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    @abstractmethod
    def setup_ui(self):
        """Metodo che ogni view deve implementare per costruire l'interfaccia"""
        pass

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()
