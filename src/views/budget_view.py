from datetime import datetime
import customtkinter as ctk
from config.settings import COLOR_EXPENSE, COLOR_INCOME, KEY_BUDGET_NEEDS, KEY_BUDGET_SAVING, KEY_BUDGET_WANTS, KEY_CURRENCY_SIGN
from src.views.base_view import BaseView

class BudgetView(BaseView):
    def __init__(self, parent, controller=None, user=None, database=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.data = database.local_db

        self.currency_sign = user.read_json_value(KEY_CURRENCY_SIGN)
        
        # Placeholder variables
        self.needs_percentage = int(user.read_json_value(KEY_BUDGET_NEEDS))
        self.wants_percentage = int(user.read_json_value(KEY_BUDGET_WANTS))
        self.savings_percentage = int(user.read_json_value(KEY_BUDGET_SAVING))
        

        
        #self.budget_filter = "September 2025"
        self.budget_filter = datetime.now().strftime("%Y-%m")
        self.needs_spent = 0
        self.needs_budget = 0
        self.wants_spent = 0
        self.wants_budget = 0
        self.savings_current = 0
        self.savings_budget = 0
        self.total_savings = 0
        self.salary = 0

        # Store references to UI elements for dynamic updates
        self.needs_label = None
        self.needs_bar = None
        self.needs_amount = None
        self.wants_label = None
        self.wants_bar = None
        self.wants_amount = None
        self.savings_label = None
        self.savings_bar = None
        self.savings_amount = None
        self.total_label = None 

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
            text="Budget",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        budget_title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        # Month/Year
        month_label = ctk.CTkLabel(
            header_frame,
            text=self.budget_filter,
            font=ctk.CTkFont(size=18),
            text_color="#B0B0B0"
        )
        month_label.grid(row=0, column=1, sticky="w")

        # Content frame
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="#404040", corner_radius=10)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)

        # Needs section (Green)
        self.needs_label = ctk.CTkLabel(
            content_frame,
            text=f"Needs ({self.needs_percentage}%)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        self.needs_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))

        self.needs_bar = ctk.CTkProgressBar(
            content_frame, 
            height=15, 
            progress_color="#4CAF50",
            fg_color="#2B2B2B"
        )
        self.needs_bar.set(0.77)  # 1150/1500
        self.needs_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 5))

        self.needs_amount = ctk.CTkLabel(
            content_frame,
            text=f"{self.needs_spent}/{self.needs_budget}€",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.needs_amount.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 15))

        # Wants section (Red)
        self.wants_label = ctk.CTkLabel(
            content_frame,
            text=f"Wants ({self.wants_percentage}%)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        self.wants_label.grid(row=3, column=0, sticky="w", padx=20, pady=(5, 5))

        self.wants_bar = ctk.CTkProgressBar(
            content_frame, 
            height=15, 
            progress_color="#F44336",
            fg_color="#2B2B2B"
        )
        self.wants_bar.set(0.89)  # 800/900
        self.wants_bar.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 5))

        self.wants_amount = ctk.CTkLabel(
            content_frame,
            text=f"{self.wants_spent}/{self.wants_budget}€",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.wants_amount.grid(row=5, column=0, sticky="w", padx=20, pady=(0, 15))

        # Savings section (Yellow)
        self.savings_label = ctk.CTkLabel(
            content_frame,
            text=f"Savings ({self.savings_percentage}%)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        self.savings_label.grid(row=6, column=0, sticky="w", padx=20, pady=(5, 5))

        self.savings_bar = ctk.CTkProgressBar(
            content_frame, 
            height=15, 
            progress_color="#FFC107",
            fg_color="#2B2B2B"
        )
        self.savings_bar.set(0.67)  # 400/600
        self.savings_bar.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 5))

        self.savings_amount = ctk.CTkLabel(
            content_frame,
            text=f"{self.savings_current}/{self.savings_budget}€",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.savings_amount.grid(row=8, column=0, sticky="w", padx=20, pady=(0, 15))


        self.salary_label = ctk.CTkLabel(           
            content_frame,
            text=f"Salary: {self.salary}€",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#9DD45D"
        )

        self.salary_label.grid(row=9, column=0, padx=20, pady=(10, 20))

        # Total savings
        self.total_label = ctk.CTkLabel(
            content_frame,
            text=f"Total Savings This Month: {self.total_savings}€",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFC107"
        )
        self.total_label.grid(row=10, column=0, padx=20, pady=(10, 20))
        self.calculator()

    def calculator(self):

        self.needs_spent = 0
        self.needs_budget = 0
        self.wants_spent = 0
        self.wants_budget = 0
        self.savings_current = 0
        self.savings_budget = 0
        self.total_savings = 0
        self.salary = 0

        new_list = []
        for transaction in self.data:
            year_month = transaction[1][0:7]

            if year_month == self.budget_filter:
                new_list.append(transaction)

        
        for transaction in new_list:
            norm = (transaction[2])
            amount = float(norm)
            tag = transaction[3]

            if tag == "Needs":
                self.needs_spent += amount
            elif tag == "Wants":
                self.wants_spent += amount
            elif tag == "Salary":
                self.salary += amount
            elif tag == "Saving":
                self.savings_current += amount

        self.update_display()

    def update_display(self):
        
        self.needs_spent = abs(self.needs_spent)
        self.wants_spent = abs(self.wants_spent)
        self.savings_current = round((abs(self.savings_current)),2)
    
        self.needs_budget = round((self.salary * self.needs_percentage / 100),2)
        self.wants_budget = round((self.salary * self.wants_percentage / 100),2)
        self.savings_budget = round((self.salary * self.savings_percentage / 100),2)

        self.total_savings += self.savings_current
        
        if self.salary_label:
            self.salary_label.configure(text=f"Salary: {self.salary}{self.currency_sign}")


        if self.needs_label:
            self.needs_label.configure(text=f"Needs ({self.needs_percentage}%)")

        if self.needs_amount:
            self.needs_amount.configure(text=f"{self.needs_spent}/{self.needs_budget}{self.currency_sign}")

            if self.needs_spent > self.needs_budget:
                self.needs_amount.configure(text_color=COLOR_EXPENSE)

        if self.needs_bar and self.needs_budget > 0:
            progress = min(self.needs_spent / self.needs_budget, 1.0)
            self.needs_bar.set(progress)
            
        if self.wants_label:
            self.wants_label.configure(text=f"Wants ({self.wants_percentage}%)")




        if self.wants_amount:
            self.wants_amount.configure(text=f"{self.wants_spent}/{self.wants_budget}{self.currency_sign}")

            if self.wants_spent > self.wants_budget:
                self.wants_amount.configure(text_color=COLOR_EXPENSE)



        if self.wants_bar and self.wants_budget > 0:
            progress = min(self.wants_spent / self.wants_budget, 1.0)
            self.wants_bar.set(progress)
            
        if self.savings_label:
            self.savings_label.configure(text=f"Savings ({self.savings_percentage}%)")


        if self.savings_amount:
            self.savings_amount.configure(text=f"{self.savings_current}/{self.savings_budget}{self.currency_sign}")

            if self.savings_current >= self.savings_budget:
                self.savings_amount.configure(text_color=COLOR_INCOME)



        if self.savings_bar and self.savings_budget > 0:
            progress = min(self.savings_current / self.savings_budget, 1.0)
            self.savings_bar.set(progress)
            
        if self.total_label:
            self.total_label.configure(text=f"Total Savings This Month: {self.total_savings}{self.currency_sign}")


