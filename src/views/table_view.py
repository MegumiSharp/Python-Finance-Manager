# To better optimize the code the best abbroach is to create and save frame having a limitate number of transactions
from src.views.base_view import BaseView
import customtkinter as ctk


class Table(BaseView):
    def __init__(self, parent, controller, data, start, stop):
        super().__init__(parent)
        self.controller = controller
        self.data = data
        self.start = start
        self.stop = stop

        # Configure HomeView grid to expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Make table frame stretch vertically
    
        self.setup_ui()



    def setup_ui(self):
        # Table container - this is the main expandable section
        table_container = ctk.CTkFrame(self, fg_color="transparent")
        table_container.grid(row=2, column=0, sticky="nsew", padx=30, pady=5)
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

        # Create scrollable frame for table
        self.table_scroll = ctk.CTkScrollableFrame(table_container, fg_color="#1a1a1a")
        self.table_scroll.grid(row=0, column=0, sticky="nsew")
        self.table_scroll.grid_columnconfigure(0, weight=1)

        # Enable mouse scroll on the table scrollable frame
        self.table_scroll.bind("<MouseWheel>", self._on_mousewheel)  # Windows/macOS
        self.table_scroll.bind("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.table_scroll.bind("<Button-5>", self._on_mousewheel)    # Linux scroll down

        for widget in self.table_scroll.winfo_children():
            widget.destroy()

        for i in range(5):
            self.table_scroll.grid_columnconfigure(i, weight=1)

        # Assicurati di non superare la lunghezza dei dati
        for idx in range(self.start, min(self.stop, len(self.data))):
            self.create_table_row(idx, self.data[idx])


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

         
    # Function to scroll the table
    def _on_mousewheel(self, event):
        if event.num == 4:  # Linux scroll up
            self.table_scroll._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.table_scroll._parent_canvas.yview_scroll(1, "units")
        else:  # Windows/macOS
            direction = -1 if event.delta > 0 else 1
            self.table_scroll._parent_canvas.yview_scroll(direction, "units")
            
    # WHen the table row is created a reference to the widget label is stored,when the del button is pressed, this reference are deleted 
    def __destroy_table_row(self, row_idx, date, amount, tag, desc, delbtn):

        date.destroy()
        amount.destroy()
        tag.destroy()
        desc.destroy()
        delbtn.destroy()

        #self.db.remove_transaction(int(row_idx))
        #self.save_db_modification("delete", row_idx)

