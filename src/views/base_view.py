from abc import ABC, abstractmethod
import customtkinter as ctk

'''
Base class for all views in the application
It provides a common interface and basic functionality for all views
Each view should inherit from this class and implement the setup_ui method
This class also provides methods to show and hide the view
It uses customtkinter for the UI components
and is designed to be used with a controller for navigation between views
The user parameter is used to access user settings and preferences 
'''       
class BaseView(ctk.CTkFrame, ABC):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user

    @abstractmethod
    def setup_ui(self):
        """Metodo che ogni view deve implementare per costruire l'interfaccia"""
        pass

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()
