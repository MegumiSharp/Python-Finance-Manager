# virtual_table.py - Fixed version using absolute positioning within scrollable area
from src.views.base_view import BaseView
import customtkinter as ctk


class VirtualTable(BaseView):
    def __init__(self, parent, controller, data, on_delete_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.data = data
        self.on_delete_callback = on_delete_callback
        
        # Virtual scrolling parameters
        self.row_height = 40
        self.visible_rows = 15  
        self.buffer_rows = 3
        self.total_rows = len(data)
        
        # Current view state
        self.scroll_top = 0
        self.first_visible_row = 0
        self.last_visible_row = 0
        self.last_rendered_range = (-1, -1)
        
        # Widget pools for reuse
        self.row_widgets = []
        
        # Setup UI first
        self.setup_ui()
        
        # Then refresh after a brief delay to ensure canvas is ready
        self.after(100, self.refresh_view)

    def setup_ui(self):
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create table container
        self.table_container = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.table_container.grid(row=0, column=0, sticky="nsew", padx=30, pady=5)
        self.table_container.grid_columnconfigure(0, weight=1)
        self.table_container.grid_rowconfigure(0, weight=1)
        
        # Create canvas for virtual scrolling
        self.canvas = ctk.CTkCanvas(
            self.table_container, 
            bg="#1a1a1a", 
            highlightthickness=0,
            height=600
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Create scrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self.table_container, 
            command=self.on_scrollbar_move
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create frame inside canvas for content - this will be our scrollable area
        self.content_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas_window = self.canvas.create_window(0, 0, anchor="nw", window=self.content_frame)
        
        # Bind events
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind mouse wheel to multiple widgets for better coverage
        widgets_to_bind = [self, self.canvas, self.content_frame, self.table_container]
        for widget in widgets_to_bind:
            widget.bind("<MouseWheel>", self.on_mousewheel)
            widget.bind("<Button-4>", self.on_mousewheel)
            widget.bind("<Button-5>", self.on_mousewheel)
        
        # Create widget pool
        self.create_widget_pool()

    def create_widget_pool(self):
        """Create a pool of reusable widgets using place geometry manager"""
        # Calculate pool size based on visible area + buffer
        pool_size = max(20, self.visible_rows + self.buffer_rows * 2)
        
        for i in range(pool_size):
            row_widgets = {
                'date': ctk.CTkLabel(self.content_frame, text="", anchor="w", width=150, height=28),
                'amount': ctk.CTkLabel(self.content_frame, text="", anchor="w", width=120, height=28),
                'tag': ctk.CTkLabel(self.content_frame, text="", anchor="w", width=120, height=28),
                'desc': ctk.CTkLabel(self.content_frame, text="", anchor="w", width=200, height=28),
                'delete': ctk.CTkButton(
                    self.content_frame,
                    text="Delete",
                    width=60,
                    height=28,
                    fg_color="#ff6b6b",
                    hover_color="#ff5252",
                    font=ctk.CTkFont(size=12)
                ),
                'visible': False,
                'data_row': -1
            }
            
            self.row_widgets.append(row_widgets)
            
    def hide_widget_row(self, row_widgets):
        """Hide a row of widgets efficiently"""
        if row_widgets['visible']:
            for key in ['date', 'amount', 'tag', 'desc', 'delete']:
                row_widgets[key].place_forget()
            row_widgets['visible'] = False
            row_widgets['data_row'] = -1
    
    def show_widget_row(self, row_widgets, y_position, data_row):
        """Show a row of widgets at the specified y position using place"""
        canvas_width = self.canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 800  # fallback width
        
        # Calculate column widths and positions
        col_widths = [0.2, 0.2, 0.2, 0.3, 0.1]  # Date, Amount, Tag, Desc, Delete
        
        x_positions = []
        current_x = 10  # Start padding
        for width_ratio in col_widths:
            x_positions.append(current_x)
            current_x += int((canvas_width - 40) * width_ratio)  # 40 for padding
        
        # Calculate actual widths for each column
        actual_widths = []
        for width_ratio in col_widths[:-1]:  # Exclude delete button
            actual_widths.append(int((canvas_width - 40) * width_ratio - 10))
        
        # Update widget sizes using configure
        row_widgets['date'].configure(width=actual_widths[0])
        row_widgets['amount'].configure(width=actual_widths[1])
        row_widgets['tag'].configure(width=actual_widths[2])
        row_widgets['desc'].configure(width=actual_widths[3])
        
        # Position widgets using place (without width/height parameters)
        row_widgets['date'].place(x=x_positions[0], y=y_position)
        row_widgets['amount'].place(x=x_positions[1], y=y_position)
        row_widgets['tag'].place(x=x_positions[2], y=y_position)
        row_widgets['desc'].place(x=x_positions[3], y=y_position)
        row_widgets['delete'].place(x=x_positions[4], y=y_position + 6)  # Center vertically
        
        row_widgets['visible'] = True
        row_widgets['data_row'] = data_row
            
    def refresh_view(self):
        """Refresh the virtual view"""
        self.total_rows = len(self.data)
        
        if self.total_rows == 0:
            self.hide_all_widgets()
            # Set minimal scroll region and content frame size for empty data
            self.canvas.configure(scrollregion=(0, 0, 0, 100))
            self.content_frame.configure(height=100)
            return
        
        # Calculate total height needed for all data
        total_height = self.total_rows * self.row_height
        
        # Update canvas scroll region
        self.canvas.configure(scrollregion=(0, 0, 0, total_height))
        
        # Set content frame height to accommodate all data
        self.content_frame.configure(height=total_height)
        
        # Calculate visible rows
        canvas_height = self.canvas.winfo_height()
        if canvas_height > 1:
            self.visible_rows = min(canvas_height // self.row_height + 2, self.total_rows)
        
        # Reset last rendered range to force full refresh
        self.last_rendered_range = (-1, -1)
        
        # Update visible items
        self.update_visible_items()

    def update_visible_items(self):
        """Update which items are visible based on scroll position"""
        if self.total_rows == 0:
            self.hide_all_widgets()
            return
            
        # Calculate scroll position
        try:
            scroll_top = self.canvas.canvasy(0)
        except:
            scroll_top = 0
            
        # Calculate visible range with buffer
        first_row = max(0, int(scroll_top // self.row_height) - self.buffer_rows)
        last_row = min(self.total_rows - 1, first_row + self.visible_rows + self.buffer_rows * 2)
        
        # OPTIMIZATION: Only update if the range actually changed
        if (first_row, last_row) == self.last_rendered_range:
            return
        
        # Hide ALL widgets first
        for row_widgets in self.row_widgets:
            self.hide_widget_row(row_widgets)
        
        # Calculate how many rows we need to display
        rows_to_display = last_row - first_row + 1
        
        # Display data using available widgets
        for i in range(min(rows_to_display, len(self.row_widgets))):
            data_row_index = first_row + i
            
            if data_row_index < len(self.data):
                row_data = self.data[data_row_index]
                
                # Update widget content
                self.update_row_widget_content(i, row_data)
                
                # Calculate y position for this row
                y_position = data_row_index * self.row_height
                
                # Show widget at the correct y position
                self.show_widget_row(self.row_widgets[i], y_position, data_row_index)
        
        # Update last rendered range
        self.last_rendered_range = (first_row, last_row)

    def update_row_widget_content(self, widget_index, row_data):
        """Update widget content only"""
        if widget_index >= len(self.row_widgets):
            return
            
        widgets = self.row_widgets[widget_index]
        
        try:
            # Extract data with better error handling
            date = str(row_data[1]) if len(row_data) > 1 else "N/A"
            amount = float(row_data[2]) if len(row_data) > 2 and row_data[2] != '' else 0.0
            tag = str(row_data[3]) if len(row_data) > 3 else "N/A"
            desc = str(row_data[4]) if len(row_data) > 4 else "N/A"
            
            # Format amount with color
            amount_color = "#ff6b6b" if amount < 0 else "#51cf66"
            amount_text = f"${abs(amount):.2f}" if amount >= 0 else f"-${abs(amount):.2f}"
            
            # Update widget content
            widgets['date'].configure(text=date)
            widgets['amount'].configure(text=amount_text, text_color=amount_color)
            widgets['tag'].configure(text=tag)
            widgets['desc'].configure(text=desc)
            
            # Update delete button command
            transaction_id = row_data[0] if len(row_data) > 0 else None
            if transaction_id is not None:
                widgets['delete'].configure(command=lambda tid=transaction_id: self.delete_row(tid))
            else:
                widgets['delete'].configure(command=None)
            
        except Exception as e:
            print(f"Error updating row widget {widget_index}: {e}")
            # Clear the widgets if there's an error
            widgets['date'].configure(text="")
            widgets['amount'].configure(text="")
            widgets['tag'].configure(text="")
            widgets['desc'].configure(text="")

    def hide_all_widgets(self):
        """Hide all widgets efficiently"""
        for row_widgets in self.row_widgets:
            self.hide_widget_row(row_widgets)
        self.last_rendered_range = (-1, -1)

    def delete_row(self, transaction_id):
        # Remove from data
        self.data = [row for row in self.data if row[0] != transaction_id]
        
        # Refresh view
        self.refresh_view()
        
        # Call callback if provided
        if self.on_delete_callback:
            self.on_delete_callback(transaction_id)

    def on_canvas_configure(self, event):
        # Update canvas window width
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        # Refresh view to recalculate visible items and reposition widgets
        self.after_idle(self.refresh_view)

    def on_scrollbar_move(self, *args):
        self.canvas.yview(*args)
        # Use after_idle for smoother scrolling
        self.after_idle(self.update_visible_items)

    def on_mousewheel(self, event):
        # Calculate scroll direction
        if hasattr(event, 'delta') and event.delta:
            delta = -int(event.delta / 120)
        elif hasattr(event, 'num'):
            delta = -1 if event.num == 4 else 1
        else:
            return
            
        # Scroll the canvas
        self.canvas.yview_scroll(delta, "units")
        
        # Update visible items immediately for smooth scrolling
        self.update_visible_items()

    def update_data(self, new_data):
        """Update the table with new data"""
        self.data = new_data.copy() if new_data else []
        self.refresh_view()

    def sort_data(self, column_index, ascending=True):
        """Sort data by column and refresh view"""
        if not self.data:
            return
            
        try:
            if column_index == 1:  # Date
                self.data.sort(key=lambda x: x[1], reverse=not ascending)
            elif column_index == 2:  # Amount
                self.data.sort(key=lambda x: float(x[2]), reverse=not ascending)
            elif column_index == 3:  # Tag
                self.data.sort(key=lambda x: str(x[3]).lower(), reverse=not ascending)
            elif column_index == 4:  # Description
                self.data.sort(key=lambda x: str(x[4]).lower(), reverse=not ascending)

            self.refresh_view()
            
        except Exception as e:
            print(f"Error sorting data: {e}")