from config.settings import (KEY_CURRENCY_SIGN, TAGS_DICTIONARY,
                            COLOR_CANCEL_BTN_HOVER, COLOR_CANCEL_BTN, COLOR_DATE_FIELD, COLOR_TAG_FIELD, COLOR_DESC_FIELD,
                            COLOR_DELETE_BTN, COLOR_DELETE_BTN_HOVER, COLOR_EXPENSE, COLOR_INCOME,
                            KEY_SUM_TRANSACTIONS, KEY_SUM_INCOME, KEY_SUM_EXPENSES, KEY_SUM_BALANCE)
from src.views.base_view import BaseView
import customtkinter as ctk

# A virtual scrollable table made out of widget created from the database local raw data
class VirtualTable(BaseView):
    def __init__(self, parent, controller, data, user):
        super().__init__(parent)
        self.controller = controller
        self.data = data
        self.currency_sign = user.read_json_value(KEY_CURRENCY_SIGN)
        
        # Callback used for updating summary
        self.summary_callback = None

        # Used to store the rows widgets, every row is a frame saved here, can be hided, deleted and showed, when needed, this is done to not recreate every widget everytime
        self.widgets_list = []
        
        # Configure main container to expand properly
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
        # Initialize UI and start rendering
        self.setup_ui()

    # =============================================================================
    # UI SETUP AND INITIALIZATION
    # =============================================================================
    
    def setup_ui(self):
        # Create main container
        self.table_container = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.table_container.grid(row=0, column=0, sticky="nsew", padx=30, pady=5)
        self.table_container.grid_columnconfigure(0, weight=1)
        self.table_container.grid_rowconfigure(0, weight=1)

        # The scrollable frame is inside the frame main container
        self.scroll_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.scroll_frame.grid(row=0, column=0, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Bind mouse wheel scrolling (to scroll the frame with the mouse wheel)
        self.scroll_frame.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows / macOS
        self.scroll_frame.bind_all("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.scroll_frame.bind_all("<Button-5>", self._on_mousewheel)    # Linux scroll down

        # Creation of all row widget, we do it for every data_row in self.data, self.data is a list of list, every list have all the info to transform in widget
        for i, data_row in enumerate(self.data):
            self._create_row(data_row, i)

    # When scrolling with the mouse the yview scroll down or up
    def _on_mousewheel(self, event):
        # Windows and macOS
        if event.num == 4 or event.delta > 0:
            self.scroll_frame._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.scroll_frame._parent_canvas.yview_scroll(1, "units")

    def _create_row(self, data_row, data_index):
        # Because the data is formatted in [database_index, date, amount, tag, desc] data_row[2] is the amount positioned in the list
        if data_row[2] >= 0:
            color = COLOR_INCOME      # The amount is positive, is green
        else:
            color = COLOR_EXPENSE        # The amount is negative, is red

        #Tags dictionary have key : color , every key is a tag
        if data_row[3] in TAGS_DICTIONARY.keys():
            tag_color = TAGS_DICTIONARY[data_row[3]]
            is_bold = ctk.CTkFont(size=14, weight="bold")
        else:
            tag_color = "#FFFFFF"
            is_bold = ctk.CTkFont(size=12)

        # The widget row, a frame with inside all the labels and button to be considered as a transaction row
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        
        # Configure columns with proportional weights for responsive design
        row_frame.grid_columnconfigure(0, weight=15, uniform="col")   # date - 15% of width
        row_frame.grid_columnconfigure(1, weight=15, uniform="col")   # amount - 15% of width  
        row_frame.grid_columnconfigure(2, weight=20, uniform="col")   # tag - 15% of width
        row_frame.grid_columnconfigure(3, weight=40, uniform="col")   # desc - 45% of width (flexible)
        row_frame.grid_columnconfigure(4, weight=10, uniform="col")   # delete - 10% of width

        # Format the amount with proper spacing
        amount_text = f"{data_row[2]}{self.currency_sign}"
        
        # A dictionary of object and information - NO fixed widths
        new_row = {
            'date': ctk.CTkLabel(row_frame, text=data_row[1], height=28, anchor="w", 
                                font=ctk.CTkFont(size=12)),
            'amount': ctk.CTkLabel(row_frame, text=amount_text, 
                                text_color=color, font=ctk.CTkFont(size=14, weight="bold"), 
                                height=28, anchor="e"),  # Right align the amount
            'tag': ctk.CTkLabel(row_frame, text=data_row[3], anchor="w", height=28,
                            font=is_bold, text_color=tag_color),
            'desc': ctk.CTkLabel(row_frame, text=data_row[4], anchor="w", height=28,
                                font=ctk.CTkFont(size=12)),
            'delete': ctk.CTkButton(
                row_frame,
                text="Delete",
                width=60,
                height=28,
                fg_color=COLOR_DELETE_BTN,
                hover_color=COLOR_DELETE_BTN_HOVER,
                font=ctk.CTkFont(size=12),
                command=lambda: self.__delete_button_event(self.widgets_list.index(row_frame))
            ),
            'visible': False,
            'data_row': data_index,
            'database_real_index': data_row[0]
        }

        # Place all widgets with consistent spacing and proper sticky values
        new_row['date'].grid(row=0, column=0, padx=(15, 5), pady=2, sticky="ew")
        new_row['amount'].grid(row=0, column=1, padx=(15, 15), pady=2, sticky="ew")  # Extra space after amount
        new_row['tag'].grid(row=0, column=2, padx=(30, 5), pady=2, sticky="ew")
        new_row['desc'].grid(row=0, column=3, padx=(40, 5), pady=2, sticky="ew")
        new_row['delete'].grid(row=0, column=4, padx=(5, 15), pady=2, sticky="e")
        
        # Lastly we add the reference of the frame widget to the widgets_list
        self.widgets_list.append(row_frame)

    # =============================================================================
    # Event to filter the widgets list
    # =============================================================================

    # Show all the widges in self.widgets_list
    def show_all(self):
        # After looping for all the widgets in the list, we position it in the grid with the index used as position, using a list ensure to not have empty position
        # The widgets frame is child of the scroll frame, so when we call grid we are placing it inside the scroll frame
        for index, widget in enumerate(self.widgets_list):
            widget.grid(row = index, column = 0, padx = 32, pady = 4, sticky = "ew")
            widget.grid()  # ensures the widget is visible if it was hidden before

        # Position the scroll bar to the start of the frame on the top (this is usefull when we call show all from the button all)
        self.scroll_frame._parent_canvas.yview_moveto(0)
        self._notify_summary_changed()                        # Notify to change the summary values using the callback funnction and implementation

    def hide_all(self):
        # After looping for all the widgets in the list, we position it in the grid with the index used as position, using a list ensure to not have empty position
        # The widgets frame is child of the scroll frame, so when we call grid we are placing it inside the scroll frame
        for widget in self.widgets_list:
            widget.grid_remove()  # ensures the widget is visible if it was hidden before

        # Position the scroll bar to the start of the frame on the top (this is usefull when we call show all from the button all)
        self.scroll_frame._parent_canvas.yview_moveto(0)
        self._notify_summary_changed()                        # Notify to change the summary values using the callback funnction and implementation

            
    # Unplace from the grid all the widget that are not income
    def show_income(self):
        # frame.winfo_children()[1].cget("text") === widget frame >> [ctklabel = date, ctklabel =amount ,ctklabel = tag, ctklabel = desc] >> [1]
        # position equal the amount >>cget("text") from the label, the text have the amount
        for frame in self.widgets_list:
            label_ref = frame.winfo_children()[1].cget("text")
            if float(label_ref.strip(self.currency_sign)) < 0:                     # We remove the currency sign and transform it into a float
                frame.grid_remove()                                                # We remove it from the grid, but do not forget it, because we do not delete it from the list of widgets
            else: 
                frame.grid()                                                       # If the button is called after another button, some widgets that are income could be hided, this will show it
        
        # The scroll frame hight differ from income, expenses and all, so this solve the problem positioning on the top 
        self.scroll_frame._parent_canvas.yview_moveto(0)
        self._notify_summary_changed()                       # Notify to change the summary values using the callback funnction and implementation

    # Same as show_income, unplace the grid all the widget that are not expenses
    def show_expenses(self):
        for frame in self.widgets_list:
            label_ref = frame.winfo_children()[1].cget("text")
            if float(label_ref.removesuffix(self.currency_sign)) > 0:
                frame.grid_remove()
            else: 
                frame.grid()

        self.scroll_frame._parent_canvas.yview_moveto(0)
        self._notify_summary_changed()                       # Notify to change the summary values using the callback funnction and implementation

    # Show only the row witch contain the searched text used in the search bar
    def show_searched(self, text):
        # Show expenses when typing -
        if text == "-":
            self.show_expenses()
            return
        
        # Show income when typing +
        if text == "+":
            self.show_income()
            return

        # Loop trough all frames in the widgets, and retrieve the texts of the labels, than search the text quary if is present in the labels, simple search
        for frame in self.widgets_list:
            search_text = text.lower()
            date = frame.winfo_children()[0].cget("text").lower()
            amount = frame.winfo_children()[1].cget("text").lower()
            tag =  frame.winfo_children()[2].cget("text").lower()
            desc = frame.winfo_children()[3].cget("text").lower()

            # Search all
            if search_text in f"{date} {amount} {tag} {desc}":
                frame.grid()
            else: 
                frame.grid_remove()

        self.scroll_frame._parent_canvas.yview_moveto(0)
        self._notify_summary_changed()                        # Notify to change the summary values using the callback funnction and implementation

    # =============================================================================
    # Delete button event confirmation
    # =============================================================================

    # Delete button event to  open a confirmation button, a top level frame that let the user confirm of deny the deletion
    def __delete_button_event(self, idx):
        # Checks if other delete button dialoge box exists, if they exist, they are destroyed
        for widget in self.controller.winfo_children():
            if isinstance(widget, ctk.CTkToplevel):
                widget.destroy()

        # Retrieve all the text from the widget to show the user what is deleting it
        date = self.widgets_list[idx].winfo_children()[0].cget("text")
        amount = self.widgets_list[idx].winfo_children()[1].cget("text")
        tag = self.widgets_list[idx].winfo_children()[2].cget("text")
        desc = self.widgets_list[idx].winfo_children()[3].cget("text")

        # Create a top level dialog box
        top_level_dialog = ctk.CTkToplevel(self.controller)
        top_level_dialog.title("Confirmation")
        top_level_dialog.resizable(False, False)
        top_level_dialog.grid_columnconfigure((0, 1), weight=1)
        top_level_dialog.rowconfigure((0, 1, 2, 3, 4), weight=1)
        top_level_dialog.attributes("-topmost", True)
        top_level_dialog.transient(self.controller)
        top_level_dialog.geometry("350x280")

        # Main warning message
        self.warning_label = ctk.CTkLabel(master=top_level_dialog,
                                        width=330,
                                        text="Are you sure you want to delete:",
                                        font=ctk.CTkFont(size=16, weight="bold"),
                                        text_color=COLOR_DELETE_BTN,
                                        fg_color="transparent")
        self.warning_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="ew")
        
        # Date field
        self.date_label = ctk.CTkLabel(master=top_level_dialog,
                                    width=330,
                                    text=f"Date: {date}",
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    text_color=COLOR_DATE_FIELD,
                                    fg_color="transparent")
        self.date_label.grid(row=1, column=0, columnspan=2, padx=20, pady=2, sticky="w")
        
        # Amount field
        self.amount_label = ctk.CTkLabel(master=top_level_dialog,
                                        width=330,
                                        text=f"Amount: {amount}",
                                        font=ctk.CTkFont(size=12, weight="bold"),
                                        text_color=COLOR_INCOME,
                                        fg_color="transparent")
        self.amount_label.grid(row=2, column=0, columnspan=2, padx=20, pady=2, sticky="w")
        
        # Tag field
        self.tag_label = ctk.CTkLabel(master=top_level_dialog,
                                    width=330,
                                    text=f"Tag: {tag}",
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    text_color=COLOR_TAG_FIELD,
                                    fg_color="transparent")
        self.tag_label.grid(row=3, column=0, columnspan=2, padx=20, pady=2, sticky="w")
        
        # Description field
        self.desc_label = ctk.CTkLabel(master=top_level_dialog,
                                    width=330,
                                    wraplength=310,
                                    text=f"Description: {desc}",
                                    font=ctk.CTkFont(size=12),
                                    text_color=COLOR_DESC_FIELD,
                                    fg_color="transparent")
        self.desc_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(2, 15), sticky="ew")
        
        # Buttons
        self.ok_button = ctk.CTkButton(master=top_level_dialog,
                                    width=120,
                                    height=35,
                                    border_width=0,
                                    text='Delete',
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    fg_color=COLOR_DELETE_BTN,
                                    hover_color=COLOR_DELETE_BTN_HOVER,
                                    command=lambda: self._ok_event(top_level_dialog, idx))
        self.ok_button.grid(row=5, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky="ew")
        
        self.cancel_button = ctk.CTkButton(master=top_level_dialog,
                                        width=120,
                                        height=35,
                                        border_width=0,
                                        text='Cancel',
                                        font=ctk.CTkFont(size=14),
                                        fg_color=COLOR_CANCEL_BTN,
                                        hover_color=COLOR_CANCEL_BTN_HOVER,
                                        command=lambda: self._cancel_event(top_level_dialog))
        self.cancel_button.grid(row=5, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew")

    # Event the the user press the delete button inside the dialog box
    def _ok_event(self, frame, idx):
        self.__remove_row(idx)
        frame.destroy()
        self._notify_summary_changed()                  # Notify to change the summary values using the callback funnction and implementation

    # Event when the user presse the cancel button or the close windows button, destroy the window
    def _cancel_event(self, frame):
        frame.destroy()

    # Remove the row from the widget list and from the screen
    def __remove_row(self, idx):
        self.widgets_list[idx].destroy()               # Remove it from the screen
        self.widgets_list.pop(idx)
        # Add code to delete it from the database local 

    # =============================================================================
    # Update summary
    # =============================================================================
    
    # One time use to register the callback function that use the labels
    def register_summary_callback(self, callback_function):
        self.summary_callback = callback_function

    # If something in the table is changed is notified, we calculate the new summary and we pass the dictionary with the values to be used in the callback function in the home_view
    def _notify_summary_changed(self):
        summary_data = self._calculate_summary()
        self.summary_callback(summary_data)

    # Calculte the summary values
    def _calculate_summary(self):
        income = 0
        expenses = 0
        transactions = 0

        # If the widget in list is visible we take the amount and use for the income expenses and transactions, based if > or < 0
        for widget in self.widgets_list:
            if widget.winfo_manager():
                amount = float(widget.winfo_children()[1].cget("text").removesuffix(self.currency_sign))
                
                if amount >= 0:
                    income += amount
                else:
                    expenses += amount
               
                transactions += 1

        # We return a dictionary of values used in the homeview to change the summary panel
        return {
            KEY_SUM_TRANSACTIONS: transactions,
            KEY_SUM_INCOME: income,
            KEY_SUM_EXPENSES: expenses,
            KEY_SUM_BALANCE: (income + expenses)
        }
    
    # =============================================================================
    # Date Ordering
    # =============================================================================
    
    # Function called when the button date is pressed, order the transactions by date
    def order_by_date(self, state=[False]):

        # Even if a bad practice this is a reference to the previous arguments everythime is called, is a way to change the ordering, ascending and descending based on the click by user
        state[0] = not state[0] 

        # This method use the built-in sorting (that use the Timsort) the best way to order an array of date, the problem was to get this array of dates.
        # Firstly we have an empty list and a list of pair
        new_widget_list = []
        date_index_pair = []


        # We append to the list of pair a pair conteining the index and date
        for i, widget in enumerate(self.widgets_list):
            date = widget.winfo_children()[0].cget("text")

            date_index_pair.append((date, i))

        # Thanks to sorted built in  function we order by date first element of the pairs, the index is ignored
        sorted_pairs = sorted(date_index_pair, reverse=state[0])
        # sorted_pairs = sorted(date_widget_pairs, reverse=True)  # Descending

        # Hide_all is responsable to hiding the current transactions
        self.hide_all()

        # We append to the new_widgets list, the widgets in order, using the index inside the sorted pair to retrieve the widget from the original list
        for pair in sorted_pairs:
            widget = self.widgets_list[pair[1]]
            new_widget_list.append(widget)
        
        # We overwrite the widgets list with the new widgets list and than show them all
        self.widgets_list = new_widget_list

        self.show_all()

    
    def order_by_amount(self):
        pass