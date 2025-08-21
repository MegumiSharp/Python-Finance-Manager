import csv
from datetime import datetime
import os
import shutil

import sys
from tkinter import messagebox
from config.settings import BACKUP_FOLDER_PATH, DATABASE_PATH, EXPORT_FOLDER_PATH, IMPORT_FOLDER_PATH
from config.textbox import IMPORT_EXPORT_MESSAGE
from src.views.base_view import BaseView  
import customtkinter as ctk

from src.utils import helpers

class ImportExport(BaseView):
    def __init__(self, parent, controller=None, user=None, database=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.database = database
        self.data = database.local_db
    
        # Configure the main layout structure
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#2B2B2B")
        self.main_frame.pack(fill="both", expand=True)
        
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # Header section
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#2B2B2B", corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=0)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=0)

        # Budget title
        budget_title = ctk.CTkLabel(
            header_frame,
            text="Import / Export Database",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        budget_title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        # Content frame
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="#404040", corner_radius=10)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_columnconfigure(2, weight=1)


        input_guide_textbox = ctk.CTkTextbox(content_frame)
        input_guide_textbox.grid(row=0, column=0, columnspan=3, padx=30, pady=(30, 10), sticky="nsew")
        input_guide_textbox.insert("0.0", IMPORT_EXPORT_MESSAGE)
        input_guide_textbox.configure(state="disabled")
        

        import_export_frame = ctk.CTkFrame(content_frame, fg_color="transparent", corner_radius=10)
        import_export_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=(0, 20))
        import_export_frame.grid_columnconfigure(0, weight=1)
        import_export_frame.grid_columnconfigure(1, weight=1)

        self.continue_btn = ctk.CTkButton(import_export_frame, text="Import", command=self.import_event)
        self.continue_btn.grid(row=0, column=0, padx=20, pady=30, sticky="n")

        self.continue_btn = ctk.CTkButton(import_export_frame, text="Export", command=self.export_event)
        self.continue_btn.grid(row=0, column=1, padx=20, pady=30, sticky="n")


        backup_frame = ctk.CTkFrame(content_frame, fg_color="transparent", corner_radius=10)
        backup_frame.grid(row=2, column=1, sticky="nsew", padx=20, pady=(0, 20))
        backup_frame.grid_columnconfigure(0, weight=1)
        backup_frame.grid_columnconfigure(1, weight=1)

        self.backup_current = ctk.CTkButton(backup_frame, text="Backup Current", command=self.backup_current_event)
        self.backup_current.grid(row=0, column=0, padx=20, pady=30, sticky="n")

        self.restore_backup = ctk.CTkButton(backup_frame, text="Restore Backup", command= self.restore_backup_event)
        self.restore_backup.grid(row=0, column=1, padx=20, pady=30, sticky="n")

    def restore_backup_event(self):
        if not os.path.isfile(BACKUP_FOLDER_PATH):
            messagebox.showinfo(f"File not founded", f"No file was founded in backup file")
            return

        if messagebox.askokcancel("Confirm", "Are you sure you want to overwrite current database with backup?"):
            shutil.copy(BACKUP_FOLDER_PATH, DATABASE_PATH)
            messagebox.showinfo(f"Backup restored", f"Backup was successfull restored")

            #Reset application to show the changes
            python = sys.executable
            os.execv(python, [python] + sys.argv)

    def backup_current_event(self):
        try:
            shutil.copy(DATABASE_PATH, BACKUP_FOLDER_PATH)
            messagebox.showinfo(f"Backup of the database created", f"Backup successfull created in backup folder")
        except:
            raise ValueError("Error creating backup")

    def import_event(self):
        data =[]
        try:  
            with open(IMPORT_FOLDER_PATH, "r") as csv_file:
                csv_reader = csv.reader(csv_file)

                for index, line in enumerate(csv_reader):
                    
                    if helpers.is_valid_date(line[0]) != True or helpers.is_valid_number(str(line[1])) != True:
                        messagebox.showinfo(f"Error during Import", f"Incorrect value in index {index+1}")
                        break
                    data.append(line)
            
            shutil.copy(DATABASE_PATH, BACKUP_FOLDER_PATH)
            self.database.local_db = data
            self.database.update_db()

            messagebox.showinfo(f"Import Successfull", f"The data was imported from the folder, for every problem, a backup of the previous db was mase in backup folder")

                    #Reset application to show the changes
            python = sys.executable
            os.execv(python, [python] + sys.argv)

        except:
            raise ValueError("Failure Import")



    def export_event(self):
        raw_data = self.database.local_db
        filered_data = [row[1:] for row in raw_data]
        try: 
            with open(EXPORT_FOLDER_PATH, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(filered_data)

            messagebox.showinfo(f"Export Successfull", f"The data was exported as csv file in export folder")
        except:
            raise ValueError("No file founded")
        
    def is_file_legal(self, folder):

        data = []
        with open(folder, "r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                data.append(line)

        for index, row in enumerate(data):
            date = row[0]
            amount = row[1]
            if not self._is_valid_date(date):
                messagebox.showinfo(f"Error in csv data", f"Date is invalid in row {index+1}, \n check csv file and retry")
                break

            if not helpers.is_valid_number(amount):
                messagebox.showinfo(f"Error in csv data", f"Amount is invalid in row {index+1}, \n check csv file and retry")
                break
    

    def _is_valid_date(self, date : str):
        try:
            date_str = date.strip()
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    