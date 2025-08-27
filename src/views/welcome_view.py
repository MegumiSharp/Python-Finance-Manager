# Import the necessary costants and settings used in the application
from config.settings import (MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT, BACKGROUND_PATH, THEMES_PATH, THEMES_TYPE, BACKGROUND_PATH, BACKGROUND_FILE_NAME, KEY_NICKNAME, KEY_THEME, DASHBOARD_FRAME)

# Importing the necessary libraries and view used in the application
from src.views.base_view import BaseView
import customtkinter as ctk
from PIL import Image
import os

# This is the welcome view, where the user can choose a theme and continue to the application (Default view when the application is started)
class WelcomeView(BaseView):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, controller, user)
        self.controller = controller
        self.user = user

        # Create main content frame from the baseview
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        # Configure the main frame to use grid for sidebar and content area
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.setup_ui()

    def setup_ui(self):
        # Create the background image
        self.bg_image = ctk.CTkImage(Image.open(os.path.join(BACKGROUND_PATH, BACKGROUND_FILE_NAME)), size=(MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT))
        self.bg_image_label = ctk.CTkLabel(self.main_frame, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # Create the change theme frame
        self.welcome_frame_widget = ctk.CTkFrame(self.main_frame, corner_radius=0)
        self.welcome_frame_widget.grid(row=0, column=0, sticky="ns")

        # Create the welcome label
        self.welcome_label = ctk.CTkLabel(
            self.welcome_frame_widget, 
            text=f'Welcome {self.user.read_json_value(KEY_NICKNAME)}! \n Choose a theme:',
            font=ctk.CTkFont(size=20, weight="bold"))
        self.welcome_label.grid(row=0, column=0, padx=30, pady=(150, 15))

        # Create the option menu for the themes
        optionmenu_var = ctk.StringVar(value= self.user.read_json_value(KEY_THEME))  # Current theme
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.welcome_frame_widget,
                values=["Default", "NightTrain", "Orange", "SweetKind"],
                command=self.__switch_frame,
                variable= optionmenu_var)
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=30, pady=(150, 15))

        # Create the continue button for passing to the home view
        self.test_button = ctk.CTkButton(self.welcome_frame_widget, text="Continue", command=self.__switch_frame)
        self.test_button.grid(row=2, column=0, padx=20, pady=10)
          
    # When pressing continue or an option in the theme option menu, we want to update the user_settings if needed and switch appearance and view
    def __switch_frame(self, theme = None):
        user_theme_value = self.user.read_json_value(KEY_THEME)

        # This is needed because optionmenu will allways give a variable to the command
        selected_theme = self.appearance_mode_optionemenu.get() if theme is None else theme
        
        # If the optionmenu theme is different from the user_settings one, it means the user clicked the continue button and the theme is changed only for the appearence
        # If not, it means the user clicked the option menu and selected another theme, this mean we need to update the user_settings with the new theme 
        if user_theme_value == selected_theme:
            ctk.set_default_color_theme(os.path.join(THEMES_PATH, THEMES_TYPE[user_theme_value]))
        else:
            ctk.set_default_color_theme(os.path.join(THEMES_PATH, THEMES_TYPE[str(selected_theme)]))
            self.user.change_json_value(KEY_THEME, str(selected_theme))

        self.controller.switch_frame(DASHBOARD_FRAME)