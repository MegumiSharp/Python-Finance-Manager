# Importing the necessary libraries
import customtkinter
from PIL import Image
from CTkTable import *
import tkinter.messagebox as messagebox

# Importing the views and models used in the application
from src.views.setup_view import SetupView
from src.views.welcome_view import WelcomeView
from src.views.dashboard_view import DashboardView
from src.models.user_settings import UserSettings

# Import the necessary costants and settings used in the application
from config.settings import (WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME, DEFAULT_APPEARANCE_MODE, KEY_IS_FIRST_TIME, VALUE_TRUE, WELCOME_FRAME, DASHBOARD_FRAME)

# Main application GUI, implemented as a class
class AppController(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.current_view = None                                                 # The current View is the frame or view showed in the windows
        self.user = UserSettings()                                               # Initialize user settings

        # Set Windows Settings like appearance and color theme or size and name
        customtkinter.set_appearance_mode(DEFAULT_APPEARANCE_MODE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.title(APP_NAME)

        # Block the resizing of the window (allegedly)
        self.grid_propagate(False)
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.maxsize(0, 0)
        self.resizable(width=False, height=False)


        # Start showing the right frame
        self.__startup()

    # Used to not have duplicate code
    def _show_view(self, view_class):
        if self.current_view:
            self.current_view.hide()  
        
        # Change the current_view to the class and use the abstract method show() to show it
        self.current_view = view_class(self, controller=self, user=self.user)
        self.current_view.show()

    # Startup function to decide what frame to show to the user, if it is the first time, the setup frame is showed
    def __startup(self):
        # Decide what frame to show to the user, if first time user show setup frame
        if self.user.read_json_value(KEY_IS_FIRST_TIME) == VALUE_TRUE:
            self._show_view(SetupView)
        else:
            self.switch_frame(WELCOME_FRAME)

    # Function used to switch from the welcome frame to the dashboard frame, is also used in setup view to change frame
    def switch_frame(self, frame_name):
        if frame_name == WELCOME_FRAME:
            self._show_view(WelcomeView)
        elif frame_name == DASHBOARD_FRAME:
            self._show_view(DashboardView)
        else:
            raise ValueError(f"Unknown frame name: {frame_name}")