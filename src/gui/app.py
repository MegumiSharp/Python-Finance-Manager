import customtkinter
import os
from PIL import Image
from CTkTable import *

# Main application GUI, implemented as a class 
class App(customtkinter.CTk):
    def __init__(self, obj):
        super().__init__()
        self.data = obj.local_db

        # Set Windows Settings like appearance and color theme or size and name
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.title("Expensia")
        self.geometry("1280x720")
        self.resizable(False, False)  # Not resizable

        # Set a Grid Layout for placing the frames, this is 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # The the image path of the os and than add the assets folder (so you do not need to write everytim assets/)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        # Assign every image used in the windows to a variables (only dark mode is supported)
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Expensia Logo.png")), size=(32, 32))      # Logo fo the app
        self.home_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))         # Icon Home white
        self.chat_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))         # Icon Chat white
        self.lens_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "search.png")), size=(24, 24))             # Icon for search bar
 
        # Create the sidebar on the left, the navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

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


        # Create all the frame
        self.home_frame()
        self.budget_frame()

        # select default frame
        self.select_frame_by_name("home")


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
        # Create ordering buttons frame
        ordering_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent", height=50)
        ordering_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))
        ordering_frame.grid_propagate(False)
        ordering_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Equal width for all columns
        
        # Ordering buttons for each column
        self.date_order_btn = customtkinter.CTkButton(
            ordering_frame, 
            text="Date ↕", 
            height=35,
            font=customtkinter.CTkFont(size=12),
            command=self.order_by_date
        )
        self.date_order_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        self.amount_order_btn = customtkinter.CTkButton(
            ordering_frame, 
            text="Amount ↕", 
            height=35,
            font=customtkinter.CTkFont(size=12),
            command=self.order_by_amount
        )
        self.amount_order_btn.grid(row=0, column=1, sticky="ew", padx=5)
        
        self.category_order_btn = customtkinter.CTkButton(
            ordering_frame, 
            text="Category ↕", 
            height=35,
            font=customtkinter.CTkFont(size=12),
            command=self.order_by_category
        )
        self.category_order_btn.grid(row=0, column=2, sticky="ew", padx=5)
        
        self.description_order_btn = customtkinter.CTkButton(
            ordering_frame, 
            text="Description ↕", 
            height=35,
            font=customtkinter.CTkFont(size=12),
            command=self.order_by_description
        )
        self.description_order_btn.grid(row=0, column=3, sticky="ew", padx=(5, 0))

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
        
        # Table header
        header_frame = customtkinter.CTkFrame(self.table_scroll, fg_color="#2b2b2b", height=40)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        header_frame.grid_columnconfigure(4, weight=0)  # Delete column doesn't expand
        
        # Header labels
        headers = ["Date", "Amount", "Category", "Description", "Action"]
        for i, header in enumerate(headers):
            label = customtkinter.CTkLabel(
                header_frame, 
                text=header, 
                font=customtkinter.CTkFont(size=14, weight="bold")
            )
            if i == 4:  # Action column
                label.grid(row=0, column=i, padx=10, pady=10, sticky="e")
            else:
                label.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
        
        # Create table rows
        self.create_table_rows()

    # The table is implemented raw for better handling custom design choice and gui choises
    def create_table_rows(self):
        # Create rows for each data entry
        for i, row_data in enumerate(self.data):
            row_frame = customtkinter.CTkFrame(self.table_scroll, fg_color="#2d2d2d", height=50)
            row_frame.grid(row=i+1, column=0, sticky="ew", padx=10, pady=2)
            row_frame.grid_propagate(False)
            row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
            row_frame.grid_columnconfigure(4, weight=0)  # Delete column doesn't expand
            
            # Add data to each column
            for j, data in enumerate(row_data):
                # Color amount based on positive/negative
                if j == 1:  # Amount column
                    color = "green" if float(data) > 0 else "red"
                    label = customtkinter.CTkLabel(
                        row_frame, 
                        text=f"${data}", 
                        font=customtkinter.CTkFont(size=12),
                        text_color=color
                    )
                else:
                    label = customtkinter.CTkLabel(
                        row_frame, 
                        text=data, 
                        font=customtkinter.CTkFont(size=12)
                    )
                label.grid(row=0, column=j, padx=10, pady=15, sticky="ew")
            
            # Add delete button
            delete_btn = customtkinter.CTkButton(
                row_frame, 
                text="Delete", 
                width=60,
                height=25,
                font=customtkinter.CTkFont(size=10),
                fg_color="#d32f2f",
                hover_color="#f44336",
                command=lambda idx=i: self.delete_transaction(idx)
            )
            delete_btn.grid(row=0, column=4, padx=10, pady=15, sticky="e")

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

