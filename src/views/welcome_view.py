import customtkinter as ctk
import os
from PIL import Image
from src.views.base_view import BaseView

from config.settings import (WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_PATH, THEMES_PATH, THEMES_TYPE, BACKGROUND_PATH, BACKGROUND_FILE_NAME, KEY_NICKNAME, KEY_THEME)

# This is the welcome view, where the user can choose a theme and continue to the application (Default view when the application is started)
class WelcomeView(BaseView):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, controller, user)
        self.controller = controller
        self.user = user

        # Set the size of the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # Create the background image
        self.bg_image = ctk.CTkImage(Image.open(os.path.join(BACKGROUND_PATH, BACKGROUND_FILE_NAME)), size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # Create the change theme frame
        self.welcome_frame_widget = ctk.CTkFrame(self, corner_radius=0)
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
                command=self.__switch_theme_event,
                variable= optionmenu_var)
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=30, pady=(150, 15))

        # Create the continue button for passing to the home view
        self.test_button = ctk.CTkButton(self.welcome_frame_widget, text="Continue", command=self.__continue_btn)
        self.test_button.grid(row=2, column=0, padx=20, pady=10)
          
    # This function is called when the continue button is pressed, it sets the theme and passes to the home view
    def __continue_btn(self):
        ctk.set_default_color_theme(os.path.join(THEMES_PATH, THEMES_TYPE[self.user.read_json_value(KEY_THEME)]))
        self.destroy()
        # pass to home view

    # This function is called when the theme is changed, it sets the theme and updates the user settings
    def __switch_theme_event(self, theme: str):
        ctk.set_default_color_theme(os.path.join(THEMES_PATH, THEMES_TYPE[str(theme)]))
        self.user.change_json_value(KEY_THEME, str(theme))
        self.destroy()
        # pass to home view