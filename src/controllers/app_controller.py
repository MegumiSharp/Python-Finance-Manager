# Import the necessary costants and settings used in the application
from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME,
    DEFAULT_APPEARANCE_MODE,
    BACKGROUND_PATH, ICONS_PATH, THEMES_PATH,
    THEMES_TYPE,
    KEY_IS_FIRST_TIME, VALUE_TRUE,
    WELCOME_FRAME
)

from src.models.user_settings import UserSettings

# Importing the necessary libraries
import customtkinter
import os
from PIL import Image
from CTkTable import *
import tkinter.messagebox as messagebox
import json


from src.views.setup_view import SetupView

# Main application GUI, implemented as a class
class App(customtkinter.CTk):
    def __init__(self, obj):
        super().__init__()
        self.data = obj.local_db

        # Set Windows Settings like appearance and color theme or size and name
        customtkinter.set_appearance_mode(DEFAULT_APPEARANCE_MODE)

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Block the resizing of the window
        self.grid_propagate(False)
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.maxsize(0, 0)
        self.resizable(width=False, height=False)

        self.user = UserSettings()  # Initialize user settings

        self.__startup()

    def __startup(self):
        # Decide what frame to show to the user, if first time user show setup frame
        if self.user.read_json_value(KEY_IS_FIRST_TIME) == VALUE_TRUE:
            self.setup_view = SetupView(self, controller=self)
            self.setup_view.show()
        else:
           self.switch_frame(WELCOME_FRAME)

        
    def switch_frame(self, frame_name):
        if frame_name == WELCOME_FRAME:
            self.__show_welcome_view()
        else:
            raise ValueError(f"Unknown frame name: {frame_name}")

    def __show_welcome_view(self):
        self.welcome_frame()

    def clear_widgets(self):
        for widget in self.winfo_children():
              widget.destroy()

    
    def welcome_frame(self):
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        # Add background 
        self.bg_image = customtkinter.CTkImage(Image.open(os.path.join(BACKGROUND_PATH, "background.jpg")), size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # Create the change theme frame - CHANGE THE VARIABLE NAME
        self.welcome_frame_widget = customtkinter.CTkFrame(self, corner_radius=0)  # Changed name
        self.welcome_frame_widget.grid(row=0, column=0, sticky="ns")
        self.welcome_label = customtkinter.CTkLabel(self.welcome_frame_widget, text=f'Welcome {self.user.read_json_value("nickname")}! \n Choose a theme:',
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        self.welcome_label.grid(row=0, column=0, padx=30, pady=(150, 15))

        optionmenu_var = customtkinter.StringVar(value= self.user.read_json_value("theme"))  # Current theme
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.welcome_frame_widget,
                                                                    values=["Default", "NightTrain", "Orange", "SweetKind"],
                                                                    command=self.change_appearance_mode_event,
                                                                    variable= optionmenu_var)
        
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=30, pady=(150, 15))

        self.test_button = customtkinter.CTkButton(self.welcome_frame_widget, text="Continue", command=self.continue_button)
        self.test_button.grid(row=2, column=0, padx=20, pady=10)


    def continue_button(self):
        customtkinter.set_default_color_theme(os.path.join(THEMES_PATH, THEMES_TYPE[self.user.read_json_value("theme")]))
        self.create_frames()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_default_color_theme(os.path.join(THEMES_PATH, THEMES_TYPE[str(new_appearance_mode)]))
        self.user.change_json_value("theme", str(new_appearance_mode))
        #self.create_frames()


    def create_frames(self):
        self.clear_widgets()
        
        self.create_navigation_frame()
        self.home_frame()
        self.budget_frame()

        # select default frame
        self.select_frame_by_name("home")


 

    def create_navigation_frame(self):
        # Assign every image used in the windows to a variables (only dark mode is supported)
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(ICONS_PATH, "Expensia Logo.png")), size=(32, 32))      # Logo fo the app
        self.home_image = customtkinter.CTkImage(Image.open(os.path.join(ICONS_PATH, "home_light.png")), size=(20, 20))         # Icon Home white
        self.chat_image = customtkinter.CTkImage(Image.open(os.path.join(ICONS_PATH, "chat_light.png")), size=(20, 20))         # Icon Chat white
        self.lens_image = customtkinter.CTkImage(Image.open(os.path.join(ICONS_PATH, "search.png")), size=(24, 24))             # Icon for search bar
 
        # Create the sidebar on the left, the navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame.grid_rowconfigure(7, weight=1)  # Bottom spacer

        '''The content of the sidebar'''
        ## Name of the App and the logo
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Expensia", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        ## Home button
        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        ## Budget button
        self.budget_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Budget",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.budget_button_event)
        self.budget_button.grid(row=2, column=0, sticky="ew")



    def _on_mousewheel(self, event):
        if event.num == 4:  # Linux scroll up
            self.table_scroll._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.table_scroll._parent_canvas.yview_scroll(1, "units")
        else:  # Windows/macOS
            direction = -1 if event.delta > 0 else 1
            self.table_scroll._parent_canvas.yview_scroll(direction, "units")

    # The home frame should hold the table of transactions a search bar and add transaztion also a method to modify the order
    def home_frame(self):
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)                              # Make the frame expand
        self.home_frame.grid_rowconfigure(2, weight=1)                                 # Make the table row expandable

        self.search_bar_frame(self.home_frame)                                         # Add a search bar in the top of the frame
        self.ordering_frame(self.home_frame)                                           # Add buttons to order the list for every category
        self.table_frame(self.home_frame)           
        self.add_transaction_frame(self.home_frame)                                    # Add at the bottom of the frame a transaction frame to add


    # Create a search bar in a frame
    def search_bar_frame(self, home_frame):
        # Create the frame of the search  on the top of the home frame
        search_frame = customtkinter.CTkFrame(home_frame, fg_color="transparent", height=60)
        search_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        search_frame.grid_propagate(False)
        search_frame.grid_columnconfigure(0, weight=1)  # Make search frame expand
        
        # Create a container for the search entry and lens icon
        search_container = customtkinter.CTkFrame(search_frame, height=40)
        search_container.grid(row=0, column=0, sticky="ew", pady=10)
        search_container.grid_propagate(False)
        search_container.grid_columnconfigure(0, weight=1)
        
        # Search entry
        self.search_var = customtkinter.StringVar()
        self.search_var.trace_add("write", self.on_search)
        self.search_entry = customtkinter.CTkEntry(
            search_container, 
            placeholder_text="Search...", 
            textvariable=self.search_var,
            height=40,
            font=customtkinter.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(5, 35))  # Right padding for lens icon
        
        # Lens icon positioned at the end (inside the search bar area)
        lens_icon = customtkinter.CTkLabel(
            search_container, 
            text="", 
            image=self.lens_image,
            width=20,
            height=20
        )
        lens_icon.grid(row=0, column=0, sticky="e", padx=(0, 10))

    # A function that use the search entry to search in the table, not yet implemented
    def on_search(self, var_name, index, operation):
        search_text = self.search_var.get()
        print(f"Searching for: {search_text}")  # For testing
       
    # The frame witch contains the buttons to order the tabe (The buttons are yet to be implemented)
    def ordering_frame(self, main_frame):
         # Table header with sort buttons
        header_frame = customtkinter.CTkFrame(main_frame, fg_color="#1a1a1a", height=50)
        header_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))
        header_frame.grid_propagate(False)
        
        headers = ["Date", "Amount", "Tag", "Description", "Actions"]
        column_weights = [2, 2, 2, 4, 1]
        
        for i, (header, weight) in enumerate(zip(headers, column_weights)):
            header_frame.grid_columnconfigure(i, weight=weight)
            
            if header in ["Date", "Amount", "Tag"]:
                btn_frame = customtkinter.CTkFrame(header_frame, fg_color="transparent")
                btn_frame.grid(row=0, column=i, sticky="ew", padx=5, pady=8)
                btn_frame.grid_columnconfigure(0, weight=1)
                
                sort_btn = customtkinter.CTkButton(
                    btn_frame,
                    text=f"{header} ↕",
                    command=lambda col=i: self.sort_table(col),
                    height=35,
                    font=customtkinter.CTkFont(size=14, weight="bold")
                )
                sort_btn.grid(row=0, column=0, sticky="ew")
            else:
                label = customtkinter.CTkLabel(
                    header_frame, 
                    text=header, 
                    font=customtkinter.CTkFont(size=14, weight="bold")
                )
                label.grid(row=0, column=i, sticky="ew", padx=10, pady=8)


    # Placeholder ordering functions (no functionality yet)
    def order_by_date(self):
        print("Order by date clicked")

    def order_by_amount(self):
        print("Order by amount clicked")

    def order_by_category(self):
        print("Order by category clicked")
    
    def order_by_description(self):
        print("Order by description clicked")

    # The table frame
    def table_frame(self, main_frame):
        # Table container - this is the main expandable section
        table_container = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        table_container.grid(row=2, column=0, sticky="nsew", padx=30, pady=5)
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

        # Create scrollable frame for table
        self.table_scroll = customtkinter.CTkScrollableFrame(table_container, fg_color="#1a1a1a")
        self.table_scroll.grid(row=0, column=0, sticky="nsew")
        self.table_scroll.grid_columnconfigure(0, weight=1)

        # Enable mouse scroll on the table scrollable frame
        self.table_scroll.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows/macOS
        self.table_scroll.bind_all("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.table_scroll.bind_all("<Button-5>", self._on_mousewheel)    # Linux scroll down

        for widget in self.table_scroll.winfo_children():
            widget.destroy()

        for i in range(5):
            self.table_scroll.grid_columnconfigure(i, weight=1)

        for idx, row in enumerate(self.data):
            self.create_table_row(idx, row)


    def create_table_row(self, row_idx, row_data):
        date = row_data[0]
        amount = float(row_data[1])
        tag = row_data[2]
        desc = row_data[3]

        amount_color = "#ff6b6b" if amount < 0 else "#51cf66"
        amount_text = f"${abs(amount):.2f}" if amount >= 0 else f"-${abs(amount):.2f}"

        customtkinter.CTkLabel(self.table_scroll, text=date).grid(row=row_idx, column=0, sticky="w", padx=10, pady=6)
        customtkinter.CTkLabel(self.table_scroll, text=amount_text, text_color=amount_color).grid(row=row_idx, column=1, sticky="w", padx=10)
        customtkinter.CTkLabel(self.table_scroll, text=tag).grid(row=row_idx, column=2, sticky="w", padx=10)
        customtkinter.CTkLabel(self.table_scroll, text=desc).grid(row=row_idx, column=3, sticky="w", padx=10)

        del_btn = customtkinter.CTkButton(
            self.table_scroll,
            text="Delete",
            width=60,
            height=28,
            fg_color="#ff6b6b",
            hover_color="#ff5252",
            font=customtkinter.CTkFont(size=12),
            command=lambda idx=row_idx: self.confirm_delete(idx)
        )
        del_btn.grid(row=row_idx, column=4, padx=10, pady=6)

    # To implement
    def delete_transaction(self, index):
        # Placeholder function for deleting transaction
        print(f"Delete transaction at index {index}")
        print(f"Transaction to delete: {self.data[index]}")
     
    # The transaction frame
    def add_transaction_frame(self, main_frame):
        # Create add transaction frame at the bottom
        add_frame = customtkinter.CTkFrame(main_frame, height=120)
        add_frame.grid(row=3, column=0, sticky="ew", padx=30, pady=(10, 20))
        add_frame.grid_propagate(False)
        add_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Add transaction label
        add_label = customtkinter.CTkLabel(
            add_frame, 
            text="Add New Transaction", 
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        add_label.grid(row=0, column=0, columnspan=4, pady=(10, 5))
        
        # Input fields
        self.date_entry = customtkinter.CTkEntry(
            add_frame, 
            placeholder_text="Date (YYYY-MM-DD)", 
            height=30
        )
        self.date_entry.grid(row=1, column=0, sticky="ew", padx=(10, 5), pady=5)
        
        self.amount_entry = customtkinter.CTkEntry(
            add_frame, 
            placeholder_text="Amount", 
            height=30
        )
        self.amount_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        self.category_entry = customtkinter.CTkEntry(
            add_frame, 
            placeholder_text="Category", 
            height=30
        )
        self.category_entry.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        
        self.description_entry = customtkinter.CTkEntry(
            add_frame, 
            placeholder_text="Description", 
            height=30
        )
        self.description_entry.grid(row=1, column=3, sticky="ew", padx=(5, 10), pady=5)
        
        # Add button
        self.add_btn = customtkinter.CTkButton(
            add_frame, 
            text="Add Transaction", 
            height=30,
            command=self.add_transaction
        )
        self.add_btn.grid(row=2, column=0, columnspan=4, pady=(5, 10), padx=10, sticky="ew")

    def add_transaction(self):
        # Placeholder function for adding transaction
        print("Add transaction clicked")
        print(f"Date: {self.date_entry.get()}")
        print(f"Amount: {self.amount_entry.get()}")
        print(f"Category: {self.category_entry.get()}")
        print(f"Description: {self.description_entry.get()}")


    # The budget frame should hold the budget of the user divided by the rule 50/30/20
    def budget_frame(self):
        self.budget_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")


    # Select the frame
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.budget_button.configure(fg_color=("gray75", "gray25") if name == "budget" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

        if name == "budget":
            self.budget_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.budget_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def budget_button_event(self):
        self.select_frame_by_name("budget")

