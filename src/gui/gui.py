import customtkinter
import os
from PIL import Image
from CTkTable import *


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

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

        # Create the sidebar on the left, the navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        #The content of the sidebar

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



    # The home frame should hold the table of transactions
    def home_frame(self):
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        self.data = [
            ["2024-01-15", "-50.00", "Food", "Lunch at restaurant"],
            ["2024-01-16", "2500.00", "Salary", "Monthly salary"],
            ["2024-01-17", "-25.99", "Transport", "Gas station"],
            ["2024-01-18", "-120.00", "Shopping", "Groceries"],
            ["2024-01-19", "100.00", "Gift", "Birthday money"],
            ["2024-01-20", "-75.50", "Food", "Dinner with friends"],
        ]

        table = CTkTable(master=self.home_frame, values=self.data)
        table.pack(expand=False, fill="both", padx=20, pady=20)


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


if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()