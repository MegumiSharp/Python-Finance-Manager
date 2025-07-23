import customtkinter as ctk
from CTkTable import *
from pathlib import Path
import tkinter as tk
from datetime import datetime
import tkinter.messagebox as messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()        

        # Set appearance mode and default color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("Expensia")
        self.geometry("1920x1080")
        self.resizable(False, False)  # Not resizable
        
        # Set background color
        self.configure(fg_color="#232935")

        # Configure grid layout (2 columns now)
        self.grid_columnconfigure(0, weight=4)  # Main frame (expanded)
        self.grid_columnconfigure(1, weight=1)  # Right frame
        self.grid_rowconfigure(0, weight=1)
        
        # Create frames
        self.main_frame = ctk.CTkFrame(self, corner_radius=40, fg_color="#0C1826")
        self.right_frame = ctk.CTkFrame(self, corner_radius=40, fg_color="#0C1826")
        
        # Grid frames
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        
        # Configure main frame grid
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)  # Table takes most space
        
        # Temp Sample data with proper structure
        self.data = [
            ["2024-01-15", "-50.00", "Food", "Lunch at restaurant"],
            ["2024-01-16", "2500.00", "Salary", "Monthly salary"],
            ["2024-01-17", "-25.99", "Transport", "Gas station"],
            ["2024-01-18", "-120.00", "Shopping", "Groceries"],
            ["2024-01-19", "100.00", "Gift", "Birthday money"],
            ["2024-01-20", "-75.50", "Food", "Dinner with friends"],
        ]
        
        self.filtered_data = self.data.copy()
        self.sort_reverse = False
        self.current_sort_column = None
        
        #self.setup_main_frame()
        #self.setup_right_frame()
        
        # Create assets directory if it doesn't exist
        assets_dir = Path("assets")
        assets_dir.mkdir(exist_ok=True)

        def setup_main_frame(self):
            pass

        def setup_right_frame(self):
            pass

if __name__ == "__main__":
    try:
        app = App()
        app.attributes('-zoomed', True)                            # Maximize Window
        app.mainloop()
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()