import customtkinter as ctk
from PIL import Image
import os
from config.settings import (KEY_IS_FIRST_TIME, KEY_NICKNAME, KEY_CURRENCY_SIGN,
                             KEY_BUDGET_NEEDS, KEY_BUDGET_WANTS, KEY_BUDGET_SAVING,
                             VALUE_FALSE, DEFAULT_NICKNAME,
                             WINDOW_WIDTH, WINDOW_HEIGHT,
                             BACKGROUND_PATH,
                             WELCOME_FRAME)       

from config.textbox import (WELCOME_HEADER_TEXT, WELCOME_TEXT, 
                            BUDGET_RULE_INFO_TEXT, INPUT_GUIDE_TEXT, INPUT_GUIDELINE_TEXT,
                            ERROR_VAL_RANGE_TEXT, ERROR_VAL_SUM_INCORRECT_TEXT, ERROR_VAL_WHOLE_TEXT)                                     # Import the text for the setup view
from src.views.base_view import BaseView                                                                                                  # Import the BaseView class

# This is the setup view, where the user can configure the application settings, like nickname, currency sign and budget rule percentages
class SetupView(BaseView):
    # This is the constructor of the SetupView class, it initializes the view and sets up the UI
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent, controller, user)
        self.controller = controller
        self.user = user

        # Set the size of the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Sidebar - fixed width
        self.grid_columnconfigure(1, weight=1)  # Main content - expandable

        self.setup_ui()

    # This method sets up the UI of the SetupView
    def setup_ui(self):
        # LEFT SIDE - Sidebar (Column 0)
        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=0)  
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1) 
        self.sidebar_frame.grid_propagate(False) 

        # Title in the sidebar
        self.title_label = ctk.CTkLabel(self.sidebar_frame,  text=WELCOME_HEADER_TEXT, font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Welcome text-box in the sidebar
        self.welcome_textbox = ctk.CTkTextbox(self.sidebar_frame, width=260, height=310) 
        self.welcome_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.welcome_textbox.insert("0.0", WELCOME_TEXT)
        self.welcome_textbox.configure(state="disabled")

        # Nickname section
        self.nickname_label = ctk.CTkLabel(self.sidebar_frame, text="Nickname :", anchor="w")
        self.nickname_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        self.nickname_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Enter your nickname")
        self.nickname_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Currency section (to choose the currency sign)
        self.monetary_symbol_label = ctk.CTkLabel(self.sidebar_frame, text="Currency Sign :", anchor="w")
        self.monetary_symbol_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")

        self.monetary_symbol_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["€", "$", "£"])
        self.monetary_symbol_optionmenu.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Continue button (to save settings and proceed)
        self.continue_btn = ctk.CTkButton(self.sidebar_frame, text="Continue", command=self.__continue_button_from_configuration_frame)
        self.continue_btn.grid(row=6, column=0, padx=20, pady=30, sticky="ew")

        # Error text label (to show validation errors)
        self.error_label = ctk.CTkLabel(self.sidebar_frame, text="", text_color="#BB4E62", anchor="w", font=("Arial", 12, "bold"))
        self.error_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="ew")

        # RIGHT SIDE - Main Content (Column 1) frame
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(0, weight=2)  # Info textbox - more space
        self.main_content_frame.grid_rowconfigure(1, weight=1)  # Budget rule frame - less space
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # Background image as background of main content
        self.bg_image = ctk.CTkImage(Image.open(os.path.join(BACKGROUND_PATH, "background.jpg")), size=(WINDOW_WIDTH-300, WINDOW_HEIGHT))
        self.bg_image_label = ctk.CTkLabel(self.main_content_frame, text="", image=self.bg_image) # Trick to set background image
        self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1) 

        # Info textbox at the top
        self.info_textbox = ctk.CTkTextbox(self.main_content_frame, height=300)
        self.info_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.info_textbox.insert("0.0", BUDGET_RULE_INFO_TEXT)
        self.info_textbox.configure(state="disabled")

        # Budget rule frame at the bottom
        self.budget_rule_frame = ctk.CTkFrame(self.main_content_frame, corner_radius=10)
        self.budget_rule_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.budget_rule_frame.grid_columnconfigure(0, weight=0)
        self.budget_rule_frame.grid_columnconfigure(1, weight=1)

        # Budget rule inputs - left side
        self.needs_label = ctk.CTkLabel(self.budget_rule_frame, text="Needs :", anchor="w")
        self.needs_label.grid(row=0, column=0, padx=(20, 10), pady=(20, 5), sticky="w")

        self.needs_entry = ctk.CTkEntry(self.budget_rule_frame, placeholder_text="50%", width=100)
        self.needs_entry.grid(row=1, column=0, padx=(20, 10), pady=(0, 10), sticky="w")

        self.wants_label = ctk.CTkLabel(self.budget_rule_frame, text="Wants :", anchor="w")
        self.wants_label.grid(row=2, column=0, padx=(20, 10), pady=(10, 5), sticky="w")

        self.wants_entry = ctk.CTkEntry(self.budget_rule_frame, placeholder_text="30%", width=100)
        self.wants_entry.grid(row=3, column=0, padx=(20, 10), pady=(0, 10), sticky="w")

        self.saving_label = ctk.CTkLabel(self.budget_rule_frame, text="Saving :", anchor="w")
        self.saving_label.grid(row=4, column=0, padx=(20, 10), pady=(10, 5), sticky="w")

        self.saving_entry = ctk.CTkEntry(self.budget_rule_frame, placeholder_text="20%", width=100)
        self.saving_entry.grid(row=5, column=0, padx=(20, 10), pady=(0, 20), sticky="w")

        # Input guide frame - right side - Explanation validation and input guide
        self.input_guide_frame = ctk.CTkFrame(self.budget_rule_frame, corner_radius=10)
        self.input_guide_frame.grid(row=0, column=1, rowspan=6, padx=(10, 20), pady=10, sticky="nsew")  
        
        self.input_guide_label = ctk.CTkLabel(
            self.input_guide_frame, 
            text=INPUT_GUIDELINE_TEXT, 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.input_guide_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.input_guide_textbox = ctk.CTkTextbox(self.input_guide_frame, height=120)
        self.input_guide_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.input_guide_textbox.insert("0.0", INPUT_GUIDE_TEXT)
        self.input_guide_textbox.configure(state="disabled")
        
        # Configure the input guide frame grid
        self.input_guide_frame.grid_rowconfigure(1, weight=1)
        self.input_guide_frame.grid_columnconfigure(0, weight=1)

    # Validate the budget rule percentages and update the error label accordingly
    def __check_budgetrule_percentage(self):
        saving = self.saving_entry.get().strip()
        needs = self.needs_entry.get().strip()
        wants = self.wants_entry.get().strip()
        error_text = ""
        
        # Check if all fields are filled
        if not saving and not needs and not wants:
            self.needs_entry.insert(0, "50")
            self.wants_entry.insert(0, "30")
            self.saving_entry.insert(0, "20")
            return True
        else:
            try:
                # Try to convert to integers
                saving_val = int(saving)
                needs_val = int(needs)
                wants_val = int(wants)
                
                # Check if values are within valid range
                if not (1 <= saving_val <= 99) or not (1 <= needs_val <= 99) or not (1 <= wants_val <= 99):
                    error_text = ERROR_VAL_RANGE_TEXT
                # Check if values add up to 100
                elif (saving_val + needs_val + wants_val) != 100:
                    error_text = f"{ERROR_VAL_SUM_INCORRECT_TEXT} {saving_val + needs_val + wants_val}%)"
            except ValueError:
                error_text = ERROR_VAL_WHOLE_TEXT

        # Update error label
        self.error_label.configure(text=error_text)
        
        # Return True if no errors
        return error_text == ""

    def __continue_button_from_configuration_frame(self):
        nickname = self.nickname_entry.get()
        currency_sign = self.monetary_symbol_optionmenu.get()

        # Only proceed if budget rule validation passes
        if self.__check_budgetrule_percentage():
            if not self.nickname_entry.get():
                nickname = DEFAULT_NICKNAME
            
            # Save budget rule values
            saving = self.saving_entry.get().strip()
            needs = self.needs_entry.get().strip()
            wants = self.wants_entry.get().strip()

            # Update user settings
            self.user.change_json_value(KEY_BUDGET_SAVING, saving)
            self.user.change_json_value(KEY_BUDGET_NEEDS, needs)
            self.user.change_json_value(KEY_BUDGET_WANTS, wants)
            self.user.change_json_value(KEY_NICKNAME, nickname)
            self.user.change_json_value(KEY_CURRENCY_SIGN, currency_sign)

            # Mark as not first time
            self.user.change_json_value(KEY_IS_FIRST_TIME, VALUE_FALSE)

            # palle
            self.destroy()
            self.controller.switch_frame(WELCOME_FRAME) 