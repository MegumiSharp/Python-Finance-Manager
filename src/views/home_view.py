import customtkinter as ctk
from PIL import Image
import os

# Local imports
from config.settings import (ICONS_PATH,
                             COLOR_BALANCE, COLOR_INCOME, COLOR_EXPENSE, KEY_CURRENCY_SIGN,
                             KEY_SUM_TRANSACTIONS, KEY_SUM_INCOME, KEY_SUM_EXPENSES, KEY_SUM_BALANCE)
from src.views.virtual_table_view import VirtualTable
from src.views.base_view import BaseView
from datetime import datetime


class HomeView(BaseView):
    """
    Main dashboard view containing transaction table, summary panel, and transaction controls.
    Implements filtering, sorting, and CRUD operations for financial transactions.
    """
    
    def __init__(self, parent, controller=None, user=None, database=None):
        super().__init__(parent)
        
        # Core dependencies
        self.controller = controller
        self.user = user
        self.data = database.local_db

        self.currency_sign = self.user.read_json_value(KEY_CURRENCY_SIGN)
        self.label_text = ctk.StringVar(value="Welcome to Expensia!")
        
        # Configure the main layout structure with proper grid weights
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        # Configure grid: left column expands, right column (summary) stays fixed
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)  # Main content expands
        self.main_frame.grid_columnconfigure(1, weight=0)  # Summary panel fixed width

        self.setup_ui()


    # =============================================================================
    # UI SETUP AND LAYOUT
    # =============================================================================
    
    # Initialize all UI components in proper order. Creates main content area and summary panel with responsive layout.
    def setup_ui(self):
        # Left side: main content area (search, filters, table, add form)
        self.main_content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=0, sticky="nsew")
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(2, weight=1)  # Table expands vertically

        # Right side: Summary Frame content area (income, expenses, ec...)
        self.summary_frame = ctk.CTkFrame(self.main_frame, width=250)
        self.summary_frame.grid(row=0, column=1, sticky="nsew")
        self.summary_frame.grid_propagate(False)  # Maintain fixed width
        
        
        # Initialize the transaction table
        self.transactions_table = VirtualTable(self.main_content_frame, self.controller, self.data, self.user)
        self.transactions_table.grid(row=2, column=0, sticky="nsew")


        #self.message_box()
        # Initialize components in correct order
        self.search_bar_frame()
        self.ordering_frame(self.main_content_frame)

        self.add_transaction_frame(self.main_content_frame)
        self.setup_summary_panel()
        self.message_box()
        self.transactions_table.order_by_date()           # Order the widgets by deafult by date and show all widges





    def message_box(self):

        search_container = ctk.CTkFrame(
            self.main_content_frame,
            height=40,
            border_width=4,
            fg_color= "#1a1a1a",
            border_color="#292929",
            corner_radius=16
        )
        search_container.grid(row=5, column=0, sticky="ew", padx=30)
        search_container.grid_propagate(False)
        search_container.grid_columnconfigure(0, weight=1)
        search_container.grid_rowconfigure(0, weight=1)

        self.message_home_view = ctk.CTkLabel(
            search_container,
            font=ctk.CTkFont(size=14),
            textvariable= self.label_text
        )
        self.message_home_view.grid(row=0, column=0, sticky="ew", padx=10, pady=5)


    def change_message_home_view(self, new_message, new_color):
        self.label_text.set(new_message)
        self.message_home_view.configure(text_color = new_color)

    # =============================================================================
    # SEARCH FUNCTIONALITY
    # =============================================================================
    
    # Create a search bar with magnifying glass icon. Uses StringVar with trace callback for real-time search.
    def search_bar_frame(self):
        # Container frame with transparent background
        search_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent", height=60)
        search_frame.grid(row=0, column=0, sticky="ew", padx=30, pady= (0, 8))
        search_frame.grid_propagate(False)
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Search input container with icon overlay
        search_container = ctk.CTkFrame(search_frame, height=40)
        search_container.grid(row=0, column=0, sticky="ew", pady=10)
        search_container.grid_propagate(False)
        search_container.grid_columnconfigure(0, weight=1)
        
        # Search entry with real-time callback
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args : self.transactions_table.show_searched(self.search_var.get()))
        
        self.search_entry = ctk.CTkEntry(
            search_container,
            textvariable=self.search_var,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(5, 35))
        
        self.lens_image = ctk.CTkImage(
            Image.open(os.path.join(ICONS_PATH, "search.png")),
            size=(24, 24)
        )
        lens_icon = ctk.CTkLabel(
            search_container,
            text="",
            image=self.lens_image,
            width=20,
            height=20
        )
        lens_icon.grid(row=0, column=0, sticky="e", padx=(0, 10))

    # =============================================================================
    # SUMMARY PANEL
    # =============================================================================
    
    def setup_summary_panel(self):
        """
        Create summary panel showing transaction statistics and filter controls.
        Uses CTkLabels with dynamic color coding for positive/negative values.
        """
        # Main statistics container
        summary_content = ctk.CTkFrame(self.summary_frame)
        summary_content.grid(row=1, column=0, sticky="sew", padx=20, pady=10)
        summary_content.grid_columnconfigure(0, weight=1)
        
        # Transactions
        transaction_label = ctk.CTkLabel(
            summary_content, 
            text="Transactions:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        transaction_label.grid(row=0, column=0, pady=(8, 4), padx=15, sticky="ew")
        
        transaction_value_label = ctk.CTkLabel(
            summary_content, 
            text="0.00", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        transaction_value_label.grid(row=1, column=0, pady=(0, 16), padx=15, sticky="ew")

        # Income
        income_label = ctk.CTkLabel(
            summary_content, 
            text="Income:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        income_label.grid(row=2, column=0, pady=(8, 4), padx=15, sticky="ew")
        
        income_value_label = ctk.CTkLabel(
            summary_content, 
            text="0.00", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLOR_INCOME  # green for income
        )
        income_value_label.grid(row=3, column=0, pady=(0, 16), padx=15, sticky="ew")

        # Expenses
        expenses_label = ctk.CTkLabel(
            summary_content, 
            text="Expenses:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        expenses_label.grid(row=4, column=0, pady=(8, 4), padx=15, sticky="ew")
        
        expenses_value_label = ctk.CTkLabel(
            summary_content, 
            text="0.00", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLOR_EXPENSE # matte dark red for expenses
        )
        expenses_value_label.grid(row=5, column=0, pady=(0, 16), padx=15, sticky="ew")

        # Balance
        balance_label = ctk.CTkLabel(
            summary_content, 
            text="Balance:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        balance_label.grid(row=6, column=0, pady=(8, 4), padx=15, sticky="ew")
        
        balance_value_label = ctk.CTkLabel(
            summary_content, 
            text="0.00", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLOR_BALANCE  # dark gray for neutral
        )
        balance_value_label.grid(row=7, column=0, pady=(0, 16), padx=15, sticky="ew")

        # Store label references if you want to update them later
        self.summary_labels = {
            KEY_SUM_TRANSACTIONS: transaction_value_label,
            KEY_SUM_INCOME: income_value_label,
            KEY_SUM_EXPENSES: expenses_value_label,
            KEY_SUM_BALANCE: balance_value_label
        }

        # Filter controls section
        self._create_filters_tabs_view()
        
        # Configure layout weights for proper expansion
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_rowconfigure(3, weight=1)
        
        # Initialize with current data (one time use)
        self.transactions_table.register_summary_callback(self.on_summary_updated)

        # We brute force the first update of the summery, (not the best way) 
        self.on_summary_updated(self.transactions_table._calculate_summary())

    # Summary callback function is passed in the virtual table and used to update the labels in summary
    # Summary_data is a dictionary with the values
    def on_summary_updated(self, summary_data):
        self.summary_labels[KEY_SUM_TRANSACTIONS].configure(text=f"{summary_data[KEY_SUM_TRANSACTIONS]}")
        self.summary_labels[KEY_SUM_INCOME].configure(text=f"{summary_data[KEY_SUM_INCOME]:.2f}{self.currency_sign}")
        self.summary_labels[KEY_SUM_EXPENSES].configure(text=f"{summary_data[KEY_SUM_EXPENSES]:.2f}{self.currency_sign}")
        self.summary_labels[KEY_SUM_BALANCE].configure(text=f"{summary_data[KEY_SUM_BALANCE]:.2f}{self.currency_sign}")

        # Dynamic color updates based on balance
        if summary_data['balance'] >= 0:
            self.summary_labels[KEY_SUM_BALANCE].configure(
                text_color=COLOR_INCOME)
        else:
            self.summary_labels[KEY_SUM_BALANCE].configure(
                text_color=COLOR_EXPENSE)

    
    def _create_filters_tabs_view(self):

        # create tabview
        tabview = ctk.CTkTabview(self.summary_frame)
        tabview.grid(row=2, column=0, padx=20, pady=10, sticky="sew")
        tabview.add("Filters")
        tabview.add("Dates")
        tabview.tab("Filters").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        tabview.tab("Dates").grid_columnconfigure(0, weight=1)



        self._create_filter_controls(tabview.tab("Filters"))


        filter_info_frame = ctk.CTkFrame(tabview.tab("Dates"))
        filter_info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        filter_info_frame.grid_columnconfigure(0, weight=1)
        
        # Filter section title
        filter_title = ctk.CTkLabel(
            filter_info_frame,
            text="Dates Filters",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        filter_title.grid(row=0, column=0, pady=4, padx=15, sticky="w")

        optionmenu_1 = ctk.CTkOptionMenu(tabview.tab("Dates"), dynamic_resizing=True,
                                                        values=self.transactions_table.get_dates())
        optionmenu_1.grid(row=1, column=0, padx=20)

        
        optionmenu_1 = ctk.CTkOptionMenu(tabview.tab("Dates"), dynamic_resizing=True,
                                                        values=["All", "Jan", "Feb", "Mar", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"])
        optionmenu_1.grid(row=2, column=0, padx=20, pady=(16,1))




    def _create_filter_controls(self, frame_tab):
        """Create filter information panel with income filter button."""
        filter_info_frame = ctk.CTkFrame(frame_tab)
        filter_info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        filter_info_frame.grid_columnconfigure(0, weight=1)
        
        # Filter section title
        filter_title = ctk.CTkLabel(
            filter_info_frame,
            text="Amount Filters",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        filter_title.grid(row=0, column=0, pady=4, padx=15, sticky="w")
        
        # Income filter button
        self.income_btn = ctk.CTkButton(
            filter_info_frame,
            text="Income",
            fg_color="#2A9221",
            command=self.transactions_table.show_income,
            font=ctk.CTkFont(size=14)
        )
        self.income_btn.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="ew")

        # Expenses filter button
        self.expenses_button = ctk.CTkButton(
            filter_info_frame,
            text="Expenses",
            fg_color="#DB5745",
            command=self.transactions_table.show_expenses,
            font=ctk.CTkFont(size=14)
        )
        self.expenses_button.grid(row=2, column=0, pady=(0, 15), padx=15, sticky="ew")

        # All filter button
        self.all = ctk.CTkButton(
            filter_info_frame,
            text="All",
            command=self.transactions_table.show_all,
            font=ctk.CTkFont(size=14)
        )
        self.all.grid(row=3, column=0, pady=(0, 15), padx=15, sticky="ew")

    




















    # =============================================================================
    # DATABASE OPERATIONS
    # =============================================================================
    
    def save_db_modification(self, action, row_id, date=None, amount=None, tag=None, desc=None):
        """
        Queue database operations for batch processing.
        Improves performance by deferring actual database writes.
        """
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
        """
        Process all queued database operations and clear the queue.
        Called when batch operations need to be committed.
        """
        for txn in self.db_transactions:
            if txn["action"] == "delete":
                self.db.remove_transaction(txn["params"])

        self.db_transactions.clear()






    # =============================================================================
    # DATA OPERATIONS
    # =============================================================================
    
    def on_transaction_deleted(self, transaction_id):
        """
        Handle transaction deletion from virtual table.
        Updates both database and local data copies, then refreshes UI.
        """
        # Remove from database immediately
        self.db.remove_transaction(transaction_id)
        
        # Update local data copies
        self.original_data = [row for row in self.original_data if row[0] != transaction_id]
        self.data = [row for row in self.data if row[0] != transaction_id]
        
        # Refresh UI
        self.update_summary()
        
        print(f"Transaction {transaction_id} deleted from database")

    # =============================================================================
    # FILTERING AND SEARCHING
    # =============================================================================
    
    def apply_filters(self):
        """
        Apply current search and date filters to original data.
        Creates new filtered dataset without modifying original data.
        """
        # Start with complete dataset
        filtered_data = self.original_data.copy()
        
        # Apply date-based filtering
        if self.current_filter != "all":
            filtered_data = self.filter_by_date_range(filtered_data, self.current_filter)

        # Apply text-based search filtering
        if self.current_search:
            filtered_data = self._apply_search_filter(filtered_data)
        
        # Update displayed data and refresh components
        self.data = filtered_data
        self.virtual_table.update_data(self.data)
        self.update_summary()

    def _apply_search_filter(self, data):
        """
        Apply text search across all visible columns.
        Case-insensitive search through date, amount, tag, and description.
        """
        query_lower = self.current_search.lower()
        return [
            row for row in data
            if any(str(field).lower().find(query_lower) != -1 for field in row[1:])
        ]

    def filter_by_date_range(self, data, filter_type):
        """
        Filter transactions by date range (day, month, or year).
        Uses datetime parsing to compare dates accurately.
        """
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

    # =============================================================================
    # TRANSACTION FORM
    # =============================================================================
    
    def add_transaction_frame(self, main_frame):
        """
        Create transaction input form at bottom of main content.
        Uses CTkEntry widgets in a grid layout with validation.
        """
        # Create fixed-height container
        add_frame = ctk.CTkFrame(main_frame, height= 80)
        add_frame.grid(row=4, column=0, sticky="sew", padx=30, pady=8)
        add_frame.grid_propagate(False)
        add_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        
        # Input fields with placeholders
        self._create_transaction_inputs(add_frame)
        
        # Submit button
        self.add_btn = ctk.CTkButton(
            add_frame,
            text="Add Transaction",
            height=30,
            command=self.add_transaction
        )
        self.add_btn.grid(row=2, column=0, columnspan=4, pady=(5, 10), padx=10, sticky="ew")

    def _create_transaction_inputs(self, parent):
        """Create input fields for transaction form with proper sizing."""
        # Date input
        self.date_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Date (YYYY-MM-DD)",
            height=30
        )
        self.date_entry.grid(row=1, column=0, sticky="ew", padx=(10, 5), pady=5)
        
        # Amount input
        self.amount_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Amount",
            height=30
        )
        self.amount_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Category input
        self.category_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Category",
            height=30
        )
        self.category_entry.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        
        # Description input
        self.description_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Description",
            height=30
        )
        self.description_entry.grid(row=1, column=3, sticky="ew", padx=(5, 10), pady=5)

    def add_transaction(self):
        """
        Process new transaction form submission.
        Validates input, adds to database, and refreshes display.
        """
        try:
            # Extract and validate form data
            date = self.date_entry.get()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            
            # Check for required fields
            if not all([date, str(amount), category, description]):
                print("Please fill all fields")
                return
                
            # Validate date format
            datetime.strptime(date, "%Y-%m-%d")
            
            # Add to database and get new ID
            new_id = self.db.add_transaction(date, amount, category, description)
            
            # Update local data
            new_transaction = [new_id, date, amount, category, description]
            self.original_data.append(new_transaction)
            
            # Clear form inputs
            self._clear_transaction_form()
            
            # Refresh display with current filters
            self.apply_filters()
            
            print(f"Added transaction: {date}, ${amount}, {category}, {description}")
            
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding transaction: {e}")

    def _clear_transaction_form(self):
        """Clear all input fields in the transaction form."""
        self.date_entry.delete(0, 'end')
        self.amount_entry.delete(0, 'end')
        self.category_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')

  
    # =============================================================================
    # SORTING AND FILTERING CONTROLS
    # =============================================================================
    
    def ordering_frame(self, main_frame):
        """
        Create header frame with sort buttons and date filter controls.
        Combines column headers with interactive filter buttons.
        """
        # Fixed-height header container
        header_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", height=50)
        header_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))
        header_frame.grid_propagate(False)

        # Configure the main frame columns to ensure proper distribution
        header_frame.grid_columnconfigure(0, weight=15, uniform="col")  # Date column
        header_frame.grid_columnconfigure(1, weight=15, uniform="col")  # Amount column
        header_frame.grid_columnconfigure(2, weight=15, uniform="col")  # Tag column
        header_frame.grid_columnconfigure(3, weight=30, uniform="col")  # Description column (wider)
        header_frame.grid_columnconfigure(4, weight=10, uniform="col")  # Actions column
        header_frame.grid_columnconfigure(5, weight=5, uniform="col")  # Actions column

        # Date button
        date_btn = ctk.CTkButton(
            header_frame,
            text="Date ↕",
            command=self.transactions_table.order_by_date,
            width=80,
            height=32,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        date_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=8)
        
        # Amount button
        amount_btn = ctk.CTkButton(
            header_frame,
            text="Amount ↕",
            command=self.transactions_table.order_by_amount,
            width=80,
            height=32,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        amount_btn.grid(row=0, column=1, sticky="ew", padx=5, pady=8)
        
        # Tag label
        tag_label = ctk.CTkLabel(
            header_frame,
            text="Tag",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        tag_label.grid(row=0, column=2, sticky="ew", padx=10, pady=8)
    
        # Description label
        description_label = ctk.CTkLabel(
            header_frame,
            text="Description",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        description_label.grid(row=0, column=3, sticky="ew", padx=10, pady=8)
    
        # Actions column (empty header)
        actions_label = ctk.CTkLabel(
            header_frame,
            text="Actions",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        actions_label.grid(row=0, column=4, sticky="ew", padx=10, pady=8)

        # empty header
        actions_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        actions_label.grid(row=0, column=5, sticky="ew", padx=10, pady=8)



    def _create_date_filter_buttons(self, parent):
        """Create compact date filter buttons (D, M, Y, All)."""
        filter_buttons = [
            ("D", "day", 5),
            ("M", "month", 6),
            ("Y", "year", 7),
            ("All", "all", 8)
        ]
        
        for text, filter_type, col in filter_buttons:
            btn = ctk.CTkButton(
                parent,
                text=text,
                height=32,
                width=32,
                command=lambda f=filter_type: self.set_date_filter(f),
                font=ctk.CTkFont(size=12 if text == "All" else 14, weight="bold")
            )
            btn.grid(row=0, column=col, padx=5, pady=8)
            
            # Store button reference for color updates
            setattr(self, f"{filter_type}_btn", btn)

    def set_date_filter(self, filter_type):
        """
        Set active date filter and update button visual states.
        Changes button colors to indicate current active filter.
        """
        self.current_filter = filter_type
        
        # Update button colors
        default_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        active_color = "#4CAF50"
        
        # Reset all buttons to default color
        for btn_type in ["day", "month", "year", "all"]:
            btn = getattr(self, f"{btn_type}_btn")
            btn.configure(fg_color=default_color)
        
        # Highlight active filter
        active_btn = getattr(self, f"{filter_type}_btn")
        active_btn.configure(fg_color=active_color)
        
        # Apply the new filter
        self.apply_filters()
