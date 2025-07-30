from src.views.base_view import BaseView
import customtkinter as ctk
from PIL import Image
import os
from config.settings import ICONS_PATH
from src.views.table_view import Table


class HomeView(BaseView):
    def __init__(self, parent, controller=None, user=None, database = None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.db = database
        self.data = self.db.local_db
        self.db_transactions = []

        self.current_page = 0
        self.pages = 1
        self.start_index = 0
        self.end_index = 50
        self.max_len = len(self.data)
        self.rows_for_pages = 50

        self.new_table = []
        
        self.page_label_var = ctk.StringVar()
        self.page_label_var.set(str(self.current_page + 1))

        # Define colors
        self.DISABLED_COLOR = "#566BC9"   # Gray for disabled
        self.DEFAULT_COLOR = ctk.ThemeManager.theme["CTkButton"]["fg_color"]   # Default button color

        # First table
        first_table = Table(self, self, self.data, self.start_index, self.end_index)
        first_table.grid(row=2, column=0, sticky="nsew")
        first_table.lower()
        self.new_table.append(first_table)

        if not (self.pages * self.rows_for_pages) > (self.max_len - (self.rows_for_pages -10 )):
            self.start_index = self.end_index + 1
            self.end_index = ((self.pages + 1) * self.rows_for_pages)

            second_table = Table(self, self, self.data, self.start_index, self.end_index)
            second_table.grid(row=2, column=0, sticky="nsew")
            second_table.lower()
            self.new_table.append(second_table)
            self.pages +=1

        # Show the first page
        self.new_table[0].lift()

        # Configure HomeView grid to expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Make table frame stretch vertically
    
        self.setup_ui()


    def event_next_page(self):
        if self.current_page + 1 == self.pages:
            return

        # Create a page when we are on the last one, this is done to prevent to load
        if self.current_page == self.pages -2 and  (self.end_index <= len(self.data)) :
            self.start_index = self.end_index + 1
            self.end_index = ((self.pages + 1) * self.rows_for_pages)

            other_table = Table(self, self, self.data, self.start_index, self.end_index)
            other_table.grid(row=2, column=0, sticky="nsew")
            other_table.lower()
            self.new_table.append(other_table)
            self.pages +=1
        
        self.new_table[self.current_page].lower()  # Hide current
        self.current_page += 1
        self.new_table[self.current_page].lift()   # Show next
        
        self.page_label_var.set(str(self.current_page + 1))
        self.update_button_states()


    def event_prev_page(self):
        if self.current_page == 0:
            return

        self.new_table[self.current_page].lower()
        self.current_page -= 1
        self.new_table[self.current_page].lift()

        self.page_label_var.set(str(self.current_page + 1))
        self.update_button_states()

    def update_button_states(self):
        if not (self.prev_btn and self.next_btn):
            return
            
        # Update previous button
        if self.current_page == 0:
            # On first page - disable/gray out previous button
            self.prev_btn.configure(fg_color=self.DISABLED_COLOR, hover = False)
        else:
            # Not on first page - enable previous button
            self.prev_btn.configure(fg_color=self.DEFAULT_COLOR, hover = True)
        
        # Update next button
        max_page = self.pages - 1
        if self.current_page >= max_page:
            # On last page - disable/gray out next button
            self.next_btn.configure(fg_color=self.DISABLED_COLOR, hover = False)
        else:
            # Not on last page - enable next button
            self.next_btn.configure(fg_color=self.DEFAULT_COLOR, hover = True)


    def save_db_modification(self, action, row_id, date = None, amount = None, tag = None, desc = None):
        if action == "delete":
            self.db_transactions.append({
                "action" : action,
                "params" : row_id
            })
        else:
            self.db_transactions.append({
                "action" : action,
                "params" : [date, amount, tag, desc]
            })

    def update_db(self):
        # Tempo update db testing
        for txn in self.db_transactions:
            self.db.remove_transaction(txn["params"] + 1)

    def setup_ui(self):

        self.search_bar_frame(self)                                         # Add a search bar in the top of the frame
        self.ordering_frame(self)                                           # Add buttons to order the list for every category
        #self.table_frame(self)     
        self.new_table[0].grid(row=2, column=0, sticky="nsew")     
        self.add_transaction_frame(self)                                    # Add at the bottom of the frame a transaction frame to add



    
    # Function to scroll the table
    def _on_mousewheel(self, event):
        if event.num == 4:  # Linux scroll up
            self.table_scroll._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.table_scroll._parent_canvas.yview_scroll(1, "units")
        else:  # Windows/macOS
            direction = -1 if event.delta > 0 else 1
            self.table_scroll._parent_canvas.yview_scroll(direction, "units")
            


        
  
    # The table frame
    def table_frame(self, main_frame):
        # Table container - this is the main expandable section
        table_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        table_container.grid(row=2, column=0, sticky="nsew", padx=30, pady=5)
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

        # Create scrollable frame for table
        self.table_scroll = ctk.CTkScrollableFrame(table_container, fg_color="#1a1a1a")
        self.table_scroll.grid(row=0, column=0, sticky="nsew")
        self.table_scroll.grid_columnconfigure(0, weight=1)

        # Enable mouse scroll on the table scrollable frame
        self.table_scroll.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows/macOS
        self.table_scroll.bind_all("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.table_scroll.bind_all("<Button-5>", self._on_mousewheel)    # Linux scroll down

        for widget in self.table_scroll.winfo_children():
            widget.destroy()

        for i in range(5):
            self.table_scroll.grid_columnconfigure(i, weight=1)

        for idx, row in enumerate(self.data):
            if idx >= 50:
                break
            self.create_table_row(idx, row)


    def create_table_row(self, row_idx, row_data):
        date = row_data[1]
        amount = float(row_data[2])
        tag = row_data[3]
        desc = row_data[4]

        amount_color = "#ff6b6b" if amount < 0 else "#51cf66"
        amount_text = f"${abs(amount):.2f}" if amount >= 0 else f"-${abs(amount):.2f}"
        
        date_lab = ctk.CTkLabel(self.table_scroll, text=date)
        date_lab.grid(row=row_idx, column=0, sticky="w", padx=10, pady=6)

        amount_lab = ctk.CTkLabel(self.table_scroll, text=amount_text, text_color=amount_color)
        amount_lab.grid(row=row_idx, column=1, sticky="w", padx=10)

        tag_lab = ctk.CTkLabel(self.table_scroll, text=tag)
        tag_lab.grid(row=row_idx, column=2, sticky="w", padx=10)

        desc_lab = ctk.CTkLabel(self.table_scroll, text=desc)
        desc_lab.grid(row=row_idx, column=3, sticky="w", padx=10)

        del_btn = ctk.CTkButton(
            self.table_scroll,
            text="Delete",
            width=60,
            height=28,
            fg_color="#ff6b6b",
            hover_color="#ff5252",
            font=ctk.CTkFont(size=12),
            command=lambda idx=row_data[0]: self.__destroy_table_row(idx, date_lab, amount_lab, tag_lab, desc_lab, del_btn)
        )
        del_btn.grid(row=row_idx, column=4, padx=10, pady=6)


        
     
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
        # Placeholder function for adding transaction
        print("Add transaction clicked")
        print(f"Date: {self.date_entry.get()}")
        print(f"Amount: {self.amount_entry.get()}")
        print(f"Category: {self.category_entry.get()}")
        print(f"Description: {self.description_entry.get()}")


            




    # Create a search bar in a frame
    def search_bar_frame(self, home_frame):
        # Create the frame of the search  on the top of the home frame
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
        
        self.lens_image = ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "search.png")), size=(24, 24))             # Icon for search bar
        # Lens icon positioned at the end (inside the search bar area)
        lens_icon = ctk.CTkLabel(
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
         # Table header with sort buttons
        header_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", height=50)
        header_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))
        header_frame.grid_propagate(False)
        
        headers = ["Date", "Amount", "Tag", "Description", ""]
            
        column_weights = [2, 2, 2, 4, 1]

        
        # Add button
        self.prev_btn = ctk.CTkButton(
            header_frame, 
            text="<", 
            height=32,
            width= 32,
            command=self.event_prev_page,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color= self.DISABLED_COLOR,
            hover = False
        )
        self.prev_btn.grid(row=0, column=5, padx=5, pady=8)


        self.page_btn = ctk.CTkButton(
            header_frame, 
            textvariable=self.page_label_var, 
            height=32,
            width= 32,
            command=self.add_transaction,
            font=ctk.CTkFont(size=14, weight="bold"),
            hover = False
        )
        self.page_btn.grid(row=0, column=6, padx=5, pady=8)

        self.next_btn = ctk.CTkButton(
            header_frame, 
            text=">", 
            height=32,
            width= 32,
            command=self.event_next_page,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.next_btn.grid(row=0, column=7, padx=5, pady=8)


        
        for i, (header, weight) in enumerate(zip(headers, column_weights)):
            header_frame.grid_columnconfigure(i, weight=weight)
            
            if header in ["Date", "Amount", "Tag"]:
                btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
                btn_frame.grid(row=0, column=i, sticky="ew", padx=5, pady=8)
                btn_frame.grid_columnconfigure(0, weight=1)
                
                sort_btn = ctk.CTkButton(
                    btn_frame,
                    text=f"{header} ↕",
                    command=lambda col=i: self.sort_table(col),
                    width= 24,
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


    # Placeholder ordering functions (no functionality yet)
    def order_by_date(self):
        print("Order by date clicked")

    def order_by_amount(self):
        print("Order by amount clicked")

    def order_by_category(self):
        print("Order by category clicked")
    
    def order_by_description(self):
        print("Order by description clicked")

    
