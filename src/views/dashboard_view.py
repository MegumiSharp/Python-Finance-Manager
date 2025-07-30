import customtkinter as ctk
from PIL import Image
import os


from config.settings import (ICONS_PATH)

from src.views.base_view import BaseView
from src.views.home_view import HomeView
from src.views.budget_view import BudgetView
from src.models.database import DatabaseManager

from src.utils.helpers import *

# Dashboard with sidebar and menu selection with different frame to show
class DashboardView(BaseView):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.data = DatabaseManager()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main content frame first
        self.main_content = ctk.CTkFrame(self, corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)

        # Initialize current_view to None
        self.current_view = None
        self.home_view = HomeView(self.main_content, self.controller, self.user, self.data)


        self.setup_ui()   

    def setup_ui(self):
        # Configure grid
        # Create sidebar
        self.create_sidebar()
        
        # Initialize with home view
        self.show_home_view()

    def create_sidebar(self):
        # Assign every image used in the windows to a variables (only dark mode is supported)
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "Expensia Logo.png")), size=(32, 32))      # Logo fo the app
        self.home_image = ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "home_light.png")), size=(20, 20))         # Icon Home white
        self.chat_image = ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "chat_light.png")), size=(20, 20))         # Icon Chat white

 
        # Create the sidebar on the left, the navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame.grid_rowconfigure(7, weight=1)  # Bottom spacer

        '''The content of the sidebar'''
        ## Name of the App and the logo
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Expensia", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        ## Home button
        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        ## Budget button
        self.budget_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Budget",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.budget_button_event)
        self.budget_button.grid(row=2, column=0, sticky="ew")

        # Set home as selected initially
        self.selected_button = self.home_button
        self.update_button_selection()

    def home_button_event(self):
        """Handle home button click"""
        self.show_home_view()

    def budget_button_event(self):
        """Handle budget button click"""
        self.show_budget_view()

    # Select the frame
    def update_button_selection(self):
        """Update button appearance to show which is selected"""
        buttons = [self.home_button, self.budget_button]
        
        for button in buttons:
            if button == self.selected_button:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color="transparent")

    def show_home_view(self):
        """Show the home view"""
        self.selected_button = self.home_button
        self.update_button_selection()

        if self.current_view:
            self.current_view.hide()
        
        self.current_view = self.home_view

        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.current_view.show()
    
    def clear_main_content(self):
        """Clear the main content area"""
        if hasattr(self, 'current_view') and self.current_view:
            self.current_view.destroy()
            self.current_view = None

    def show_budget_view(self):
        self.selected_button = self.budget_button
        self.update_button_selection()
        self.current_view.hide()

        self.current_view = BudgetView(self.main_content, self.controller, self.user)
        self.current_view.show()

