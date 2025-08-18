from config.settings import (COLOR_EDIT_BTN, COLOR_EDIT_BTN_HOVER, DB_ACTION_ADD, DB_ACTION_DELETE, DB_ACTION_EDIT, DELETE_ICON_FILE_NAME, EDIT_ICON_FILE_NAME, ICONS_PATH, INCORRECT_DATE, INCORRECT_YEAR, KEY_CURRENCY_SIGN, TAGS_DICTIONARY,
                            COLOR_CANCEL_BTN_HOVER, COLOR_CANCEL_BTN, COLOR_DATE_FIELD, COLOR_TAG_FIELD, COLOR_DESC_FIELD,
                            COLOR_DELETE_BTN, COLOR_DELETE_BTN_HOVER, COLOR_EXPENSE, COLOR_INCOME,
                            KEY_SUM_TRANSACTIONS, KEY_SUM_INCOME, KEY_SUM_EXPENSES, KEY_SUM_BALANCE)
from src.views.base_view import BaseView
from src.utils import helpers
import customtkinter as ctk
from PIL import Image
import os


# A virtual scrollable table made out of widget created from the database local raw data
class VirtualTable(BaseView):
    def __init__(self, parent, controller, database, user):
        super().__init__(parent)
        self.controller = controller
        self.database = database
        self.data = database.local_db
        self.currency_sign = user.read_json_value(KEY_CURRENCY_SIGN)

        self.db_transactions = []

        self.edit_image = ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, EDIT_ICON_FILE_NAME)))
        
        self.delete_image = ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, DELETE_ICON_FILE_NAME)))

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
            self.create_row(data_row)

    # When scrolling with the mouse the yview scroll down or up
    def _on_mousewheel(self, event):
        # Windows and macOS
        if event.num == 4 or event.delta > 0:
            self.scroll_frame._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.scroll_frame._parent_canvas.yview_scroll(1, "units")

    def create_row(self, data_row):
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
        row_frame.grid_columnconfigure(2, weight=15, uniform="col")   # tag - 15% of width
        row_frame.grid_columnconfigure(3, weight=30, uniform="col")   # desc - 40% of width (flexible)
        row_frame.grid_columnconfigure(4, weight=5, uniform="col")   # modify - 10% of width
        row_frame.grid_columnconfigure(5, weight=5, uniform="col")   # delete - 10% of width

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
            'modify': ctk.CTkButton(
                row_frame,
                text= "",
                image= self.edit_image,
                width=32,
                height=32,
                fg_color=COLOR_EDIT_BTN,
                hover_color=COLOR_EDIT_BTN_HOVER,
                font=ctk.CTkFont(size=12),
                command=lambda: self.__edit_button_event(self.widgets_list.index(row_frame))
            ),
            'delete': ctk.CTkButton(
                row_frame,
                text= "",
                image= self.delete_image,
                width=32,
                height=32,
                fg_color=COLOR_DELETE_BTN,
                hover_color=COLOR_DELETE_BTN_HOVER,
                font=ctk.CTkFont(size=12),
                command=lambda: self.__delete_button_event(self.widgets_list.index(row_frame))
            ),
        }

        # Place all widgets with consistent spacing and proper sticky values
        new_row['date'].grid(row=0, column=0, pady=2, sticky="ew")
        new_row['amount'].grid(row=0, column=1, padx =(0, 16), pady=2, sticky="ew")  # Extra space after amount
        new_row['tag'].grid(row=0, column=2, pady=2, sticky="ew")
        new_row['desc'].grid(row=0, column=3, pady=2, sticky="ew")
        new_row['modify'].grid(row=0, column=4,pady=2, sticky="e")
        new_row['delete'].grid(row=0, column=5, padx= (8,0), pady=2, sticky="w")
        
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
    def show_income(self, date, month):

        self.filter_dates(date, month)
        # frame.winfo_children()[1].cget("text") === widget frame >> [ctklabel = date, ctklabel =amount ,ctklabel = tag, ctklabel = desc] >> [1]
        # position equal the amount >>cget("text") from the label, the text have the amount
        for frame in self.widgets_list:
            if frame.winfo_ismapped():
                label_ref = frame.winfo_children()[1].cget("text")
                if float(label_ref.strip(self.currency_sign)) < 0:                     # We remove the currency sign and transform it into a float
                    frame.grid_remove()                                                # We remove it from the grid, but do not forget it, because we do not delete it from the list of widgets
                else: 
                    frame.grid()                                                       # If the button is called after another button, some widgets that are income could be hided, this will show it
            
        # The scroll frame hight differ from income, expenses and all, so this solve the problem positioning on the top 
        self.scroll_frame._parent_canvas.yview_moveto(0)
        self._notify_summary_changed()                       # Notify to change the summary values using the callback funnction and implementation

    # Same as show_income, unplace the grid all the widget that are not expenses
    def show_expenses(self, date, month):
        self.filter_dates(date, month)

        for frame in self.widgets_list:
            if frame.winfo_ismapped():
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
        self.save_db_modification(DB_ACTION_DELETE, self.data[idx][0])

    # Event when the user presse the cancel button or the close windows button, destroy the window
    def _cancel_event(self, frame):
        frame.destroy()

    # Remove the row from the widget list and from the screen
    def __remove_row(self, idx):
        self.widgets_list[idx].destroy()               # Remove it from the screen
        self.widgets_list.pop(idx)
        # Add code to delete it from the database local 


    # =============================================================================
    # Edit button event confirmation 
    # =============================================================================

    # Edit button event to  open a confirmation button, a top level frame that let the user confirm of deny the deletion
    def __edit_button_event(self, idx):
        # Checks if other edit button dialoge box exists, if they exist, they are destroyed
        for widget in self.controller.winfo_children():
            if isinstance(widget, ctk.CTkToplevel):
                widget.destroy()

        # Retrieve all the text from the widget to show the user what is deleting it
        self.current_date = self.widgets_list[idx].winfo_children()[0].cget("text")
        self.current_amount = self.widgets_list[idx].winfo_children()[1].cget("text")
        self.current_tag = self.widgets_list[idx].winfo_children()[2].cget("text")
        self.current_desc = self.widgets_list[idx].winfo_children()[3].cget("text")

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
                                        text="What do you want to Edit?:",
                                        font=ctk.CTkFont(size=16, weight="bold"),
                                        text_color=COLOR_DELETE_BTN,
                                        fg_color="transparent")
        self.warning_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="ew")
        
        # Date field
        self.date_label = ctk.CTkEntry(master=top_level_dialog,
                                    width=330,
                                    placeholder_text=self.current_date,
                                    font=ctk.CTkFont(size=12, weight="bold"))
        self.date_label.grid(row=1, column=0, columnspan=2, padx=20, pady=2, sticky="w")
        
        # Amount field
        self.amount_label = ctk.CTkEntry(master=top_level_dialog,
                                        width=330,
                                        placeholder_text=self.current_amount,
                                        font=ctk.CTkFont(size=12, weight="bold"))
        self.amount_label.grid(row=2, column=0, columnspan=2, padx=20, pady=2, sticky="w")
        
        # Tag field
        self.tag_label = ctk.CTkEntry(master=top_level_dialog,
                                    width=330,
                                    placeholder_text=self.current_tag,
                                    font=ctk.CTkFont(size=12, weight="bold"))
        self.tag_label.grid(row=3, column=0, columnspan=2, padx=20, pady=2, sticky="w")
        
        # Description field
        self.desc_label = ctk.CTkEntry(master=top_level_dialog,
                                    width=330,
                                    placeholder_text=self.current_desc,
                                    font=ctk.CTkFont(size=12))
        self.desc_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(2, 15), sticky="ew")
        
        # Buttons
        self.ok_button = ctk.CTkButton(master=top_level_dialog,
                                    width=120,
                                    height=35,
                                    border_width=0,
                                    text='Edit',
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    fg_color=COLOR_DELETE_BTN,
                                    hover_color=COLOR_DELETE_BTN_HOVER,
                                    command=lambda: self._confirm_edit(top_level_dialog, idx))
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
    def _confirm_edit(self, frame, idx):
        user_date = self.date_label.get()
        user_amount = self.amount_label.get()
        user_tag = self.tag_label.get() 
        user_desc = self.desc_label.get()

        user_date_error = helpers.is_valid_date(user_date)
        
        if user_date == "" and  user_amount == "" and user_tag == "" and  user_desc == "":
            self.warning_label.configure(text="Click cancel to exit edit mode")
            return

        if user_date != "" and user_date_error != True:
            if user_date_error == INCORRECT_DATE:
                self.warning_label.configure(text="The Date have incorrect format:")
            elif user_date_error == INCORRECT_YEAR: 
                self.warning_label.configure(text="The Year is incorrect:")
            return

        if not helpers.is_valid_number(user_amount) and user_amount != "":
            self.warning_label.configure(text="Incorrect Amount, use . for decimal")
            return
            
        if user_tag == "":
            user_tag = self.current_tag

        if user_desc == "":
            user_desc = self.current_desc

        if user_date == "":
            user_date = self.current_date

        if user_amount == "":
            user_amount = self.current_amount.removesuffix(self.currency_sign)
        
        user_amount = str(round(float(user_amount),2))


        self.widgets_list[idx].winfo_children()[0].configure(text = user_date)
        self.widgets_list[idx].winfo_children()[1].configure(text = (f"{user_amount}{self.currency_sign}"))
        self.widgets_list[idx].winfo_children()[2].configure(text = user_tag)
        self.widgets_list[idx].winfo_children()[3].configure(text = user_desc)

        self.update_row_colors(user_amount, user_tag, idx)
        

        self._notify_summary_changed()                  # Notify to change the summary values using the callback funnction and implementation
        self.save_db_modification(DB_ACTION_EDIT, self.data[idx][0], user_date, user_amount, user_tag, user_desc)
        frame.destroy()

    def update_row_colors(self, amount, tag, idx):
        # Because the data is formatted in [database_index, date, amount, tag, desc] data_row[2] is the amount positioned in the list
        if float(amount.removesuffix(self.currency_sign)) >= 0:
            color = COLOR_INCOME      # The amount is positive, is green
        else:
            color = COLOR_EXPENSE        # The amount is negative, is red

        #Tags dictionary have key : color , every key is a tag
        if tag in TAGS_DICTIONARY.keys():
            tag_color = TAGS_DICTIONARY[tag]
            is_bold = ctk.CTkFont(size=14, weight="bold")
        else:
            tag_color = "#FFFFFF"
            is_bold = ctk.CTkFont(size=12)


        self.widgets_list[idx].winfo_children()[1].configure(text_color = color)
        self.widgets_list[idx].winfo_children()[2].configure(text_color= tag_color, font=is_bold,)


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
        # Toggle sorting order (ascending/descending)
        state[0] = not state[0] 

        # Create list to store only visible widgets with their amount values
        visible_widgets = []
        date_index_pair = []

        # Collect only visible (mapped) widgets
        for i, widget in enumerate(self.widgets_list):
            if widget.winfo_manager():  # Only process visible widgets
                visible_widgets.append(widget)
                # Get amount text, remove currency sign, convert to float
                date_text = widget.winfo_children()[0].cget("text")
                date_index_pair.append((date_text, len(visible_widgets) - 1))

        # Sort by amount (numeric sorting, not string sorting)
        sorted_pairs = sorted(date_index_pair, key=lambda x: x[0], reverse=state[0])

        # Hide all currently visible widgets
        for widget in visible_widgets:
            widget.grid_remove()

        # Show widgets in sorted order, maintaining current filters
        for row_position, (date_text, original_index) in enumerate(sorted_pairs):
            widget = visible_widgets[original_index]
            widget.grid(row=row_position, column=0, padx=32, pady=4, sticky="ew")

        # Reset scroll position to top
        self.scroll_frame._parent_canvas.yview_moveto(0)
        # Update summary with current visible data
        self._notify_summary_changed()

    # Function called when the button date is pressed, order the transactions by amount
    def order_by_amount(self, state=[False]):
        # Toggle sorting order (ascending/descending)
        state[0] = not state[0] 

        # Create list to store only visible widgets with their amount values
        visible_widgets = []
        amount_index_pair = []

        # Collect only visible (mapped) widgets
        for i, widget in enumerate(self.widgets_list):
            if widget.winfo_ismapped():  # Only process visible widgets
                visible_widgets.append(widget)
                # Get amount text, remove currency sign, convert to float
                amount_text = widget.winfo_children()[1].cget("text")
                amount_value = float(amount_text.removesuffix(self.currency_sign))
                amount_index_pair.append((amount_value, len(visible_widgets) - 1))

        # Sort by amount (numeric sorting, not string sorting)
        sorted_pairs = sorted(amount_index_pair, key=lambda x: x[0], reverse=state[0])

        # Hide all currently visible widgets
        for widget in visible_widgets:
            widget.grid_remove()

        # Show widgets in sorted order, maintaining current filters
        for row_position, (amount_value, original_index) in enumerate(sorted_pairs):
            widget = visible_widgets[original_index]
            widget.grid(row=row_position, column=0, padx=32, pady=4, sticky="ew")

        # Reset scroll position to top
        self.scroll_frame._parent_canvas.yview_moveto(0)
        # Update summary with current visible data
        self._notify_summary_changed()

    # =============================================================================
    # Date Filtering
    # =============================================================================
    
    # Gets the year dates from the data, this is used for the optionmenu in the summary sidebar
    def get_dates(self):
        # It create a set (so without duplicates) of the element in index 1 sliced. The element in index 1 of self.data is the date formatted in "2025-02-10", this is sliced to "2025" and than
        # added to the set, giving something like this {'2025', '2024'}
        dates ={sublist[1][0:4] for sublist in self.data}

        # The sets is than sorted and converted in a list, because optionmenu accepts only list
        sorted_dates = list(sorted(dates))

        sorted_dates.insert(0, "All")

        return sorted_dates
    
    
    def filter_dates(self, date_value, month_value):
        months = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"
        }

        if date_value == "All" and month_value ==  "All":
            self.show_all()
            self.scroll_frame._parent_canvas.yview_moveto(0)
            self._notify_summary_changed()   
            return
        
        if date_value == "All" and month_value != "All":
            for frame in self.widgets_list:
                label_ref = frame.winfo_children()[0].cget("text")[5:7]
                if label_ref == months[month_value]:
                    frame.grid()
                else: 
                    frame.grid_remove()

            self.scroll_frame._parent_canvas.yview_moveto(0)
            self._notify_summary_changed()   
            return
        
        if month_value == "All" and date_value != "All":
            for frame in self.widgets_list:
                year_label = frame.winfo_children()[0].cget("text")[0:4]
                if date_value == year_label:
                    frame.grid()
                else: 
                    frame.grid_remove()

            self.scroll_frame._parent_canvas.yview_moveto(0)
            self._notify_summary_changed()   
            return

        for frame in self.widgets_list:
            year_label = frame.winfo_children()[0].cget("text")[0:4]
            month_label = frame.winfo_children()[0].cget("text")[5:7]
            if date_value == year_label and months[month_value] == month_label:
                frame.grid()
            else: 
                frame.grid_remove()

        self.scroll_frame._parent_canvas.yview_moveto(0)
        self._notify_summary_changed()   
  
    # =============================================================================
    # DATABASE OPERATIONS
    # =============================================================================
    
    def save_db_modification(self, action, row_id = None, date=None, amount=None, tag=None, desc=None):
        """
        Queue database operations for batch processing.
        Improves performance by deferring actual database writes.
        """
        if action == DB_ACTION_DELETE:
            self.db_transactions.append({
                "action": action,
                "db_idx": row_id
            })
        elif action == DB_ACTION_EDIT:
            self.db_transactions.append({
                "action": action,
                "db_idx": row_id,
                "date": date,
                "amount" : amount,
                "tag" : tag,
                "desc" : desc,
            })
        elif action == DB_ACTION_ADD:
            self.db_transactions.append({
                "action": action,
                "date": date,
                "amount" : amount,
                "tag" : tag,
                "desc" : desc,
            })

    def update_db(self):
        """
        Process all queued database operations and clear the queue.
        Called when batch operations need to be committed.
        """
        for txn in self.db_transactions:
            if txn["action"] == DB_ACTION_DELETE:
                self.database.remove_transaction(txn["db_idx"])
            elif txn["action"] == DB_ACTION_EDIT:
                self.database.edit_transaction(txn["db_idx"], txn["date"], txn["amount"],txn["tag"],txn["desc"] )
            elif txn["action"] == DB_ACTION_ADD:
                self.database.add_transaction(txn["date"], txn["amount"],txn["tag"],txn["desc"])

        self.database.conn.commit()
        self.database.update_local()
        self.db_transactions.clear()
