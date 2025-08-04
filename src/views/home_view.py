from src.views.base_view import BaseView
import customtkinter as ctk
from PIL import Image
import os
from config.settings import ICONS_PATH
from src.views.virtual_table_view import VirtualTable
from datetime import datetime


class HomeView(BaseView):
    def __init__(self, parent, controller=None, user=None, database=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.db = database
        self.data = self.db.local_db.copy()  # Work with a copy
        self.original_data = self.db.local_db.copy()  # Keep original for filtering
        self.db_transactions = []

        # Current filter state
        self.current_filter = "all"  # all, day, month, year
        self.current_search = ""

        # Create main content frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        # Configure the main frame to use grid - adjusted column weights
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)  # main_content_frame expands
        self.main_frame.grid_columnconfigure(1, weight=0)  # summary_frame stays fixed

        self.setup_ui()

    def save_db_modification(self, action, row_id, date=None, amount=None, tag=None, desc=None):
        if action == "delete":
            self.db_transactions.append({
                "action": action,
                "params": row_id
            })
        else:
            self.db_transactions.append({
                "action": action,
                "params": [date, amount, tag, desc]
            })

    def update_db(self):
        # Process pending database transactions
        for txn in self.db_transactions:
            if txn["action"] == "delete":
                self.db.remove_transaction(txn["params"])
        self.db_transactions.clear()

    def setup_ui(self):
        # Create main content frame (left side) - takes most of the space
        self.main_content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=0, sticky="nsew", pady=(20, 20))  # Added top padding
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(2, weight=1)  # Make table frame stretch vertically

        # Create summary frame (right side) - reduced width
        self.summary_frame = ctk.CTkFrame(self.main_frame, width=250)  # Reduced from 300 to 250
        self.summary_frame.grid(row=0, column=1, sticky="nsew", pady=(20, 20))  # Added top padding
        self.summary_frame.grid_propagate(False)  # Important: prevent the frame from shrinking
        
        # Setup main content components
        self.search_bar_frame(self.main_content_frame)                                         
        self.ordering_frame(self.main_content_frame)                                           

        # Create virtual table with callback
        self.virtual_table = VirtualTable(
            self.main_content_frame, 
            self, 
            self.data,
            on_delete_callback=self.on_transaction_deleted
        )
        self.virtual_table.grid(row=2, column=0, sticky="nsew")
        
        self.add_transaction_frame(self.main_content_frame)
        
        # Setup summary panel
        self.setup_summary_panel()

    def setup_summary_panel(self):
        """Create the summary panel on the right side"""
        # Summary content framei
        summary_content = ctk.CTkFrame(self.summary_frame)
        summary_content.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        summary_content.grid_columnconfigure(0, weight=1)
        

         # Total transactions
        self.total_transactions_label_text = ctk.CTkLabel(
            summary_content,
            text="Transactions:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.total_transactions_label_text.grid(row=0, column=0, pady=(8, 4), padx=15, sticky="ew")

        # Total transactions
        self.total_transactions_label = ctk.CTkLabel(
            summary_content,
            text="0",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.total_transactions_label.grid(row=1, column=0, pady=(0, 16), padx=15, sticky="ew")
        
        # Total income
        self.total_income_label_text = ctk.CTkLabel(
            summary_content,
            text="Income:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.total_income_label_text.grid(row=2, column=0, pady=(8, 4), padx=15, sticky="ew")

        self.total_income_label = ctk.CTkLabel(
            summary_content,
            text="Income:",
            text_color="#2A9221",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.total_income_label.grid(row=3, column=0, pady=(0, 16), padx=15, sticky="ew")
        

        # Total expenses
        self.total_expenses_label_text = ctk.CTkLabel(
            summary_content,
            text="Expenses:",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.total_expenses_label_text.grid(row=4, column=0, pady=(8, 4), padx=15, sticky="ew")

        # Total expenses
        self.total_expenses_label = ctk.CTkLabel(
            summary_content,
            text="$0.00",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="red"
        )
        self.total_expenses_label.grid(row=5, column=0, pady=(0, 16), padx=15, sticky="ew")
        
        # Net balance
        self.net_balance_label_text = ctk.CTkLabel(
            summary_content,
            text="Balance:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.net_balance_label_text.grid(row=6, column=0, pady=(8, 4), padx=15, sticky="ew")

                # Net balance
        self.net_balance_label = ctk.CTkLabel(
            summary_content,
            text="$0.00",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.net_balance_label.grid(row=7, column=0, pady=(0, 16), padx=15, sticky="ew")
        
        # Filter info
        filter_info_frame = ctk.CTkFrame(self.summary_frame)
        filter_info_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        filter_info_frame.grid_columnconfigure(0, weight=1)
        
        filter_title = ctk.CTkLabel(
            filter_info_frame,
            text="Current Filter",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        filter_title.grid(row=0, column=0, pady=(15, 5), padx=15, sticky="w")
        
        self.income_btn = ctk.CTkButton(
            filter_info_frame,
            text="Income",
            fg_color= "#2A9221",
            command = self.show_income,
            font=ctk.CTkFont(size=14)
        )
        self.income_btn.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="ew")
        
        # Make the summary frame expandable
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_rowconfigure(3, weight=1)  # Add flexible space at bottom
        
        # Initial summary update
        self.update_summary()

    def update_summary(self):
        """Update the summary panel with current data statistics"""
        if not self.data:
            self.total_transactions_label.configure(text="0")
            self.total_income_label.configure(text="$0.00")
            self.total_expenses_label.configure(text="$0.00")
            self.net_balance_label.configure(text="$0.00")
            return
        
        total_count = len(self.data)
        total_income = sum(float(row[2]) for row in self.data if float(row[2]) > 0)
        total_expenses = sum(abs(float(row[2])) for row in self.data if float(row[2]) < 0)
        net_balance = total_income - total_expenses
        
        # Update labels
        self.total_transactions_label.configure(text=f"{total_count}")
        self.total_income_label.configure(text=f"${total_income:.2f}")
        self.total_expenses_label.configure(text=f"${total_expenses:.2f}")
        
        # Color code the net balance
        balance_color = "#2A9221" if net_balance >= 0 else "red"
        self.net_balance_label.configure(
            text=f"${net_balance:.2f}",
            text_color=balance_color
        )

    def show_income(self):
        self.sort_table(2, False)

        self.update_summary()

        

    def on_transaction_deleted(self, transaction_id):
        """Handle transaction deletion from virtual table"""
        # Remove from database
        self.db.remove_transaction(transaction_id)
        
        # Update our data copies
        self.original_data = [row for row in self.original_data if row[0] != transaction_id]
        self.data = [row for row in self.data if row[0] != transaction_id]
        
        # Update summary
        self.update_summary()
        
        print(f"Transaction {transaction_id} deleted from database")

    def apply_filters(self):
        """Apply current search and date filters"""
        # Start with original data
        filtered_data = self.original_data.copy()
        
        # Apply date filter
        if self.current_filter != "all":
            filtered_data = self.filter_by_date_range(filtered_data, self.current_filter)

        # Apply search filter
        if self.current_search:
            query_lower = self.current_search.lower()
            filtered_data = [
                row for row in filtered_data
                if any(str(field).lower().find(query_lower) != -1 for field in row[1:])
            ]
        
        # Update data and refresh table
        self.data = filtered_data
        self.virtual_table.update_data(self.data)
        
        # Update summary
        self.update_summary()

    def filter_by_date_range(self, data, filter_type):
        """Filter data by date range"""
        now = datetime.now()
        
        if filter_type == "year":
            target_year = now.year
            return [
                row for row in data
                if datetime.strptime(row[1], "%Y-%m-%d").year == target_year
            ]
        elif filter_type == "month":
            target_year, target_month = now.year, now.month
            return [
                row for row in data
                if (datetime.strptime(row[1], "%Y-%m-%d").year == target_year and
                    datetime.strptime(row[1], "%Y-%m-%d").month == target_month)
            ]
        elif filter_type == "day":
            target_date = now.strftime("%Y-%m-%d")
            return [
                row for row in data
                if row[1] == target_date
            ]
        else:  # "all"
            return data

    # The transaction frame
    def add_transaction_frame(self, main_frame):
        # Create add transaction frame at the bottom
        add_frame = ctk.CTkFrame(main_frame, height=120)
        add_frame.grid(row=4, column=0, sticky="ew", padx=30, pady=(10, 20))
        add_frame.grid_propagate(False)
        add_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Add transaction label
        add_label = ctk.CTkLabel(
            add_frame, 
            text="Add New Transaction", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        add_label.grid(row=0, column=0, columnspan=4, pady=(10, 5))
        
        # Input fields
        self.date_entry = ctk.CTkEntry(
            add_frame, 
            placeholder_text="Date (YYYY-MM-DD)", 
            height=30
        )
        self.date_entry.grid(row=1, column=0, sticky="ew", padx=(10, 5), pady=5)
        
        self.amount_entry = ctk.CTkEntry(
            add_frame, 
            placeholder_text="Amount", 
            height=30
        )
        self.amount_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        self.category_entry = ctk.CTkEntry(
            add_frame, 
            placeholder_text="Category", 
            height=30
        )
        self.category_entry.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        
        self.description_entry = ctk.CTkEntry(
            add_frame, 
            placeholder_text="Description", 
            height=30
        )
        self.description_entry.grid(row=1, column=3, sticky="ew", padx=(5, 10), pady=5)
        
        # Add button
        self.add_btn = ctk.CTkButton(
            add_frame, 
            text="Add Transaction", 
            height=30,
            command=self.add_transaction
        )
        self.add_btn.grid(row=2, column=0, columnspan=4, pady=(5, 10), padx=10, sticky="ew")

    def add_transaction(self):
        """Add new transaction and refresh table"""
        try:
            # Get input values
            date = self.date_entry.get()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            
            # Validate inputs
            if not all([date, str(amount), category, description]):
                print("Please fill all fields")
                return
                
            # Validate date format
            datetime.strptime(date, "%Y-%m-%d")
            
            # Add to database (you'll need to implement this in your db class)
            new_id = self.db.add_transaction(date, amount, category, description)
            
            # Add to our data
            new_transaction = [new_id, date, amount, category, description]
            self.original_data.append(new_transaction)
            
            # Clear input fields
            self.date_entry.delete(0, 'end')
            self.amount_entry.delete(0, 'end')
            self.category_entry.delete(0, 'end')
            self.description_entry.delete(0, 'end')
            
            # Refresh table with current filters
            self.apply_filters()
            
            print(f"Added transaction: {date}, ${amount}, {category}, {description}")
            
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding transaction: {e}")

    # Create a search bar in a frame
    def search_bar_frame(self, home_frame):
        # Create the frame of the search on the top of the home frame
        search_frame = ctk.CTkFrame(home_frame, fg_color="transparent", height=60)
        search_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        search_frame.grid_propagate(False)
        search_frame.grid_columnconfigure(0, weight=1)  # Make search frame expand
        
        # Create a container for the search entry and lens icon
        search_container = ctk.CTkFrame(search_frame, height=40)
        search_container.grid(row=0, column=0, sticky="ew", pady=10)
        search_container.grid_propagate(False)
        search_container.grid_columnconfigure(0, weight=1)
        
        # Search entry
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.on_search)
        self.search_entry = ctk.CTkEntry(
            search_container, 
            placeholder_text="Search...", 
            textvariable=self.search_var,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(5, 35))  # Right padding for lens icon
        
        self.lens_image = ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "search.png")), size=(24, 24))
        # Lens icon positioned at the end (inside the search bar area)
        lens_icon = ctk.CTkLabel(
            search_container, 
            text="", 
            image=self.lens_image,
            width=20,
            height=20
        )
        lens_icon.grid(row=0, column=0, sticky="e", padx=(0, 10))

    def on_search(self, var_name, index, operation):
        """Handle search input changes"""
        self.current_search = self.search_var.get()
        self.apply_filters()

    # The frame which contains the buttons to order the table and date filters
    def ordering_frame(self, main_frame):
        # Table header with sort buttons
        header_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", height=50)
        header_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))
        header_frame.grid_propagate(False)
        
        headers = ["Date", "Amount", "Tag", "Description", ""]
        column_weights = [2, 2, 2, 4, 1]

        # Date filter buttons (D = Day, M = Month, Y = Year)
        self.day_btn = ctk.CTkButton(
            header_frame, 
            text="D", 
            height=32,
            width=32,
            command=lambda: self.set_date_filter("day"),
            font=ctk.CTkFont(size=14, weight="bold"),
            hover=True
        )
        self.day_btn.grid(row=0, column=5, padx=5, pady=8)

        self.month_btn = ctk.CTkButton(
            header_frame, 
            text="M",
            height=32,
            width=32,
            command=lambda: self.set_date_filter("month"),
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.month_btn.grid(row=0, column=6, padx=5, pady=8)

        self.year_btn = ctk.CTkButton(
            header_frame, 
            text="Y", 
            height=32,
            width=32,
            command=lambda: self.set_date_filter("year"),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.year_btn.grid(row=0, column=7, padx=5, pady=8)

        # All transactions button
        self.all_btn = ctk.CTkButton(
            header_frame, 
            text="All", 
            height=32,
            width=32,
            command=lambda: self.set_date_filter("all"),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.all_btn.grid(row=0, column=8, padx=5, pady=8)

        # Column headers and sort buttons
        for i, (header, weight) in enumerate(zip(headers, column_weights)):
            header_frame.grid_columnconfigure(i, weight=weight)
            
            if header in ["Date", "Amount", "Tag"]:
                btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
                btn_frame.grid(row=0, column=i, sticky="ew", padx=5, pady=8)
                btn_frame.grid_columnconfigure(0, weight=1)
                
                sort_btn = ctk.CTkButton(
                    btn_frame,
                    text=f"{header} ↕",
                    command=lambda col=i+1: self.sort_table(col),  # +1 because data columns start at index 1
                    width=24,
                    height=32,
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                sort_btn.grid(row=0, column=0, sticky="ew")
            else:
                label = ctk.CTkLabel(
                    header_frame, 
                    text=header, 
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                label.grid(row=0, column=i, sticky="ew", padx=10, pady=8)

    def set_date_filter(self, filter_type):
        """Set the current date filter and update button colors"""
        self.current_filter = filter_type
        
        # Reset all button colors
        default_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        active_color = "#4CAF50"  # Green for active filter
        
        self.day_btn.configure(fg_color=default_color)
        self.month_btn.configure(fg_color=default_color)
        self.year_btn.configure(fg_color=default_color)
        self.all_btn.configure(fg_color=default_color)
        
        # Highlight active filter
        if filter_type == "day":
            self.day_btn.configure(fg_color=active_color)
        elif filter_type == "month":
            self.month_btn.configure(fg_color=active_color)
        elif filter_type == "year":
            self.year_btn.configure(fg_color=active_color)
        elif filter_type == "all":
            self.all_btn.configure(fg_color=active_color)
        
        # Apply the filter
        self.apply_filters()

    def sort_table(self, column_index, boolean = None):
        """Sort the table by column"""
        self.virtual_table.sort_data(column_index, boolean)