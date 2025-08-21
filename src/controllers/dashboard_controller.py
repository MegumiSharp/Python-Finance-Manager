import customtkinter as ctk
from PIL import Image
import os

from config.settings import (ICONS_PATH)
from src.views.base_view import BaseView
from src.views.home_view import HomeView
from src.views.budget_view import BudgetView
from src.views.import_export_view import ImportExport
from src.models.database import DatabaseManager 
from src.utils.helpers import *

# A controller of the dashboard views, it contain the navigation sidebar and it create the views and control the switching between them
class DashboardController(BaseView):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.data = DatabaseManager()
        self.current_view = None

        # Create main content frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        # Configure the main frame to use grid for sidebar and content area
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=0)  # Sidebar - fixed width
        self.main_frame.grid_columnconfigure(1, weight=1)  # Main content - expandable

        # Create a content container for the views (this will use pack)
        self.content_container = ctk.CTkFrame(self.main_frame, corner_radius=0)
        self.content_container.grid(row=0, column=1, sticky="nsew")

        # Initialize button variables first
        self.buttons = {}
        
        self.icons = {
            HomeView: ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "home_light.png")), size=(20, 20)),
            BudgetView: ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "chat_light.png")), size=(20, 20)),
            ImportExport: ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "imp-exp.png")), size=(20, 20)),
        }
        
        # Create views after buttons are created
        self.views = {
            HomeView: HomeView(self.content_container, controller=self.controller, user=self.user, database=self.data),
            BudgetView: BudgetView(self.content_container, controller=self.controller, user=self.user, database=self.data),
            ImportExport: ImportExport(self.content_container, controller=self.controller, user=self.user, database=self.data)
        }

        self.setup_ui()

        # Start with the HomeView
        self.switch_main_content_frame(HomeView)


    # Function to set up the UI sidebar of the DashboardController
    def setup_ui(self):
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "Expensia Logo.png")), size=(32, 32))

        # Create the sidebar on the left
        self.navigation_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, width=300)
        self.navigation_frame.grid_rowconfigure(0, weight=0)  # Logo row
        self.navigation_frame.grid_rowconfigure(1, weight=0)  # Home button
        self.navigation_frame.grid_rowconfigure(2, weight=0)  # Budget button  
        self.navigation_frame.grid_rowconfigure(3, weight=0)  # Future buttons
        self.navigation_frame.grid_rowconfigure(4, weight=0)  # Future buttons
        self.navigation_frame.grid_rowconfigure(5, weight=1)  # Empty space
        self.navigation_frame.grid(row=0, column=0, sticky="ns")
        
        # App name and logo
        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame, 
            text="  Expensia", 
            image=self.logo_image,
            compound="left", 
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Home button
        self.home_button = self.__create_button(frame =self.navigation_frame, text = "Home", istance = HomeView,)
        self.home_button.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.buttons[HomeView] = self.home_button
        
        # Budget button
        self.budget_button = self.__create_button(frame =self.navigation_frame, text = "Budget", istance = BudgetView,)
        self.budget_button.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.buttons[BudgetView] = self.budget_button

        # Import Export Button
        self.import_export_btn = self.__create_button(frame =self.navigation_frame, text = "Import/Export", istance = ImportExport,)
        self.import_export_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        self.buttons[ImportExport] = self.import_export_btn

    # Function to create a generic button for the sidebar
    # It initializes the button with the provided frame, text, and instance type
    def __create_button(self, frame, text, istance):
        self.new_button = ctk.CTkButton(
            frame, 
            corner_radius=20, 
            height=40, 
            border_spacing=10, 
            text=text,
            fg_color="transparent", 
            text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"),
            image=self.icons[istance], 
            anchor="w", 
            command=lambda: self.switch_main_content_frame(istance)
        )
        # Initialize the button in the buttons dictionary
        self.buttons[istance] = None
        return self.new_button
 
    # This function is used to update the button appearance when switching views
    # It assumes that buttons are stored in a dictionary with view classes as keys
    def __update_button_selection(self, view_class):
        # Validate that the view_class exists in buttons
        if view_class not in self.buttons:
            return
        
        # Get the selected button
        self.current_button = self.buttons[view_class]
        
        # Update all button states
        for button_view_class, button in self.buttons.items():
            if button_view_class == view_class:
                # Highlight the selected button
                button.configure(fg_color=("gray75", "gray25"))
            else:
                # Make other buttons transparent
                button.configure(fg_color="transparent")

    # Function to switch the main content frame to the specified view class
    # It updates the button selection and shows the new view
    def switch_main_content_frame(self, view_class):
        # Only update button selection if buttons dictionary exists
        if hasattr(self, 'buttons') and self.buttons:
            self.__update_button_selection(view_class)

        if self.current_view:
            self.current_view.hide()

        # Change the current_view to the class and use the abstract method show() to show it
        if view_class in self.views:
            self.current_view = self.views[view_class]
            self.current_view.show()

        # When switching to BudgetView, update data and recalculate
        if view_class == BudgetView:
            self.views[BudgetView].update_data_and_recalculate()

        if view_class == HomeView:
            self.views[HomeView].change_message_home_view("Welcome to Expensia", "#FFFFFF")

    def on_closure(self):
        self.views[HomeView].on_closure()