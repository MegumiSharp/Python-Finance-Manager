import customtkinter as ctk
from PIL import Image
import os

# Local imports
from config.settings import ICONS_PATH
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
        self.db = database
        
        # Data management - working with copies for filtering performance
        self.data = self.db.local_db.copy()
        self.original_data = self.db.local_db.copy()
        self.db_transactions = []  # Pending database operations queue
        
        # Filter and search state
        self.current_filter = "all"  # Options: all, day, month, year
        self.current_search = ""
        
        # Initialize UI layout
        self._setup_main_layout()
        self.setup_ui()

    def _setup_main_layout(self):
        """Configure the main layout structure with proper grid weights."""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        # Configure grid: left column expands, right column (summary) stays fixed
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)  # Main content expands
        self.main_frame.grid_columnconfigure(1, weight=0)  # Summary panel fixed width

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
    # UI SETUP AND LAYOUT
    # =============================================================================
    
    def setup_ui(self):
        """
        Initialize all UI components in proper order.
        Creates main content area and summary panel with responsive layout.
        """
        # Left side: main content area (search, filters, table, add form)
        self._create_main_content_area()
        
        # Right side: summary statistics panel
        self._create_summary_panel()
        
        # Initialize components in correct order
        self.search_bar_frame(self.main_content_frame)
        self.ordering_frame(self.main_content_frame)
        self._create_virtual_table()
        self.add_transaction_frame(self.main_content_frame)
        self.setup_summary_panel()

    def _create_main_content_area(self):
        """Create the main content frame with proper grid configuration."""
        self.main_content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=0, sticky="nsew", pady=(20, 20))
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(2, weight=1)  # Table expands vertically

    def _create_summary_panel(self):
        """Create the fixed-width summary panel on the right side."""
        self.summary_frame = ctk.CTkFrame(self.main_frame, width=250)
        self.summary_frame.grid(row=0, column=1, sticky="nsew", pady=(20, 20))
        self.summary_frame.grid_propagate(False)  # Maintain fixed width

    def _create_virtual_table(self):
        """Initialize the virtual scrolling table with delete callback."""
        self.virtual_table = VirtualTable(
            self.main_content_frame,
            self,
            self.data,
            on_delete_callback=self.on_transaction_deleted
        )
        self.virtual_table.grid(row=2, column=0, sticky="nsew")

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
        summary_content.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        summary_content.grid_columnconfigure(0, weight=1)

        # Transaction count display
        self._create_summary_stat(summary_content, "Transactions:", "total_transactions", 0, 1)
        
        # Income display with green color
        self._create_summary_stat(summary_content, "Income:", "total_income", 2, 3, "#2A9221")
        
        # Expenses display with red color
        self._create_summary_stat(summary_content, "Expenses:", "total_expenses", 4, 5, "red")
        
        # Net balance with dynamic color based on value
        self._create_summary_stat(summary_content, "Balance:", "net_balance", 6, 7)

        # Filter controls section
        self._create_filter_controls()
        
        # Configure layout weights for proper expansion
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_rowconfigure(3, weight=1)
        
        # Initialize with current data
        self.update_summary()

    def _create_summary_stat(self, parent, label_text, attr_prefix, label_row, value_row, color=None):
        """
        Helper method to create consistent summary statistic displays.
        Creates label-value pairs with optional color coding.
        """
        # Label
        label = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.grid(row=label_row, column=0, pady=(8, 4), padx=15, sticky="ew")
        
        # Value
        value_label = ctk.CTkLabel(
            parent, 
            text="$0.00", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        if color:
            value_label.configure(text_color=color)
        
        value_label.grid(row=value_row, column=0, pady=(0, 16), padx=15, sticky="ew")
        
        # Store reference for updates
        setattr(self, f"{attr_prefix}_label_text", label)
        setattr(self, f"{attr_prefix}_label", value_label)

    def _create_filter_controls(self):
        """Create filter information panel with income filter button."""
        filter_info_frame = ctk.CTkFrame(self.summary_frame)
        filter_info_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        filter_info_frame.grid_columnconfigure(0, weight=1)
        
        # Filter section title
        filter_title = ctk.CTkLabel(
            filter_info_frame,
            text="Current Filter",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        filter_title.grid(row=0, column=0, pady=(15, 5), padx=15, sticky="w")
        
        # Income filter button
        self.income_btn = ctk.CTkButton(
            filter_info_frame,
            text="Income",
            fg_color="#2A9221",
            command=self.show_income,
            font=ctk.CTkFont(size=14)
        )
        self.income_btn.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="ew")

    def update_summary(self):
        """
        Recalculate and update all summary statistics based on current filtered data.
        Handles empty data gracefully and applies color coding to balance.
        """
        if not self.data:
            self._set_empty_summary()
            return
        
        # Calculate statistics from current filtered data
        total_count = len(self.data)
        total_income = sum(float(row[2]) for row in self.data if float(row[2]) > 0)
        total_expenses = sum(abs(float(row[2])) for row in self.data if float(row[2]) < 0)
        net_balance = total_income - total_expenses
        
        # Update display labels
        self.total_transactions_label.configure(text=f"{total_count}")
        self.total_income_label.configure(text=f"${total_income:.2f}")
        self.total_expenses_label.configure(text=f"${total_expenses:.2f}")
        
        # Dynamic color coding for balance
        balance_color = "#2A9221" if net_balance >= 0 else "red"
        self.net_balance_label.configure(
            text=f"${net_balance:.2f}",
            text_color=balance_color
        )

    def _set_empty_summary(self):
        """Set all summary values to zero when no data is available."""
        self.total_transactions_label.configure(text="0")
        self.total_income_label.configure(text="$0.00")
        self.total_expenses_label.configure(text="$0.00")
        self.net_balance_label.configure(text="$0.00")

    def show_income(self):
        """
        Filter to show only income transactions by sorting amount descending.
        Triggers table sort and summary update.
        """
        self.sort_table(2, False)  # Sort by amount column, descending
        self.update_summary()

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
        add_frame = ctk.CTkFrame(main_frame, height=120)
        add_frame.grid(row=4, column=0, sticky="ew", padx=30, pady=(10, 20))
        add_frame.grid_propagate(False)
        add_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Form title
        add_label = ctk.CTkLabel(
            add_frame,
            text="Add New Transaction",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        add_label.grid(row=0, column=0, columnspan=4, pady=(10, 5))
        
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
    # SEARCH FUNCTIONALITY
    # =============================================================================
    
    def search_bar_frame(self, home_frame):
        """
        Create search bar with magnifying glass icon.
        Uses StringVar with trace callback for real-time search.
        """
        # Container frame with transparent background
        search_frame = ctk.CTkFrame(home_frame, fg_color="transparent", height=60)
        search_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        search_frame.grid_propagate(False)
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Search input container with icon overlay
        search_container = ctk.CTkFrame(search_frame, height=40)
        search_container.grid(row=0, column=0, sticky="ew", pady=10)
        search_container.grid_propagate(False)
        search_container.grid_columnconfigure(0, weight=1)
        
        # Search entry with real-time callback
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.on_search)
        
        self.search_entry = ctk.CTkEntry(
            search_container,
            textvariable=self.search_var,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(5, 35))
        
        # Search icon overlay
        self._add_search_icon(search_container)

    def _add_search_icon(self, parent):
        """Add magnifying glass icon to search bar."""
        self.lens_image = ctk.CTkImage(
            Image.open(os.path.join(ICONS_PATH, "search.png")),
            size=(24, 24)
        )
        lens_icon = ctk.CTkLabel(
            parent,
            text="",
            image=self.lens_image,
            width=20,
            height=20
        )
        lens_icon.grid(row=0, column=0, sticky="e", padx=(0, 10))

    def on_search(self, var_name, index, operation):
        """
        Handle real-time search input changes.
        Updates filter state and refreshes display immediately.
        """
        self.current_search = self.search_var.get()
        self.apply_filters()

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
        
        # Create sortable column headers
        self._create_column_headers(header_frame)
        
        # Add date filter buttons
        self._create_date_filter_buttons(header_frame)

    def _create_column_headers(self, parent):
        """Create sortable column headers with appropriate weights."""
        headers = ["Date", "Amount", "Tag", "Description", ""]
        column_weights = [2, 2, 2, 4, 1]

        for i, (header, weight) in enumerate(zip(headers, column_weights)):
            parent.grid_columnconfigure(i, weight=weight)
            
            # Sortable columns get buttons
            if header in ["Date", "Amount", "Tag"]:
                self._create_sort_button(parent, header, i)
            else:
                # Non-sortable columns get labels
                label = ctk.CTkLabel(
                    parent,
                    text=header,
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                label.grid(row=0, column=i, sticky="ew", padx=10, pady=8)

    def _create_sort_button(self, parent, header, column_index):
        """Create individual sort button for a column."""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=0, column=column_index, sticky="ew", padx=5, pady=8)
        btn_frame.grid_columnconfigure(0, weight=1)
        
        sort_btn = ctk.CTkButton(
            btn_frame,
            text=f"{header} ↕",
            command=lambda col=column_index+1: self.sort_table(col),
            width=24,
            height=32,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        sort_btn.grid(row=0, column=0, sticky="ew")

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

    def sort_table(self, column_index, boolean=None):
        """
        Delegate sorting to virtual table component.
        Maintains separation of concerns between view and table logic.
        """
        self.virtual_table.sort_data(column_index, boolean)