import customtkinter
import os
from PIL import Image
from CTkTable import *
import tkinter.messagebox as messagebox
import json
import re

# Main application GUI, implemented as a class 
class App(customtkinter.CTk):
    WIDTH = 1280
    HEIGHT = 720

    THEMES_TYPE = {
        "NightTrain" : "NightTrain.json",
        "Default" : "Default.json",
        "Orange" : "Orange.json",
        "SweetKind" : "Sweetkind.json",
    }
        
    THEMES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "themes")

    
    def __init__(self, obj):
        super().__init__()
        self.data = obj.local_db
        self.user_settings_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../usersettings/user_settings.json")

        # Set Windows Settings like appearance and color theme or size and name
        customtkinter.set_appearance_mode("dark")

        self.title("Expensia")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)  # Not resizable

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        # Decide what frame to show to the user, if first time user show configuration frame
        if self.read_json_value("first_time") == "true":
            self.configuration_frame()
        else:
            self.welcome_frame()

    def clear_widgets(self):
        for widget in self.winfo_children():
              widget.destroy()

    def configuration_frame(self):

        welcome_text = (
            "Your smart companion for tracking transactions and managing your finances.\n\n"
            "In this setup panel, you can:\n"
            "- Customize your currency symbol\n"
            "- Set your account name\n"
            "- Adjust your budget rule values to match your financial goals\n\n"
            "Take a moment to configure everything just the way you like.\n\n"
            "When you're ready, click Continue to get started!"
        )

        budget_rule_info = """
        A smart way to help you track your expenses — Budget Rule

        What is a Budget Rule? A Budget Rule helps you organize your spending by dividing your transactions into 3 simple labels:

        1. Needs – Essentials like rent, food, and bills
        2. Wants – Non-essentials like eating out or games
        3. Savings – Money you set aside for the future or to pay off debt (calculated automatically)

        You choose how much of your total income goes into each label. 50% for Needs, 30% for Wants, 20% for Savings

        This is how it works:

        • In the tag menu you can choose which tags are considered Wants and which are Needs. The Savings label is calculated by default based on what's left. 
        • When you use the special built-in tag "Income", the app will divide that amount using your chosen percentages and apply it to your Budget Rule.
        • By clicking Budget Rule in the sidebar, a dedicated tab opens where you can see how much you've spent in each label and when.

        The app compares your spending with your rules and alerts you if you're going over in any area. 
        You can stick to the classic 50/30/20 split or adjust the percentages to match your lifestyle.
        """

        input_guide_text = """
        Before clicking continue, write a nickname to use in the welcome page, and chose your currency sign for the amount. 
        
        If  no value are insered inside the needs wants saving field,  default value will be used, 50/30/20.
        
        Valid Input Examples:
        • Enter whole numbers only (1-99)
        • Do not include the % symbol
        • All three values must add up to 100"""

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        # Welcome text
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Welcome in Expensia!", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Textbox
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=250, height=260)
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="n")
        self.textbox.insert("0.0", welcome_text)
        self.textbox.configure(state="disabled")

        # Nickname label and entry
        self.nickname_label = customtkinter.CTkLabel(self.sidebar_frame, text="Nickname :", anchor="w")
        self.nickname_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        self.nickname_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Enter your nickname")
        self.nickname_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Currency selector
        self.monetary_symbol_label = customtkinter.CTkLabel(self.sidebar_frame, text="Currency Sign :", anchor="w")
        self.monetary_symbol_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")

        self.monetary_symbol_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["€", "$", "£"])
        self.monetary_symbol_optionmenu.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Continue button
        self.test_button = customtkinter.CTkButton(self.sidebar_frame, text="Continue", command=self.continue_button_from_configuration_frame)
        self.test_button.grid(row=6, column=0, padx=20, pady=30, sticky="ew")

        # Error label placeholder
        self.error_label = customtkinter.CTkLabel(self.sidebar_frame, text="", text_color="#D61A3C", anchor="w", font=("Arial", 12, "bold"))
        self.error_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="nw")

        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.bg_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "background.jpg")), size=(self.WIDTH, self.HEIGHT))
        self.bg_image_label = customtkinter.CTkLabel(self, text="",image=self.bg_image)
        self.bg_image_label.grid(row=0, column=1)

        
        self.textbox = customtkinter.CTkTextbox(self, width=250, height=360)
        self.textbox.grid(row=0, column=1, padx=20, pady=10, sticky="new")
        self.textbox.insert("0.0", budget_rule_info)
        self.textbox.configure(state="disabled")

        self.budget_rule_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.budget_rule_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=(350, 0), sticky="ew")
        self.budget_rule_frame.grid_rowconfigure(10, weight=1)
        self.budget_rule_frame.grid_columnconfigure(0, weight=0)
        self.budget_rule_frame.grid_columnconfigure(1, weight=1)

        # Budget rule entries - left side
        self.needs_label = customtkinter.CTkLabel(self.budget_rule_frame, text="Needs :", anchor="w")
        self.needs_label.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="w")

        self.needs_entry = customtkinter.CTkEntry(self.budget_rule_frame, placeholder_text="50%", width=100)
        self.needs_entry.grid(row=1, column=0, padx=(20, 10), pady=(0, 10), sticky="w")

        self.wants_label = customtkinter.CTkLabel(self.budget_rule_frame, text="Wants :", anchor="w")
        self.wants_label.grid(row=2, column=0, padx=(20, 10), pady=(10, 0), sticky="w")

        self.wants_entry = customtkinter.CTkEntry(self.budget_rule_frame, placeholder_text="30%", width=100)
        self.wants_entry.grid(row=3, column=0, padx=(20, 10), pady=(0, 10), sticky="w")

        self.saving_label = customtkinter.CTkLabel(self.budget_rule_frame, text="Saving :", anchor="w")
        self.saving_label.grid(row=4, column=0, padx=(20, 10), pady=(10, 0), sticky="w")

        self.saving_entry = customtkinter.CTkEntry(self.budget_rule_frame, placeholder_text="20%", width=100)
        self.saving_entry.grid(row=5, column=0, padx=(20, 10), pady=(0, 10), sticky="w")

        # Input guide frame - right side
        self.input_guide_frame = customtkinter.CTkFrame(self.budget_rule_frame, corner_radius=10)
        self.input_guide_frame.grid(row=0, column=1, rowspan=6, padx=(10, 20), pady=10, sticky="nsew")
        
        self.input_guide_label = customtkinter.CTkLabel(self.input_guide_frame, text="Input Guidelines", 
                                                       font=customtkinter.CTkFont(size=16, weight="bold"))
        self.input_guide_label.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="ew")

        self.input_guide_textbox = customtkinter.CTkTextbox(self.input_guide_frame, height=200)
        self.input_guide_textbox.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.input_guide_textbox.insert("0.0", input_guide_text)
        self.input_guide_textbox.configure(state="disabled")
        
        # Configure the input guide frame grid
        self.input_guide_frame.grid_rowconfigure(1, weight=1)
        self.input_guide_frame.grid_columnconfigure(0, weight=1)

    
    def check_budgetrule_percentage(self):
        saving = self.saving_entry.get().strip()
        needs = self.needs_entry.get().strip()
        wants = self.wants_entry.get().strip()
        error_text = ""
        
        # Check if all fields are filled
        if not saving or not needs or not wants:
            self.needs_entry.insert(0, 50)
            self.wants_entry.insert(0, 30)
            self.saving_entry.insert(0, 20)
            return True
        else:
            try:
                # Try to convert to integers
                saving_val = int(saving)
                needs_val = int(needs)
                wants_val = int(wants)
                
                # Check if values are within valid range
                if not (1 <= saving_val <= 99) or not (1 <= needs_val <= 99) or not (1 <= wants_val <= 99):
                    error_text = "Values must be between 1 and 99"
                # Check if values add up to 100
                elif (saving_val + needs_val + wants_val) != 100:
                    error_text = f"Values must add up to 100% (currently: {saving_val + needs_val + wants_val}%)"
                    
            except ValueError:
                error_text = "Values must be whole numbers only"

        # Update error label
        self.error_label.configure(text=error_text)
        
        # Return True if no errors
        return error_text == ""

    def continue_button_from_configuration_frame(self):
        nickname = self.nickname_entry.get()
        currency_sign = self.monetary_symbol_optionmenu.get()

        # Only proceed if budget rule validation passes
        if self.check_budgetrule_percentage():
            self.change_json_value("currency_sign", currency_sign)

            if not self.nickname_entry.get():
                nickname = "User"
            
            self.change_json_value("nickname", nickname)
            
            # Save budget rule values
            saving = int(self.saving_entry.get().strip())
            needs = int(self.needs_entry.get().strip())
            wants = int(self.wants_entry.get().strip())
            
            self.change_json_value("budget_rule_saving", saving)
            self.change_json_value("budget_rule_needs", needs)
            self.change_json_value("budget_rule_wants", wants)
            
            # Proceed to next frame
            self.welcome_frame()
            self.change_json_value("first_time", "false")

    def welcome_frame(self):
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        # Add background 
        self.bg_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "background.jpg")), size=(self.WIDTH, self.HEIGHT))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # Create the change theme frame - CHANGE THE VARIABLE NAME
        self.welcome_frame_widget = customtkinter.CTkFrame(self, corner_radius=0)  # Changed name
        self.welcome_frame_widget.grid(row=0, column=0, sticky="ns")
        self.welcome_label = customtkinter.CTkLabel(self.welcome_frame_widget, text=f'Welcome {self.read_json_value("nickname")}! \n Choose a theme:',
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        self.welcome_label.grid(row=0, column=0, padx=30, pady=(150, 15))

        optionmenu_var = customtkinter.StringVar(value= self.read_json_value("theme"))  # Current theme 
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.welcome_frame_widget, 
                                                                    values=["Default", "NightTrain", "Orange", "SweetKind"],
                                                                    command=self.change_appearance_mode_event,
                                                                    variable= optionmenu_var)
        
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=30, pady=(150, 15))

        self.test_button = customtkinter.CTkButton(self.welcome_frame_widget, text="Continue", command=self.continue_button)
        self.test_button.grid(row=2, column=0, padx=20, pady=10)


    def continue_button(self):
        customtkinter.set_default_color_theme(os.path.join(self.THEMES_PATH, self.THEMES_TYPE[self.read_json_value("theme")]))
        self.create_frames()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_default_color_theme(os.path.join(self.THEMES_PATH, self.THEMES_TYPE[str(new_appearance_mode)]))
        self.change_json_value("theme", str(new_appearance_mode))
        self.create_frames()


    def create_frames(self):
        self.clear_widgets()
        
        self.navigation_frame()
        self.home_frame()
        self.budget_frame()

        # select default frame
        self.select_frame_by_name("home")


    
    def read_json_value(self, key: str):
        with open(self.user_settings_path, "r") as f:
            data = json.load(f)
        
        return str(data[key])
    
    def change_json_value(self, key: str, value:str):
        # Load existing settings or initialize empty dict if file is empty
        try:
            with open(self.user_settings_path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        #update the key in json
        data[key] = value

        # Save the updated settings
        with open(self.user_settings_path, "w") as f:
            json.dump(data, f, indent=4)


    def navigation_frame(self):
        # Assign every image used in the windows to a variables (only dark mode is supported)
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "Expensia Logo.png")), size=(32, 32))      # Logo fo the app
        self.home_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "home_light.png")), size=(20, 20))         # Icon Home white
        self.chat_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "chat_light.png")), size=(20, 20))         # Icon Chat white
        self.lens_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "search.png")), size=(24, 24))             # Icon for search bar
 
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

