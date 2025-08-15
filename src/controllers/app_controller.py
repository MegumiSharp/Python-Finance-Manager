# Importing the necessary libraries
import os
import sys
from tkinter import PhotoImage
import customtkinter
from tkinter import messagebox

# Importing the views and models used in the application
from src.views.setup_view import SetupView
from src.views.welcome_view import WelcomeView
from src.models.user_settings import UserSettings
from src.controllers.dashboard_controller import DashboardController


# Import the necessary costants and settings used in the application
from config.settings import (WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME, DEFAULT_APPEARANCE_MODE, KEY_IS_FIRST_TIME, VALUE_TRUE, WELCOME_FRAME, DASHBOARD_FRAME, ICONS_PATH,TASKBAR_ICON_FILE_NAME)

# Main application GUI, implemented as a class
class AppController(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.current_view = None                                                 # The current View is the frame or view showed in the windows
        self.user = UserSettings()                                               # Initialize user settings
        self.views = {}

        # Modify the taskbar icon to the current expensia logo
        img = PhotoImage(file=os.path.join(ICONS_PATH, TASKBAR_ICON_FILE_NAME))
        self.iconphoto(True, img) 

        # Set Windows Settings like appearance and color theme or size and name
        customtkinter.set_appearance_mode(DEFAULT_APPEARANCE_MODE)
        
        # The geometry of the window, it appear in the same position (working for monitor 1920x1080 , with 2 monitor)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+300+150")

        self.title(APP_NAME)

        # Block the resizing of the window (allegedly)
        self.grid_propagate(False)
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.maxsize(0, 0)
        self.resizable(width=False, height=False)

        # Start showing the right frame
        self.__startup()

    # Startup function to decide what frame to show to the user, if it is the first time, the setup frame is showed
    def __startup(self):
        # Decide what frame to show to the user, if first time user show setup frame
        if self.user.read_json_value(KEY_IS_FIRST_TIME) == VALUE_TRUE:
            self._show_view(SetupView)
        else:
            self.switch_frame(WELCOME_FRAME)

    # Checks if the current_view hold a value, if not return
    def _hide_or_destroy_current_view(self, view_class):
        if not self.current_view:
            return

        #If the class is SetupView in the current view, because is not needed after the first setup, we destroy it instead of hiding it
        if isinstance(self.current_view, SetupView) and view_class == SetupView:
            self.current_view.destroy()
            return
        
        # If th current_view exist and is not the SetupView, we want to save it and re-use it in the future, maybe, so we hide it
        self.current_view.hide()  

    # If the current_view is not empty, it hides it than create if the view_class is not present in the dictionary it create 
    def _show_view(self, view_class):
        self._hide_or_destroy_current_view(view_class)

        if view_class not in self.views:
            self.views[view_class] = view_class(self, controller=self, user=self.user)
        
        # Change the current_view to the class and use the abstract method show() to show it
        self.current_view = self.views[view_class]
        self.current_view.show()

    # Function used to switch from the welcome frame to the dashboard frame, is also used in setup view to change frame
    def switch_frame(self, frame_name):
        if frame_name == WELCOME_FRAME:
            self._show_view(WelcomeView)
        elif frame_name == DASHBOARD_FRAME:
            self._show_view(DashboardController)
        else:
            raise ValueError(f"Unknown frame name: {frame_name}")
    
    # Close confirmation
    def on_closure(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.views[DashboardController].on_closure()
            

            self.destroy()  # Actually closes the window