# Import the necessary costants and settings used in the application
import os
from PIL import Image
from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME,
    DEFAULT_THEME, DEFAULT_APPEARANCE_MODE,
    USER_SETTINGS_PATH, BACKGROUND_PATH, ICONS_PATH, THEMES_PATH,
    THEMES_TYPE
)

# Import the Text used in the Welcome Frame and the Budget Rule Frame
from config.textbox import (
    WELCOME_HEADER_TEXT, WELCOME_TEXT, BUDGET_RULE_INFO_TEXT, INPUT_GUIDE_TEXT
)

from src.views.base_view import BaseView
import customtkinter

class SetupView(BaseView):
    def setup_ui(self):
        # Configure the main grid - IMPORTANT!
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Sidebar - fixed width
        self.grid_columnconfigure(1, weight=1)  # Main content - expandable
        
        # LEFT SIDE - Sidebar (Column 0)
        self.sidebar_frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)  # Increased width
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)  # Changed from 10 to 8
        self.sidebar_frame.grid_propagate(False)  # Maintain fixed width

        # Sidebar content
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text=WELCOME_HEADER_TEXT, 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=260, height=310)  # Adjusted size
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.textbox.insert("0.0", WELCOME_TEXT)
        self.textbox.configure(state="disabled")

        # Nickname section
        self.nickname_label = customtkinter.CTkLabel(self.sidebar_frame, text="Nickname :", anchor="w")
        self.nickname_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        self.nickname_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Enter your nickname")
        self.nickname_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Currency section
        self.monetary_symbol_label = customtkinter.CTkLabel(self.sidebar_frame, text="Currency Sign :", anchor="w")
        self.monetary_symbol_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")

        self.monetary_symbol_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["€", "$", "£"])
        self.monetary_symbol_optionmenu.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Continue button
        self.test_button = customtkinter.CTkButton(
            self.sidebar_frame, 
            text="Continue", 
            command=self.continue_button_from_configuration_frame
        )
        self.test_button.grid(row=6, column=0, padx=20, pady=30, sticky="ew")

     

        # Error label
        self.error_label = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text="", 
            text_color="#BB4E62", 
            anchor="w", 
            font=("Arial", 12, "bold")
        )
        self.error_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="nw")

        # RIGHT SIDE - Main Content (Column 1)
        self.main_content_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(0, weight=2)  # Info textbox - more space
        self.main_content_frame.grid_rowconfigure(1, weight=1)  # Budget rule frame - less space
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # Background image as background of main content
        self.bg_image = customtkinter.CTkImage(
            Image.open(os.path.join(BACKGROUND_PATH, "background.jpg")), 
            size=(WINDOW_WIDTH-300, WINDOW_HEIGHT)  # Adjust for new sidebar width
        )
        self.bg_image_label = customtkinter.CTkLabel(self.main_content_frame, text="", image=self.bg_image)
        self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)  # Use place for background

        # Info textbox at the top - BIGGER
        self.info_textbox = customtkinter.CTkTextbox(
            self.main_content_frame, 
            height=300   # Increased height significantly
        )
        self.info_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")  # Changed to nsew
        self.info_textbox.insert("0.0", BUDGET_RULE_INFO_TEXT)
        self.info_textbox.configure(state="disabled")

        # Budget rule frame at the bottom - SMALLER
        self.budget_rule_frame = customtkinter.CTkFrame(self.main_content_frame, corner_radius=10)
        self.budget_rule_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")  # Changed from nsew to ew
        self.budget_rule_frame.grid_columnconfigure(0, weight=0)
        self.budget_rule_frame.grid_columnconfigure(1, weight=1)

        # Budget rule inputs - left side
        self.needs_label = customtkinter.CTkLabel(self.budget_rule_frame, text="Needs :", anchor="w")
        self.needs_label.grid(row=0, column=0, padx=(20, 10), pady=(20, 5), sticky="w")

        self.needs_entry = customtkinter.CTkEntry(self.budget_rule_frame, placeholder_text="50%", width=100)
        self.needs_entry.grid(row=1, column=0, padx=(20, 10), pady=(0, 10), sticky="w")

        self.wants_label = customtkinter.CTkLabel(self.budget_rule_frame, text="Wants :", anchor="w")
        self.wants_label.grid(row=2, column=0, padx=(20, 10), pady=(10, 5), sticky="w")

        self.wants_entry = customtkinter.CTkEntry(self.budget_rule_frame, placeholder_text="30%", width=100)
        self.wants_entry.grid(row=3, column=0, padx=(20, 10), pady=(0, 10), sticky="w")

        self.saving_label = customtkinter.CTkLabel(self.budget_rule_frame, text="Saving :", anchor="w")
        self.saving_label.grid(row=4, column=0, padx=(20, 10), pady=(10, 5), sticky="w")

        self.saving_entry = customtkinter.CTkEntry(self.budget_rule_frame, placeholder_text="20%", width=100)
        self.saving_entry.grid(row=5, column=0, padx=(20, 10), pady=(0, 20), sticky="w")

        # Input guide frame - right side - SMALLER
        self.input_guide_frame = customtkinter.CTkFrame(self.budget_rule_frame, corner_radius=10)
        self.input_guide_frame.grid(row=0, column=1, rowspan=6, padx=(10, 20), pady=10, sticky="nsew")  # Reduced padding
        
        self.input_guide_label = customtkinter.CTkLabel(
            self.input_guide_frame, 
            text="Input Guidelines", 
            font=customtkinter.CTkFont(size=14, weight="bold")  # Smaller font
        )
        self.input_guide_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")  # Reduced padding

        self.input_guide_textbox = customtkinter.CTkTextbox(self.input_guide_frame, height=120)  # Much smaller height
        self.input_guide_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")  # Reduced padding
        self.input_guide_textbox.insert("0.0", INPUT_GUIDE_TEXT)
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
            #WelcomeView.create_welcome_frame()
            #self.change_json_value("first_time", "false")
