"""
Virtual Table Implementation with Scrolling and Widget Reuse
============================================================

This module implements a high-performance virtual table for displaying large datasets
using CustomTkinter. The table uses widget pooling and absolute positioning to handle
thousands of rows efficiently while maintaining smooth scrolling performance.

Key Features:
- Virtual scrolling for performance with large datasets
- Widget pooling to minimize memory usage and improve rendering speed
- Absolute positioning using place() for precise control
- Real-time sorting and filtering support
- Integrated delete functionality with callbacks

Performance Optimizations:
- Only renders visible rows plus buffer
- Reuses widgets instead of creating/destroying them
- Batch updates to minimize UI redraws
- Efficient scroll event handling
"""

from src.views.base_view import BaseView
import customtkinter as ctk


class VirtualTable(BaseView):
    """
    High-performance virtual scrolling table implementation.
    
    Uses widget pooling and absolute positioning to efficiently display large datasets.
    Only renders visible rows plus a small buffer, dramatically improving performance
    compared to traditional approaches that render all data.
    """
    
    def __init__(self, parent, controller, data, on_delete_callback=None):
        super().__init__(parent)
        
        # Core dependencies and data
        self.controller = controller
        self.data = data
        self.on_delete_callback = on_delete_callback
        
        # Virtual scrolling configuration
        self.row_height = 40          # Fixed height per row for calculation accuracy
        self.visible_rows = 15        # Initial estimate of visible rows
        self.buffer_rows = 3          # Extra rows rendered above/below visible area
        self.total_rows = len(data)
        
        # Scroll and rendering state tracking
        self.scroll_top = 0
        self.first_visible_row = 0
        self.last_visible_row = 0
        self.last_rendered_range = (-1, -1)  # Optimization: track what was last rendered
        
        # Widget management
        self.row_widgets = []  # Pool of reusable widget sets
        
        # Initialize UI and start rendering
        self.setup_ui()
        self.after(100, self.refresh_view)  # Delay to ensure canvas is ready

    # =============================================================================
    # UI SETUP AND INITIALIZATION
    # =============================================================================
    
    def setup_ui(self):
        """
        Initialize the complete UI structure for virtual scrolling table.
        Creates canvas-scrollbar combination with internal content frame.
        """
        # Configure main container to expand properly
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create table container with dark theme
        self._create_table_container()
        
        # Create scrollable canvas with scrollbar
        self._create_scrolling_canvas()
        
        # Create content frame inside canvas for absolute positioning
        self._create_content_frame()
        
        # Setup event bindings for interaction
        self._bind_scroll_events()
        
        # Initialize widget pool for performance
        self.create_widget_pool()

    def _create_table_container(self):
        """Create the main container frame with proper theming."""
        self.table_container = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.table_container.grid(row=0, column=0, sticky="nsew", padx=30, pady=5)
        self.table_container.grid_columnconfigure(0, weight=1)
        self.table_container.grid_rowconfigure(0, weight=1)

    def _create_scrolling_canvas(self):
        """
        Create canvas for virtual scrolling with integrated scrollbar.
        Canvas enables precise control over rendering and scrolling behavior.
        """
        # Main scrollable canvas
        self.canvas = ctk.CTkCanvas(
            self.table_container,
            bg="#1a1a1a",
            highlightthickness=0,
            height=600
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Vertical scrollbar linked to canvas
        self.scrollbar = ctk.CTkScrollbar(
            self.table_container,
            command=self.on_scrollbar_move
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def _create_content_frame(self):
        """
        Create internal frame for absolute widget positioning.
        This frame serves as the coordinate space for place() geometry manager.
        """
        self.content_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas_window = self.canvas.create_window(0, 0, anchor="nw", window=self.content_frame)

    def _bind_scroll_events(self):
        """
        Setup event bindings for smooth scrolling across multiple widgets.
        Ensures mouse wheel works regardless of which component has focus.
        """
        # Canvas resize handling for responsive layout
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Mouse wheel support across all relevant widgets
        widgets_to_bind = [self, self.canvas, self.content_frame, self.table_container]
        for widget in widgets_to_bind:
            widget.bind("<MouseWheel>", self.on_mousewheel)     # Windows/Mac
            widget.bind("<Button-4>", self.on_mousewheel)       # Linux scroll up
            widget.bind("<Button-5>", self.on_mousewheel)       # Linux scroll down

    # =============================================================================
    # WIDGET POOL MANAGEMENT
    # =============================================================================
    
    def create_widget_pool(self):
        """
        Create reusable pool of widget sets for performance optimization.
        
        Widget pooling prevents constant creation/destruction of GUI elements,
        which is expensive. Instead, we create a fixed pool and reuse widgets
        by updating their content and position as needed.
        """
        # Calculate optimal pool size: visible area + buffer on both sides
        pool_size = max(20, self.visible_rows + self.buffer_rows * 2)
        
        # Create widget sets for each potential row
        for i in range(pool_size):
            row_widgets = self._create_widget_set()
            self.row_widgets.append(row_widgets)

    def _create_widget_set(self):
        """
        Create a complete set of widgets for one table row.
        Each set contains labels for data display and a delete button.
        """
        return {
            'date': ctk.CTkLabel(
                self.content_frame, 
                text="", 
                anchor="w", 
                width=150, 
                height=28
            ),
            'amount': ctk.CTkLabel(
                self.content_frame, 
                text="", 
                anchor="w", 
                width=120, 
                height=28
            ),
            'tag': ctk.CTkLabel(
                self.content_frame, 
                text="", 
                anchor="w", 
                width=120, 
                height=28
            ),
            'desc': ctk.CTkLabel(
                self.content_frame, 
                text="", 
                anchor="w", 
                width=200, 
                height=28
            ),
            'delete': ctk.CTkButton(
                self.content_frame,
                text="Delete",
                width=60,
                height=28,
                fg_color="#ff6b6b",
                hover_color="#ff5252",
                font=ctk.CTkFont(size=12)
            ),
            'visible': False,      # Track visibility state
            'data_row': -1         # Track which data row this widget set represents
        }

    # =============================================================================
    # WIDGET VISIBILITY MANAGEMENT
    # =============================================================================
    
    def hide_widget_row(self, row_widgets):
        """
        Efficiently hide a complete row of widgets.
        Uses place_forget() to remove widgets from layout without destroying them.
        """
        if row_widgets['visible']:
            # Hide all widgets in the row
            for widget_key in ['date', 'amount', 'tag', 'desc', 'delete']:
                row_widgets[widget_key].place_forget()
            
            # Update state tracking
            row_widgets['visible'] = False
            row_widgets['data_row'] = -1

    def show_widget_row(self, row_widgets, y_position, data_row):
        """
        Show and position a row of widgets using absolute positioning.
        
        Uses place() geometry manager for pixel-perfect control over widget positions.
        Calculates responsive column widths based on canvas size.
        """
        # Get current canvas width for responsive layout
        canvas_width = self._get_canvas_width()
        
        # Calculate column positions and widths
        positions, widths = self._calculate_column_layout(canvas_width)
        
        # Update widget sizes for responsive design
        self._resize_widgets(row_widgets, widths)
        
        # Position widgets using absolute coordinates
        self._position_widgets(row_widgets, positions, y_position)
        
        # Update state tracking
        row_widgets['visible'] = True
        row_widgets['data_row'] = data_row

    def _get_canvas_width(self):
        """Get canvas width with fallback for initialization."""
        canvas_width = self.canvas.winfo_width()
        return canvas_width if canvas_width > 1 else 800

    def _calculate_column_layout(self, canvas_width):
        """
        Calculate responsive column positions and widths.
        Returns positions and widths arrays for table columns.
        """
        # Column width ratios: Date, Amount, Tag, Description, Delete
        col_ratios = [0.2, 0.2, 0.2, 0.3, 0.1]
        
        # Calculate absolute positions
        positions = []
        current_x = 10  # Left padding
        
        for ratio in col_ratios:
            positions.append(current_x)
            current_x += int((canvas_width - 40) * ratio)  # 40px total padding
        
        # Calculate column widths (excluding delete button)
        widths = []
        for ratio in col_ratios[:-1]:
            widths.append(int((canvas_width - 40) * ratio - 10))  # 10px spacing
        
        return positions, widths

    def _resize_widgets(self, row_widgets, widths):
        """Update widget sizes for responsive layout."""
        widget_keys = ['date', 'amount', 'tag', 'desc']
        for key, width in zip(widget_keys, widths):
            row_widgets[key].configure(width=width)

    def _position_widgets(self, row_widgets, positions, y_position):
        """Position all widgets in a row using place() geometry manager."""
        row_widgets['date'].place(x=positions[0], y=y_position)
        row_widgets['amount'].place(x=positions[1], y=y_position)
        row_widgets['tag'].place(x=positions[2], y=y_position)
        row_widgets['desc'].place(x=positions[3], y=y_position)
        
        # Center delete button vertically within row
        row_widgets['delete'].place(x=positions[4], y=y_position + 6)

    def hide_all_widgets(self):
        """
        Hide all widgets in the pool efficiently.
        Used when clearing the table or switching to empty dataset.
        """
        for row_widgets in self.row_widgets:
            self.hide_widget_row(row_widgets)
        self.last_rendered_range = (-1, -1)  # Reset render tracking

    # =============================================================================
    # VIRTUAL SCROLLING CORE LOGIC
    # =============================================================================
    
    def refresh_view(self):
        """
        Complete refresh of the virtual table view.
        
        Recalculates scroll region, visible row count, and triggers full re-render.
        Called when data changes or window is resized.
        """
        self.total_rows = len(self.data)
        
        # Handle empty data case
        if self.total_rows == 0:
            self._handle_empty_data()
            return
        
        # Setup scrolling area for full dataset
        self._configure_scroll_region()
        
        # Recalculate visible row count based on current canvas size
        self._update_visible_row_count()
        
        # Force complete re-render
        self.last_rendered_range = (-1, -1)
        self.update_visible_items()

    def _handle_empty_data(self):
        """Configure table for empty dataset display."""
        self.hide_all_widgets()
        self.canvas.configure(scrollregion=(0, 0, 0, 100))
        self.content_frame.configure(height=100)

    def _configure_scroll_region(self):
        """Setup canvas scroll region based on total data size."""
        total_height = self.total_rows * self.row_height
        self.canvas.configure(scrollregion=(0, 0, 0, total_height))
        self.content_frame.configure(height=total_height)

    def _update_visible_row_count(self):
        """Calculate how many rows can fit in current canvas height."""
        canvas_height = self.canvas.winfo_height()
        if canvas_height > 1:
            self.visible_rows = min(
                canvas_height // self.row_height + 2, 
                self.total_rows
            )

    def update_visible_items(self):
        """
        Core virtual scrolling logic - update which rows are actually rendered.
        
        This is the performance-critical function that determines which data rows
        should be visible and updates the widget pool accordingly. Uses range
        comparison to avoid unnecessary re-renders.
        """
        if self.total_rows == 0:
            self.hide_all_widgets()
            return
        
        # Calculate current scroll position and visible range
        visible_range = self._calculate_visible_range()
        first_row, last_row = visible_range
        
        # OPTIMIZATION: Skip render if range hasn't changed
        if visible_range == self.last_rendered_range:
            return
        
        # Clear all widgets and render new range
        self._render_visible_range(first_row, last_row)
        
        # Update tracking for next optimization check
        self.last_rendered_range = visible_range

    def _calculate_visible_range(self):
        """
        Calculate which data rows should be rendered based on scroll position.
        Includes buffer rows above and below visible area for smooth scrolling.
        """
        try:
            scroll_top = self.canvas.canvasy(0)
        except:
            scroll_top = 0
        
        # Calculate visible range with buffer
        first_row = max(0, int(scroll_top // self.row_height) - self.buffer_rows)
        last_row = min(
            self.total_rows - 1, 
            first_row + self.visible_rows + self.buffer_rows * 2
        )
        
        return (first_row, last_row)

    def _render_visible_range(self, first_row, last_row):
        """
        Render the specified range of data rows using available widgets.
        Maps data rows to widget pool entries and updates their content/position.
        """
        # Hide all widgets first
        for row_widgets in self.row_widgets:
            self.hide_widget_row(row_widgets)
        
        # Calculate how many rows to display
        rows_to_display = last_row - first_row + 1
        available_widgets = len(self.row_widgets)
        
        # Display data using available widget pool
        for i in range(min(rows_to_display, available_widgets)):
            data_row_index = first_row + i
            
            if data_row_index < len(self.data):
                # Update widget content with current data
                row_data = self.data[data_row_index]
                self.update_row_widget_content(i, row_data)
                
                # Calculate absolute position for this row
                y_position = data_row_index * self.row_height
                
                # Show widget at calculated position
                self.show_widget_row(self.row_widgets[i], y_position, data_row_index)

    # =============================================================================
    # WIDGET CONTENT MANAGEMENT
    # =============================================================================
    
    def update_row_widget_content(self, widget_index, row_data):
        """
        Update widget content without changing position or visibility.
        
        Handles data formatting, color coding, and event binding.
        Includes error handling for malformed data rows.
        """
        if widget_index >= len(self.row_widgets):
            return
        
        widgets = self.row_widgets[widget_index]
        
        try:
            # Extract and validate data with fallbacks
            extracted_data = self._extract_row_data(row_data)
            
            # Update display widgets with formatted data
            self._update_display_widgets(widgets, extracted_data)
            
            # Setup delete button with transaction ID
            self._configure_delete_button(widgets, row_data)
            
        except Exception as e:
            print(f"Error updating row widget {widget_index}: {e}")
            self._clear_widget_content(widgets)

    def _extract_row_data(self, row_data):
        """Extract and format data from row with error handling."""
        date = str(row_data[1]) if len(row_data) > 1 else "N/A"
        
        # Handle amount with proper type conversion
        raw_amount = row_data[2] if len(row_data) > 2 and row_data[2] != '' else 0.0
        amount = float(raw_amount)
        
        tag = str(row_data[3]) if len(row_data) > 3 else "N/A"
        desc = str(row_data[4]) if len(row_data) > 4 else "N/A"
        
        return {
            'date': date,
            'amount': amount,
            'tag': tag,
            'desc': desc
        }

    def _update_display_widgets(self, widgets, data):
        """Update widget display content with proper formatting and colors."""
        # Format amount with appropriate color coding
        amount_color = "#ff6b6b" if data['amount'] < 0 else "#51cf66"
        amount_text = f"${abs(data['amount']):.2f}"
        if data['amount'] < 0:
            amount_text = f"-{amount_text}"
        
        # Update widget content
        widgets['date'].configure(text=data['date'])
        widgets['amount'].configure(text=amount_text, text_color=amount_color)
        widgets['tag'].configure(text=data['tag'])
        widgets['desc'].configure(text=data['desc'])

    def _configure_delete_button(self, widgets, row_data):
        """Setup delete button with appropriate transaction ID callback."""
        transaction_id = row_data[0] if len(row_data) > 0 else None
        
        if transaction_id is not None:
            widgets['delete'].configure(
                command=lambda tid=transaction_id: self.delete_row(tid)
            )
        else:
            widgets['delete'].configure(command=None)

    def _clear_widget_content(self, widgets):
        """Clear all widget content in case of errors."""
        for key in ['date', 'amount', 'tag', 'desc']:
            widgets[key].configure(text="")

    # =============================================================================
    # EVENT HANDLERS
    # =============================================================================
    
    def delete_row(self, transaction_id):
        """
        Handle row deletion with data update and UI refresh.
        Updates local data and triggers callback for database operations.
        """
        # Remove from local data copy
        self.data = [row for row in self.data if row[0] != transaction_id]
        
        # Refresh display with updated data
        self.refresh_view()
        
        # Notify parent component via callback
        if self.on_delete_callback:
            self.on_delete_callback(transaction_id)

    def on_canvas_configure(self, event):
        """
        Handle canvas resize events for responsive layout.
        Updates canvas window width and triggers view refresh.
        """
        # Update internal window width to match canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        # Refresh view for responsive repositioning
        self.after_idle(self.refresh_view)

    def on_scrollbar_move(self, *args):
        """
        Handle scrollbar movement events.
        Moves canvas view and updates visible items.
        """
        self.canvas.yview(*args)
        # Use after_idle for smoother scrolling performance
        self.after_idle(self.update_visible_items)

    def on_mousewheel(self, event):
        """
        Handle mouse wheel scrolling with cross-platform compatibility.
        Supports Windows (delta), Linux (num), and Mac scrolling.
        """
        # Calculate scroll direction based on event type
        if hasattr(event, 'delta') and event.delta:
            delta = -int(event.delta / 120)  # Windows/Mac
        elif hasattr(event, 'num'):
            delta = -1 if event.num == 4 else 1  # Linux
        else:
            return
        
        # Scroll canvas and update visible items immediately
        self.canvas.yview_scroll(delta, "units")
        self.update_visible_items()

    # =============================================================================
    # DATA OPERATIONS
    # =============================================================================
    
    def update_data(self, new_data):
        """
        Update table with completely new dataset.
        Handles None data gracefully and triggers full refresh.
        """
        self.data = new_data.copy() if new_data else []
        self.refresh_view()

    def sort_data(self, column_index, ascending=True):
        """
        Sort table data by specified column with type-aware comparison.
        
        Handles different data types appropriately:
        - Dates: string comparison (assumes ISO format)
        - Amounts: numeric comparison
        - Text fields: case-insensitive string comparison
        """
        if not self.data:
            return
        
        try:
            # Apply appropriate sorting based on column type
            if column_index == 1:  # Date column
                self.data.sort(key=lambda x: x[1], reverse=not ascending)
            elif column_index == 2:  # Amount column
                self.data.sort(key=lambda x: float(x[2]), reverse=not ascending)
            elif column_index == 3:  # Tag column
                self.data.sort(key=lambda x: str(x[3]).lower(), reverse=not ascending)
            elif column_index == 4:  # Description column
                self.data.sort(key=lambda x: str(x[4]).lower(), reverse=not ascending)

            # Refresh display with sorted data
            self.refresh_view()
            
        except Exception as e:
            print(f"Error sorting data: {e}")