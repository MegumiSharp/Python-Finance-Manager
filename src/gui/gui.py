import customtkinter as ctk
from CTkTable import *
from pathlib import Path

class App(ctk.CTk):
    def __init__(self):
        super().__init__()        # Set appearance mode and default color theme
        ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"
        ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

        self.title("Expensia")
        self.geometry(f"{1280}x{720}")
        
        # Set background color
        self.configure(fg_color="#232935")  # Dynamic background color

        # configure grid layout (3x3)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)


        # Create sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=325, height=481, corner_radius=40, fg_color= "#0C1826")

        self.middle_frame = ctk.CTkFrame(self, width=325, height=481, corner_radius=40, fg_color= "#0C1826")
        self.right_frame = ctk.CTkFrame(self, width=325, height=481, corner_radius=40, fg_color= "#0C1826")


        # Set the sidebar at the center of the first column with padding
        self.sidebar_frame.grid(
            row=0, column=0, rowspan=3, sticky="nesw", padx=20, pady=20)

        self.middle_frame.grid(
            row=0, column=1, rowspan=1, sticky="nesw", padx=20, pady=20)
        

        self.right_frame.grid(
            row=0, column=2, rowspan=1, sticky="nesw", padx=20, pady=20)
        

        value = [[1,2,3,4,5],
                [1,2,3,4,5],
                [1,2,3,4,5],
                [1,2,3,4,5],
                [1,2,3,4,5]]

        table = CTkTable(master=self.middle_frame, row=5, column=5, values=value)
        table.pack(expand=True, fill="both", padx=20, pady=20)

        # Create assets directory if it doesn't exist
        assets_dir = Path("assets")
        assets_dir.mkdir(exist_ok=True)


if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()