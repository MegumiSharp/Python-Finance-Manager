# Importing the necessary libraries and view used in the application
from config.settings import COLOR_EXPENSE, KEY_BUDGET_NEEDS, KEY_BUDGET_SAVING, KEY_BUDGET_WANTS, KEY_CURRENCY_SIGN
from src.views.base_view import BaseView
from datetime import datetime
import customtkinter as ctk

class BudgetView(BaseView):
    def __init__(self, parent, controller=None, user=None, database=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.database = database
        self.data = database.local_db

        self.currency_sign = user.read_json_value(KEY_CURRENCY_SIGN)
        
        # Placeholder variables
        self.needs_percentage = int(user.read_json_value(KEY_BUDGET_NEEDS))
        self.wants_percentage = int(user.read_json_value(KEY_BUDGET_WANTS))
        self.savings_percentage = int(user.read_json_value(KEY_BUDGET_SAVING))
            
        self.budget_filter = datetime.now().strftime("%Y-%m")
        self.needs_spent = 0
        self.needs_budget = 0
        self.wants_spent = 0
        self.wants_budget = 0
        self.savings_budget = 0
        self.saving_spent = 0
        self.salary = 0
        self.monthly_savings_allocated = 0  # Savings allocated from salary this month

        # Store references to UI elements for dynamic updates
        self.needs_label = None
        self.needs_bar = None
        self.needs_amount = None
        self.wants_label = None
        self.wants_bar = None
        self.wants_amount = None
        self.savings_label = None
        self.savings_amount = None

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
        self.needs_bar.set(0.0)
        self.needs_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 5))

        self.needs_amount = ctk.CTkLabel(
            content_frame,
            text=f"{self.needs_spent}/{self.needs_budget}{self.currency_sign}",
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
        self.wants_bar.set(0.0)
        self.wants_bar.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 5))

        self.wants_amount = ctk.CTkLabel(
            content_frame,
            text=f"{self.wants_spent}/{self.wants_budget}{self.currency_sign}",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.wants_amount.grid(row=5, column=0, sticky="w", padx=20, pady=(0, 15))

        # Savings section (Purple)
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
            progress_color="#BF77DB",
            fg_color="#2B2B2B"
        )
        self.savings_bar.set(0.0)
        self.savings_bar.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 5))

        self.savings_amount = ctk.CTkLabel(
            content_frame,
            text=f"{self.saving_spent:.2f}/{self.savings_budget:.2f}{self.currency_sign}",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.savings_amount.grid(row=8, column=0, sticky="w", padx=20, pady=(0, 15))

        # Salary section
        self.salary_label = ctk.CTkLabel(           
            content_frame,
            text=f"Salary: {self.salary}{self.currency_sign}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#9DD45D"
        )
        self.salary_label.grid(row=9, column=0, padx=20, pady=(10, 10))

        # Monthly savings allocated from salary
        self.monthly_savings_label = ctk.CTkLabel(
            content_frame,
            text=f"Savings This Month: {self.monthly_savings_allocated}{self.currency_sign}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFC107"
        )
        self.monthly_savings_label.grid(row=10, column=0, padx=20, pady=(0, 20))

        self.calculator()

    def update_data_and_recalculate(self):
        """Update data from database and recalculate budget values"""
        self.data = self.database.local_db
        self.calculator()

    def calculator(self):
        self.data = self.database.local_db
        # Reset all values
        self.needs_spent = 0
        self.needs_budget = 0
        self.wants_spent = 0
        self.wants_budget = 0
        self.savings_budget = 0
        self.saving_spent = 0
        self.salary = 0
        self.monthly_savings_allocated = 0

        # Filter transactions for current month
        current_month_transactions = []
        for transaction in self.data:
            year_month = transaction[1][0:7]
            if year_month == self.budget_filter:
                current_month_transactions.append(transaction)

        # Process transactions
        for transaction in current_month_transactions:
            amount = float(transaction[2])
            tag = transaction[3]

            if tag == "Needs":
                # Needs should be negative amounts (expenses)
                self.needs_spent += abs(amount)
            elif tag == "Wants":
                # Wants should be negative amounts (expenses)
                self.wants_spent += abs(amount)
            elif tag == "Salary":
                # Salary is positive income
                self.salary += amount
                # Calculate savings allocated from this salary
                monthly_saving = amount * self.savings_percentage / 100
                self.monthly_savings_allocated += monthly_saving
            elif tag == "Saving":
                # Saving transactions are withdrawals from savings (negative amounts like -99)
                # We add the absolute value to track how much was withdrawn
                self.saving_spent += abs(amount)

        self.update_display()

    def update_display(self):
        # Calculate budgets based on salary
        self.needs_budget = round((self.salary * self.needs_percentage / 100), 2)
        self.wants_budget = round((self.salary * self.wants_percentage / 100), 2)
        self.savings_budget = round((self.salary * self.savings_percentage / 100), 2)

        # Update salary label
        if self.salary_label:
            self.salary_label.configure(text=f"Salary: {self.salary:.2f}{self.currency_sign}")

        # Update needs section
        if self.needs_label:
            self.needs_label.configure(text=f"Needs ({self.needs_percentage}%)")

        if self.needs_amount:
            self.needs_amount.configure(text=f"{self.needs_spent:.2f}/{self.needs_budget:.2f}{self.currency_sign}")
            
            if self.needs_spent > self.needs_budget:
                self.needs_amount.configure(text_color=COLOR_EXPENSE)
            else:
                self.needs_amount.configure(text_color="#FFFFFF")

        if self.needs_bar and self.needs_budget > 0:
            progress = min(self.needs_spent / self.needs_budget, 1.0)
            self.needs_bar.set(progress)
        elif self.needs_bar:
            self.needs_bar.set(0.0)
            
        # Update wants section
        if self.wants_label:
            self.wants_label.configure(text=f"Wants ({self.wants_percentage}%)")

        if self.wants_amount:
            self.wants_amount.configure(text=f"{self.wants_spent:.2f}/{self.wants_budget:.2f}{self.currency_sign}")

            if self.wants_spent > self.wants_budget:
                self.wants_amount.configure(text_color=COLOR_EXPENSE)
            else:
                self.wants_amount.configure(text_color="#FFFFFF")

        if self.wants_bar and self.wants_budget > 0:
            progress = min(self.wants_spent / self.wants_budget, 1.0)
            self.wants_bar.set(progress)
        elif self.wants_bar:
            self.wants_bar.set(0.0)

        # Update savings section
        if self.savings_label:
            self.savings_label.configure(text=f"Savings ({self.savings_percentage}%)")

        if self.savings_amount:
            # Show remaining savings (budget - spent)
            remaining_savings = self.savings_budget - self.saving_spent
            self.savings_amount.configure(text=f"{remaining_savings:.2f}/{self.savings_budget:.2f}{self.currency_sign}")

            if remaining_savings < 0:
                self.savings_amount.configure(text_color=COLOR_EXPENSE)
            else:
                self.savings_amount.configure(text_color="#FFFFFF")

        if self.savings_bar and self.savings_budget > 0:
            # Progress bar shows how much is left (reverse logic)
            remaining_savings = self.savings_budget - self.saving_spent
            progress = max(remaining_savings / self.savings_budget, 0.0)
            self.savings_bar.set(progress)
        elif self.savings_bar:
            self.savings_bar.set(1.0)  # Full bar when no budget set
            
        # Update monthly savings allocated label
        if hasattr(self, 'monthly_savings_label') and self.monthly_savings_label:
            self.monthly_savings_label.configure(text=f"Savings This Month: {self.monthly_savings_allocated:.2f}{self.currency_sign}")