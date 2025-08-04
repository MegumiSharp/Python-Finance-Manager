# CustomTkinter Grid Layout and Frame Architecture Documentation


This creates a seamless user experience where views can be switched instantly while preserving all internal state and layout configurations. 

## Table of Contents
1. [BaseView Foundation](#baseview-foundation)
1. [Hide/Show System Implementation](#hideshow-system-implementation)
2. [DashboardView Layout](#dashboardview-layout)
3. [HomeView Layout](#homeview-layout)
4. [SetupView Layout](#setupview-layout)
5. [WelcomeView Layout](#welcomeview-layout)
6. [Grid Weight System](#grid-weight-system)
8. [Best Practices](#best-practices)



## BaseView Foundation

The `BaseView` class serves as the foundation for all views in the application. It establishes the basic grid structure:

```python
class BaseView(ctk.CTkFrame, ABC):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent)
        # Setup the main frame grid
        self.grid_columnconfigure(0, weight=1)  # Single column expands
        self.grid_rowconfigure(0, weight=1)     # Single row expands
```

A 0x0 grid is all the available window space in the application.


```
┌─────────────────────────────────────┐
│            BaseView                 │
│  ┌─────────────────────────────────┐│
│  │         Column 0                ││
│  │       (weight=1)                ││
│  │                                 ││
│  │     Row 0 (weight=1)            ││
│  │                                 ││
│  │   [Child content goes here]     ││
│  │                                 ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```


## Hide/Show System Implementation

The application uses a sophisticated hide/show system that manages view transitions without destroying widgets. This system combines **pack geometry** for top-level view management with **grid geometry** for internal layouts.

The following code is in the abstract class BaseView and is inhinherited from all view in the application:


```python
def show(self):
    self.pack(fill="both", expand=True)

def hide(self):
    self.pack_forget()
```


The application uses a **hybrid geometry management** approach:

1. **Pack Geometry** - For top-level view switching (show/hide)
2. **Grid Geometry** - For internal widget layout within each view

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Application Window                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                BaseView Container                   │    │
│  │            [Using PACK geometry]                    │    │
│  │                                                     │    │
│  │    Currently Visible View (e.g., DashboardView)     │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │            main_frame                       │    │    │
│  │  │         [Using GRID geometry]               │    │    │
│  │  │                                             │    │    │
│  │  │  ┌─────────────┬─────────────────────────┐  │    │    │
│  │  │  │   Sidebar   │     Content Area        │  │    │    │
│  │  │  │  (Grid 0,0) │      (Grid 0,1)         │  │    │    │
│  │  │  │             │                         │  │    │    │
│  │  │  └─────────────┴─────────────────────────┘  │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Hidden Views (HomeView, SetupView, etc.)                   │
│  [Removed from pack but widgets preserved]                  │
└─────────────────────────────────────────────────────────────┘
```

It's simpler than it looks. Every view is in a "box," so to speak, that can be shown or hidden when needed. This removes the need to recreate the widgets in the view from scratch.


### View Lifecycle States

Each view goes through different states in its lifecycle:

#### 1. Initialization State
```python
def __init__(self, parent, controller=None, user=None):
    super().__init__(parent)  # Creates CTkFrame but doesn't display it
    self.setup_ui()           # Creates internal grid structure
    # View exists in memory but is not visible
```

#### 2. Showing State
```python
def show(self):
    self.pack(fill="both", expand=True)
    # View becomes visible and fills parent container
```

#### 3. Hidden State
```python
def hide(self):
    self.pack_forget()
    # View is removed from display but remains in memory
    # All internal grid structure is preserved
```

### DashboardView Dynamic Content Management

The Dashboard is a `view` with a sidebar containing different menu options and a main content area that changes when a menu option is selected. This creates a situation where we need to preserve the main content area when the user switches using the sidebar, because recreating all the widgets every time is very costly.

The `DashboardView` implements a sophisticated content switching system:

```python
def show_home_view(self):
    """Show the home view"""
    self.selected_button = self.home_button
    self.update_button_selection()

    if self.current_view:
        self.current_view.hide()  # Hide current view
    
    # Create home view if it doesn't exist (lazy loading)
    if self.home_view is None:
        self.home_view = HomeView(self.content_container, self.controller, self.user, self.data)
    
    self.current_view = self.home_view
    self.current_view.show()  # Show new view
```

### Content Container Architecture

The `content_container` in DashboardView acts as a dynamic viewport:

```
┌──────────────────────────────────────────────────────────────┐
│                      DashboardView                           │
│  ┌─────────────┬──────────────────────────────────────────┐  │
│  │   Sidebar   │           content_container              │  │
│  │             │        [Grid position 0,1]               │  │
│  │ ┌─────────┐ │                                          │  │
│  │ │  Home   │ │  ┌─────────────────────────────────────┐ │  │
│  │ │ [Active]│ │  │                                     │ │  │
│  │ └─────────┘ │  │         HomeView                    │ │  │
│  │ ┌─────────┐ │  │      [Currently Shown]              │ │  │
│  │ │ Budget  │ │  │                                     │ │  │
│  │ │         │ │  │    ┌─────────────────────────────┐  │ │  │
│  │ └─────────┘ │  │    │      Search Bar             │  │ │  │
│  │             │  │    └─────────────────────────────┘  │ │  │
│  │             │  │    ┌─────────────────────────────┐  │ │  │
│  │             │  │    │      Data Table             │  │ │  │
│  │             │  │    └─────────────────────────────┘  │ │  │
│  │             │  └─────────────────────────────────────┘ │  │
│  └─────────────┴──────────────────────────────────────────┘  │
│                                                              │
│  Hidden Views:                                               │
│  - BudgetView [In memory, not packed]                        │
│  - Future views [Created on demand]                          │
└──────────────────────────────────────────────────────────────┘
```

### Memory Management Strategy

The application uses different strategies for managing view instances:

#### 1. Singleton Pattern (HomeView)
Ensure that only one instance of a class exists throughout the apllication:

```python
# HomeView is created once and reused
if self.home_view is None:
    self.home_view = HomeView(self.content_container, self.controller, self.user, self.data)

self.current_view = self.home_view
self.current_view.show()
```



### Grid Preservation During Hide/Show

When a view is hidden using `pack_forget()`, its internal grid structure remains intact:

```
Hidden HomeView State:
┌─────────────────────────────────────────────────────────────────┐
│                    HomeView [Hidden]                            │
│  ┌─────────────────────────────────────┬────────────────────┐   │
│  │           Main Content              │    Summary Panel   │   │
│  │  ┌─────────────────────────────────┐│ ┌────────────────┐ │   │
│  │  │        Search Bar               ││ │  Transactions: │ │   │
│  │  │    [Grid preserved]             ││ │     [Cached]   │ │   │
│  │  └─────────────────────────────────┘│ └────────────────┘ │   │
│  │  ┌─────────────────────────────────┐│                    │   │
│  │  │      Virtual Table              ││    [All internal   │   │
│  │  │   [Data state preserved]        ││     state intact]  │   │
│  │  └─────────────────────────────────┘│                    │   │
│  └─────────────────────────────────────┴────────────────────┘   │
│                 [Not visible in UI]                             │
└─────────────────────────────────────────────────────────────────┘
```

This hide/show system provides several advantages:

1. **Fast Switching** - No widget reconstruction needed
2. **State Preservation** - User data, scroll positions, filter states remain
3. **Memory Efficiency** - Views are created only when needed
4. **Smooth Transitions** - No flickering or loading delays

### Implementation Pattern for New Views

When creating new views, follow this pattern:

```python
class NewView(BaseView):
    def __init__(self, parent, controller=None, user=None):
        super().__init__(parent)  # Inherits show/hide methods
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)  # Uses pack for main container
        
        # Configure grid for internal layout
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Use grid for all internal widgets
        widget.grid(row=0, column=0, sticky="nsew")
```

### Integration with Controller

The controller manages view transitions:

```python
def switch_frame(self, frame_name):
    # Hide current frame
    if hasattr(self, 'current_frame') and self.current_frame:
        self.current_frame.hide()
    
    # Show new frame
    self.current_frame = self.frames[frame_name]
    self.current_frame.show()
```


## DashboardView Layout

The `DashboardView` implements a **sidebar + content area** layout using a 2-column grid system.

### Grid Configuration
```python
self.main_frame.grid_rowconfigure(0, weight=1)
self.main_frame.grid_columnconfigure(0, weight=0)  # Sidebar - fixed width
self.main_frame.grid_columnconfigure(1, weight=1)  # Main content - expandable
```

DashboardView t


```
┌──────────────────────────────────────────────────────────┐
│                    DashboardView                         │
│  ┌─────────────┬──────────────────────────────────────┐  │
│  │   Sidebar   │          Content Area                │  │
│  │  Column 0   │           Column 1                   │  │
│  │ (weight=0)  │          (weight=1)                  │  │
│  │             │                                      │  │
│  │ ┌─────────┐ │  ┌─────────────────────────────────┐ │  │
│  │ │  Logo   │ │  │                                 │ │  │
│  │ └─────────┘ │  │        content_container        │ │  │
│  │ ┌─────────┐ │  │      (HomeView/BudgetView)      │ │  │
│  │ │  Home   │ │  │                                 │ │  │
│  │ └─────────┘ │  │                                 │ │  │
│  │ ┌─────────┐ │  │                                 │ │  │
│  │ │ Budget  │ │  │                                 │ │  │
│  │ └─────────┘ │  └─────────────────────────────────┘ │  │
│  └─────────────┴──────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### Key Components

1. **Sidebar (navigation_frame)**
   - Fixed width (300px)
   - Contains logo and navigation buttons
   - Uses vertical grid layout (rows 0-5)

2. **Content Container**
   - Expandable width (weight=1)
   - Hosts different views (HomeView, BudgetView)
   - Uses pack layout internally

## HomeView Layout

The `HomeView` implements a **main content + summary panel** layout with complex nested grids.


```python
self.main_frame.grid_rowconfigure(0, weight=1)
self.main_frame.grid_columnconfigure(0, weight=1)  # main_content_frame expands
self.main_frame.grid_columnconfigure(1, weight=0)  # summary_frame stays fixed
```


```
┌────────────────────────────────────────────────────────────────┐
│                           HomeView                             │
│  ┌─────────────────────────────────────┬────────────────────┐  │
│  │           Main Content              │    Summary Panel   │  │
│  │            Column 0                 │      Column 1      │  │
│  │          (weight=1)                 │     (weight=0)     │  │
│  │                                     │                    │  │
│  │  ┌─────────────────────────────────┐│ ┌────────────────┐ │  │
│  │  │        Search Bar               ││ │  Transactions: │ │  │  
│  │  │           Row 0                 ││ │       42       │ │  │  
│  │  └─────────────────────────────────┘│ ├────────────────┤ │  │
│  │  ┌─────────────────────────────────┐│ │    Income:     │ │  │  
│  │  │      Ordering Frame             ││ │   $1,250.00    │ │  │  
│  │  │           Row 1                 ││ │                │ │  │  
│  │  └─────────────────────────────────┘│ ├────────────────┤ │  │
│  │  ┌─────────────────────────────────┐│ │   Expenses:    │ │  │  
│  │  │                                 ││ │    $850.00     │ │  │  
│  │  │      Virtual Table              ││ │                │ │  │  
│  │  │         Row 2                   ││ ├────────────────┤ │  │
│  │  │      (weight=1)                 ││ │   Balance:     │ │  │  
│  │  │                                 ││ │   $400.00      │ │  │  
│  │  └─────────────────────────────────┘│ └────────────────┘ │  │
│  │  ┌─────────────────────────────────┐│                    │  │
│  │  │   Add Transaction Frame         ││                    │  │
│  │  │           Row 4                 ││                    │  │
│  │  └─────────────────────────────────┘│                    │  │
│  └─────────────────────────────────────┴────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### Main Content Frame Structure

The main content area uses a vertical layout with 5 rows:

```python
self.main_content_frame.grid_columnconfigure(0, weight=1)
self.main_content_frame.grid_rowconfigure(2, weight=1)  # Table expands vertically
```

1. **Row 0: Search Bar** - Fixed height search interface
2. **Row 1: Ordering Frame** - Filter buttons and column headers
3. **Row 2: Virtual Table** - Expandable data display (weight=1)
4. **Row 3: [Empty]** - Reserved for future content
5. **Row 4: Add Transaction** - Fixed height input form

## SetupView Layout

The `SetupView` uses a **sidebar + main content** layout similar to DashboardView but with different content organization.


```
┌────────────────────────────────────────────────────────────────┐
│                          SetupView                             │
│  ┌─────────────────┬────────────────────────────────────────┐  │
│  │    Sidebar      │           Main Content                 │  │
│  │   Column 0      │            Column 1                    │  │
│  │  (width=300)    │          (weight=1)                    │  │
│  │                 │                                        │  │
│  │ ┌─────────────┐ │  ┌──────────────────────────────────┐  │  │
│  │ │   Welcome   │ │  │                                  │  │  │
│  │ │   Header    │ │  │        Background Image          │  │  │
│  │ └─────────────┘ │  │                                  │  │  │
│  │ ┌─────────────┐ │  │  ┌─────────────────────────────┐ │  │  │
│  │ │   Welcome   │ │  │  │       Info Textbox          │ │  │  │
│  │ │   Textbox   │ │  │  │        Row 0                │ │  │  │
│  │ └─────────────┘ │  │  │      (weight=2)             │ │  │  │
│  │ ┌─────────────┐ │  │  └─────────────────────────────┘ │  │  │
│  │ │  Nickname   │ │  │  ┌─────────────────────────────┐ │  │  │
│  │ │   Input     │ │  │  │    Budget Rule Frame        │ │  │  │
│  │ └─────────────┘ │  │  │        Row 1                │ │  │  │
│  │ ┌─────────────┐ │  │  │      (weight=1)             │ │  │  │
│  │ │  Currency   │ │  │  │                             │ │  │  │
│  │ │  Selection  │ │  │  │  [Budget input fields]      │ │  │  │
│  │ └─────────────┘ │  │  └─────────────────────────────┘ │  │  │
│  │ ┌─────────────┐ │  └──────────────────────────────────┘  │  │
│  │ │  Continue   │ │                                        │  │
│  │ │   Button    │ │                                        │  │
│  │ └─────────────┘ │                                        │  │
│  └─────────────────┴────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

## WelcomeView Layout

The `WelcomeView` uses the simplest layout with overlapping elements.

```
┌────────────────────────────────────────────────────────┐
│                    WelcomeView                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │               Main Frame                         │  │
│  │            Single Column/Row                     │  │
│  │                                                  │  │
│  │    Background Image (grid position 0,0)          │  │
│  │                                                  │  │
│  │         ┌──────────────────────┐                 │  │
│  │         │   Welcome Widget     │                 │  │
│  │         │   (grid pos 0,0)     │                 │  │
│  │         │    sticky="ns"       │                 │  │
│  │         │                      │                 │  │
│  │         │  ┌────────────────┐  │                 │  │
│  │         │  │ Welcome Label  │  │                 │  │
│  │         │  └────────────────┘  │                 │  │
│  │         │  ┌────────────────┐  │                 │  │
│  │         │  │ Theme Selector │  │                 │  │
│  │         │  └────────────────┘  │                 │  │
│  │         │  ┌────────────────┐  │                 │  │
│  │         │  │ Continue Btn   │  │                 │  │
│  │         │  └────────────────┘  │                 │  │
│  │         └──────────────────────┘                 │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

## Grid Weight System

Understanding the `weight` parameter is crucial for responsive layouts:

### Weight=0 (Fixed Size)
- Element maintains its natural or specified size
- Does not expand when window is resized
- Used for sidebars, toolbars, fixed panels

### Weight=1 (Expandable)
- Element expands to fill available space
- Responsive to window resizing
- Used for main content areas

### Weight>1 (Proportional)
- Multiple elements with weights share space proportionally
- Weight=2 gets twice as much space as weight=1
- Used when you need specific size ratios


```python
# Scenario 1: Fixed sidebar + expandable content
grid_columnconfigure(0, weight=0)  # Sidebar stays 300px
grid_columnconfigure(1, weight=1)  # Content expands

# Scenario 2: Three-column layout with proportions
grid_columnconfigure(0, weight=1)  # 25% of space
grid_columnconfigure(1, weight=2)  # 50% of space  
grid_columnconfigure(2, weight=1)  # 25% of space

# Scenario 3: Header/content/footer
grid_rowconfigure(0, weight=0)     # Fixed header
grid_rowconfigure(1, weight=1)     # Expandable content
grid_rowconfigure(2, weight=0)     # Fixed footer
```

### Sticky Options
- `"nsew"` - Fill entire cell
- `"ns"` - Fill vertically only
- `"ew"` - Fill horizontally only
- `"n"`, `"s"`, `"e"`, `"w"` - Align to specific side

### Padding and Spacing
```python
# External spacing (between widget and cell border)
widget.grid(padx=20, pady=10)

# Internal spacing (within the widget)
widget.configure(border_width=5)
```

### Responsive Design Principles
1. Use weight=1 for main content areas
2. Use weight=0 for fixed-size panels
3. Configure sticky="nsew" for full cell expansion
4. Test layouts at different window sizes
5. Consider minimum window dimensions

### Common Layout Patterns

#### Two-Column Layout (Sidebar + Content)
```python
frame.grid_columnconfigure(0, weight=0)  # Sidebar
frame.grid_columnconfigure(1, weight=1)  # Content
```

#### Three-Row Layout (Header + Content + Footer)
```python
frame.grid_rowconfigure(0, weight=0)     # Header
frame.grid_rowconfigure(1, weight=1)     # Content
frame.grid_rowconfigure(2, weight=0)     # Footer
```

#### Grid Layout (Multiple equal cells)
```python
for i in range(rows):
    frame.grid_rowconfigure(i, weight=1)
for j in range(cols):
    frame.grid_columnconfigure(j, weight=1)
```


------------