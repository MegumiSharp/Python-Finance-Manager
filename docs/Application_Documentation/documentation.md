


# Project Documentation

This documentation delves into my approach to using CustomTkinter and explains how the various parts of the program work. The project is intended as a learning and organizational exercise rather than as a production-ready application.

One of the most important elements in the program is the grid system—the internal layout system used by Tkinter and adopted by CustomTkinter to position elements within the window. This is one of the most critical aspects to understand, as it effectively defines the structure of the window and the GUI.

## File Structure

```
root/
├── assets/
│   └── themes/
│       ├── __init__.py
│       ├── Default.json
│       ├── NightTrain.json
│       ├── Orange.json
│       └── Sweetkind.json
├── backup/
│   └── .gitkeep
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── textbox.py
├── data/
│   ├── database/
│   │   └── .gitkeep
│   └── user_settings/
│       └── .gitkeep
├── docs/
│   ├── Application_Documentation/
│   │   ├── documentation.md
│   │   ├── observer_pattern.md
│   │   └── the_grid_layout.md
│   ├── development_path.md
│   └── user_guide.md
├── examples/
│   └── transactions.db
├── export/
│   └── .gitkeep
├── import/
│   └── .gitkeep
├── src/
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── app_controller.py
│   │   └── dashboard_controller.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── user_settings.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── views/
│       ├── __init__.py
│       ├── base_view.py
│       ├── budget_view.py
│       ├── home_view.py
│       ├── import_export_view.py
│       ├── setup_view.py
│       ├── virtual_table_view.py
│       └── welcome_view.py
├── .gitignore
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

---

## Why Use Python for a CRUD Application?

First, I need to discuss the choice of implementing this *project in Python with a GUI*. I'll start by saying that Python is an extremely powerful language, and the libraries available online allow you to do virtually anything you want, but that doesn't mean it's the right thing to do or the best method to accomplish it.

Just look at the graphical library I'm using: creating widgets and frames requires a considerable number of lines of code, which leads to less immediate code maintainability and comprehension.

While Python technically supports multi-threading, it's not very good at it due to some specific issues, like the fact that only one thread can execute Python code at a time. Threading is mostly useful for I/O-bound tasks, not CPU-intensive operations.

For this reason, the GUI ends up being more **static than it appears**. This is because, apart from certain specific widgets, GUI operations must run on the main thread to handle events properly.

A problem I encountered was the creation of rows for each transaction—an action that (for tables larger than 400 entries) increased the program's loading time up to 5 seconds. Fortunately, I found a less elegant but more optimized solution.

CRUD (Create, Read, Update, Delete) applications are not particularly complex in themselves, but they are an excellent source of learning. My stubbornness, given my recent study of Python, led me to continue wanting to create such an application in this language even though it's not the optimal way to do it.

Python, as I said, is very powerful, but is best suited for:
- Scripting and automation
- Web scraping and data analysis
- Rapid prototyping
- Backend development

I'm confident in saying that GUI libraries certainly don't expect the quantity of elements and frames that I've created and intend to create.

In short, the only reason I decided to continue down this path is because I'm less interested in the application itself and more interested in the journey of commitment and study I'm undertaking.

### Technologies I'm Learning Through This Project

- Python with CustomTkinter library
- JSON file implementation
- SQLite3 database usage
- MVC design pattern implementation

These are all things I've never done before. Pushing in this direction, I believe that while it may not lead to an overly ambitious project (at least theoretically), it will certainly be a well-documented, structured, and composed project to demonstrate my commitment in this regard.

## MVC Design Pattern Implementation

The application demonstrates a thoughtful implementation of the **Model-View-Controller** design pattern, adapted specifically for GUI development with CustomTkinter.

### Model Layer

The model layer in the application primarily consists of the `UserSettings` class and database integration components. The `UserSettings` serves as the central repository for application configuration, managing everything from user preferences like nickname and currency selection to complex budget rule percentages. This model handles the persistence of data through JSON file operations and provides a clean interface for other components to access and modify application state.

The database integration represents another aspect of the model layer, handling transaction data through `sqlite3`. The model provides methods for **creating**, **reading**, **updating**, and **deleting** financial transactions while maintaining data integrity and providing efficient access patterns for the user interface components.

### Controller Layer

The `AppController` serves as the central coordinator for the application, managing the overall application lifecycle and handling navigation between different views. This controller demonstrates the Front Controller pattern by providing a single entry point for all navigation decisions and view transitions.

### View Layer

The view architecture centers around the `BaseView` abstract class, which establishes a consistent interface for all user interface components. This abstract base class serves as more than just a common parent; it enforces architectural standards by requiring all views to implement the `setup_ui` method while providing common functionality for showing and hiding views.

### Architecture Benefits

The overall architecture provides a solid foundation for future development while remaining approachable for learning and maintenance. The clear structure and consistent patterns make the codebase accessible to other developers while the performance optimizations ensure the application remains responsive as it scales. This balance between theoretical soundness and practical effectiveness represents the hallmark of mature software architecture.

## Configuration Files and Directories

- `assets/` contains the background used in the `setup` and `welcome` views. It also includes icons and themes.
- `themes/` contains JSON files with `customtkinter` variables and methods that change the color of all the widgets.
- `config/` contains settings and textboxes used throughout the source code.
- `transactions.db` is a database containing the user's transaction table. **It is created empty at the start of the application.**
- `user_settings.json` is a simple way to store user settings, such as the currency symbol.
- `docs/` contains the documentation, code of conduct, and other documents to make the project more professional.

A brief explanation about `config`, and more precisely `settings.py`: In the code, I often needed to declare paths to files and reuse many string values in different situations—such as the app name, version, etc. The `settings.py` file contains constants for all the strings and numbers used frequently in the source code.

The presence of `__init__.py` tells Python to treat the folder it is in as a package that can be imported. In this project, all these files are empty and are used solely to improve the readability of the package structure.

### `settings.py` and `textbox.py`

While writing the code using `customtkinter`, I frequently needed to handle various strings, sometimes to represent plain text, and other times to define file `paths`. Even when dealing with simple text strings, they were often tied to fundamental aspects of the application's configuration—such as `window_width` or `available_currencies`. These values are not meant to change dynamically during the execution of the application, **but they might reasonably change between versions or for different deployments**.

For instance, if I wanted to update the color used to represent expenses to a different shade of red in the future, I would need to manually search through every file where that color value is used—an inefficient and error-prone process.

To address this, I made what may be considered an unpopular design choice: I centralized all such configuration values into a single `settings.py` file. This file acts as a collection of `constants` used throughout the program. The benefit is clear—any significant behavior or style change can be made easily and safely in one place.

A potentially controversial aspect of this approach is how I handled default user settings. In `settings.py`, I created constants not only for the default values but also for the corresponding keys. This might appear unusual, but the motivation is straightforward: **avoiding typos**. By defining these strings as constants, any mistake in their usage becomes immediately detectable by the interpreter or static analysis tools.

At the end of the project, I plan to run performance tests to assess whether this approach has introduced any measurable slowdown. However, for the time being, I consider it a worthwhile trade-off in favor of readability and code maintainability—goals I have deliberately prioritized throughout the development process.

Similar to `settings.py`, the file `textbox.py` stores all the textboxes used throughout the application—essentially, very long strings. This centralization helps keep the code organized by grouping large blocks of text in one place, making them easier to manage and update.

> I won't go into detail about the constants used in this file, as its content is straightforward and easy to understand for everyone.

## `main.py`

The main function is used to start the application. As a debugging method, it uses the `traceback` module, which provides a history of the function calls that led to the point where an exception or error occurred. This allows any error that happens within the program to not only be caught, but also traced back to the main function. It's a very useful module for debugging purposes.

The `main` itself doesn't contain much logic: it simply creates an instance of the `AppController` class—which we'll discuss later—and then calls the `mainloop()` function. This function is provided by the `customtkinter` module and is essential for managing the graphical interface of the application.

Another useful feature is `app.protocol`, which is a way to call the function `on_closure` of AppController when the application is closed. This is done to ensure that a closing popup appears and some saving is done in the background.

One of the most common Python idioms is: `if __name__ == "__main__":` It controls when the code runs depending on how the Python file is used, only running the `main()` if the script is being run directly and not when it's imported.

## `app_controller.py` – Application Controller Overview

This file serves as the **controller** in the MVC architecture of the application. Originally responsible for the entire GUI, it was later refactored to manage only the logic of switching between views (frames), keeping the code modular and maintainable.

Inherits from `customtkinter.CTk` to manage the main application window and leverage extended `customtkinter` features.

```python
class AppController(customtkinter.CTk):
```

When an instance is created:
- The application window is initialized.
- Constants from `settings.py` are applied (e.g., window size, title, theme).
- A `UserSettings` instance is created to manage persistent data in a JSON file.
- The method `__startup()` is called to determine the first screen to display.

Some settings are configured using constants defined in `settings.py`, including the window size, title, theme, and whether the window is resizable (although this last setting doesn't work perfectly).
Additionally, a connection is made to a `user_settings.json` file. If the file doesn't exist, it gets created.

Each newly created view receives:

* A reference to this file (`controller`)
* A reference to the window (`self`)
* A reference to the (`user_settings`)

These references are crucial for operations like setting the grid layout and calling methods such as `switch_frame` from within the views.

### Key Components

**`current_view`**: A variable that stores the currently displayed view. Initially, it's empty. When `__show_view()` is called, it is assigned the instance of the view to be shown. Each view inherits from an abstract class that defines `.show()` and `.hide()` methods to display or hide the view in the window.

**`_show_view()` and `self.views`**: At startup, a dictionary is created that maps view classes to their instances. This dictionary is used by `_show_view()`:
  * If a view is currently active, it gets hidden.
  * If the requested view is already in the dictionary, it's reused.
  * If not, it's instantiated and added to the dictionary.
  * Finally, `current_view` is updated to the requested view.

This approach allows for the reuse of view instances from the beginning to the end of the application, enabling efficient switching through `switch_frame()`.

`_hide_or_destroy_current_view` is self-explanatory, deciding to hide a view or destroy it based on whether the view is needed after the first time.

`on_closure` makes a message box appear to confirm the exit of the application. This calls `on_closure` of the dashboard controller to ensure changes made are saved.

## `base_view.py`

This is a base class, or abstract class, for all views in the application. It provides a common interface and basic functionality for all views. Each view **inherits** from this class and implements the `setup_ui` method. The core features of this class are the `show` and `hide` methods.

Each view uses the `grid` functionality of **CustomTkinter** to arrange widgets in an invisible grid inside the window. Although it is generally best **not to mix** `pack` and `grid` (because `pack` stacks widgets one after another, either top to bottom or left to right), we only use the `pack` feature inside the base view.

Here's how it works: when creating a view, like `SetupView`, it uses `grid` to position widgets **inside its frame**, but the frame itself is **not initially placed** anywhere in the window. The frame is just initialized and not yet added to the window.

Using the `show` function, the frame widget is packed into the window. Because all the widgets are inside the frame, this method makes it easy to show and hide entire views. Each view acts like a container, and calling `show` from the base view packs the container into the window.

```
+----------------------------------+
|           Main Window            |
|                                  |
|   +--------------------------+   | <-- frame (view container)
|   |   Frame (initially NOT   |   |     contains widgets arranged by grid
|   |   packed in window)      |   |
|   |                          |   |
|   |  +-------+  +--------+   |   | <-- widgets positioned by grid inside frame
|   |  |Label  |  | Entry  |   |   |
|   |  +-------+  +--------+   |   |
|   |                          |   |
|   +--------------------------+   |
|                                  |
+----------------------------------+

BaseView.show() method:
- Calls `frame.pack()` to add the frame to the window,
  making all the widgets inside visible.

BaseView.hide() method:
- Calls `frame.pack_forget()` to remove the frame from the window,
  hiding the entire view.
```

The following code present in the file:
```python
self.grid_columnconfigure(0, weight=1)
self.grid_rowconfigure(0, weight=1)
```
Creates a grid with 1 column and one row, essentially a rectangle that expands in the window created by customtkinter. Referring to the ASCII drawing, the grid will be created inside the various views and will be positioned in row 0 and column 0, essentially inside the main window.

## `setup_view.py` - First Startup Configuration for the User

This file is responsible for creating a view or frame with configuration elements for the user. This type of configuration includes:

- **Nickname** - Used for the welcome screen
- **Currency Sign** - The symbol to use in transactions to identify whether we're talking about euros, dollars, or pounds
- **Budget Rule Percentages** - A system for budget organization dedicated to setting aside money, necessary expenses like bills, and superfluous expenses

Additionally, this screen has useful information as an introductory and explanatory screen outside of the GitHub repo. It's possible that additional elements may be added.

Regarding the code in the `__init__`, you'll find the code necessary to inherit from the parameters when the class instance is called, such as controller and user_settings (json), in addition to inheriting from `BaseView`. Generally, all views have a similar appearance.

```python
# This is the constructor of the SetupView class, it initializes the view and sets up the UI
def __init__(self, parent, controller=None, user=None):
    super().__init__(parent, controller, user)
    self.controller = controller
    self.user = user

    # Inherit the grid from the baseview and then expand on the window, this is done to have a responsive frame
    self.main_frame = ctk.CTkFrame(self, corner_radius=0)
    self.main_frame.pack(fill="both", expand=True)
    
    # Configure the main frame to use grid for sidebar and content area
    self.main_frame.grid_rowconfigure(0, weight=1)
    self.main_frame.grid_columnconfigure(0, weight=0)  # Sidebar - fixed width
    self.main_frame.grid_columnconfigure(1, weight=1)  # Main content - expandable
    self.main_frame.grid(row=0, column=0, sticky="nsew")

    # Creates the widgets in the frames
    self.setup_ui()
```

The code comments itself, but like the next view, we inherited the baseview grid and expand it on the window with pack, then we apply the grid we want. When we are finished with this view, calling `.hide()` will hide the view.

## `welcome_view.py`

A simple view for the start of the program that welcomes the user. The user can choose a theme before continuing to the dashboard.

Like other views, we use the self baseview grid to create a frame and then create a grid on top of it. This is a simple grid 0x0, like the baseview. It is important to notice that even if the grid is equal to the baseview, it is **needed** to ensure the central bar scales according to the size of the window.

```python
# Create main content frame from the baseview
self.main_frame = ctk.CTkFrame(self, corner_radius=0)
self.main_frame.pack(fill="both", expand=True)

# Configure the main frame to use grid for sidebar and content area
self.main_frame.grid_rowconfigure(0, weight=1)
self.main_frame.grid_columnconfigure(0, weight=1)
self.main_frame.grid(row=0, column=0, sticky="nsew")
```


## `dashboard_controller.py` - Centralized navigation controller

The `dashboard_controller.py` serves as a centralized navigation controller for the Expensia application. While the app controller manages the overall application flow, the dashboard controller specifically handles the main interface with its sidebar navigation and dynamic content switching.

The dashboard controller was designed as a separate component to maintain clean code architecture and scalability. Rather than creating a single monolithic `dashboard_view` file that would contain all views (home_view, budget_view, import_export_view), which would exceed 1500 lines of code, the solution adopts a modular approach where:

- The dashboard controller manages the sidebar navigation
- Each main content area is implemented as a separate view file
- Views are instantiated once and switched dynamically for better performance
- The design acts as an extension of the app controller pattern



```python
def __init__(self, parent, controller=None, user=None):
    super().__init__(parent)
    self.controller = controller
    self.user = user
    self.data = DatabaseManager()
    self.current_view = None
    
    # Create main content frame
    self.main_frame = ctk.CTkFrame(self, corner_radius=0)
    self.main_frame.pack(fill="both", expand=True)
    
    # Configure grid layout: sidebar (column 0) + content area (column 1)
    self.main_frame.grid_rowconfigure(0, weight=1)
    self.main_frame.grid_columnconfigure(0, weight=0)  # Sidebar - fixed width
    self.main_frame.grid_columnconfigure(1, weight=1)  # Main content - expandable
```

The dashboard creates a database connection that can be shared among all views. It implements a two-column grid layout where:
- **Column 0**: Fixed-width sidebar for navigation
- **Column 1**: Expandable content area for views

The `weight` configuration ensures the sidebar maintains its intended size without expanding to fill available space.


The controller maintains a dictionary of view instances (`self.views`) and a current view tracker (`self.current_view`). This approach enables fast view switching without recreating objects, improving performance and maintaining state between switches.



The sidebar navigation is implemented with:
- **Logo and branding**: App name and logo at the top
- **Navigation buttons**: Dynamically created buttons with icons
- **Visual feedback**: Selected button highlighting
- **Scalable design**: Easy addition of new navigation options

One of the strongest features of the dashboard controller is its scalability. Adding a new navigation button requires minimal code changes.



Adding a new button is straightforward. Here's an example for adding a "Tag" view:

```python
# 1. Import the new view
from src.views.tag_view import TagView

# 2. Add icon in __init__
self.icons = {
    # ... existing icons
    TagView: ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "tag_view.png")), size=(20, 20))
}

# 3. Add view instance
self.views = {
    # ... existing views
    TagView: TagView(self.content_container, controller=self.controller, user=self.user, database=self.data)
}

# 4. Create button in setup_ui (remember to increment the row number)
self.tag_button = self.__create_button(
    frame=self.navigation_frame, 
    text="Tag", 
    instance=TagView
)
self.tag_button.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
self.buttons[TagView] = self.tag_button
```

 `setup_ui()`
Creates the sidebar interface including:
- Application logo and title
- Navigation buttons with icons
- Grid layout configuration

`__create_button(frame, text, instance)`
Generic button factory method that:
- Creates styled navigation buttons
- Configures click handlers
- Associates buttons with view instances
- Maintains consistent styling across all buttons

 `__update_button_selection(view_class)`
Manages visual feedback by:
- Highlighting the currently selected button
- Resetting other buttons to default state
- Providing clear visual indication of active view

`switch_main_content_frame(view_class)`
Handles view transitions by:
- Updating button selection visual state
- Hiding the current view
- Showing the requested view
- Executing view-specific initialization (e.g., data updates for BudgetView)

 `on_closure()`
Manages cleanup operations when the dashboard is closed, ensuring proper resource disposal.


The **HomeView** receives special treatment due to its complexity. As the most important view containing the main data table, the table component is implemented as a separate object instantiated within the HomeView, maintaining clean separation of concerns while keeping related functionality together.

## **`budget_view.py`** - Budget Controller

The Budget view handles displaying the screen for budget management and visualization. More details about this can be found in the [user guide](docs/user_guide.md). In the class constructor, we have several variables that are useful for budget management, some of which are taken from the user_settings.json file which is also updated based on various functions.

The `BudgetView` module provides a graphical interface to display and monitor the user's monthly budget following the 50/30/20 rule (or custom percentages):
- **Needs**: Essential expenses
- **Wants**: Non-essential expenses  
- **Savings**: Money to be set aside


The `BudgetView` class inherits from `BaseView` and requires the following parameters:
- `parent`: Parent widget
- `controller`: Application controller
- `user`: User object for settings
- `database`: Database for transactions

**Budget Configuration:**
- `needs_percentage`, `wants_percentage`, `savings_percentage`: Custom percentages from settings file
- `currency_sign`: User's currency symbol

**Calculation Variables:**
- `needs_spent/budget`, `wants_spent/budget`, `saving_spent/savings_budget`: Spent amounts and allocated budgets
- `salary`: Total monthly salary
- `monthly_savings_allocated`: Savings allocated from current month's salary

**UI References:**
- Labels, progress bars and amount displays for each category


`setup_ui()`
Builds the graphical interface with:
- Header with "Budget" title and current month
- Colored sections for Needs (green), Wants (red), Savings (purple)
- Progress bars to visualize budget usage
- Labels to show spent/available amounts
- Information about salary and monthly savings

`calculator()`
Processes transaction data:
- Filters transactions for the current month (`budget_filter`)
- Categorizes expenses by tag (Needs, Wants, Salary, Saving)
- Calculates total spent per category
- Determines savings allocation from salary

 `update_display()`
Updates the interface with calculated values:
- Calculates each category's budget based on salary
- Updates progress bars (red if budget exceeded)
- Shows remaining amounts for savings
- Applies warning colors for overages

 `update_data_and_recalculate()`
Public method to reload data from database and recalculate values when necessary.

**Income:** "Salary" tags are considered positive income that determines the total budget.

**Expenses:** "Needs" and "Wants" tags are expenses (negative amounts) that reduce available budget.

**Savings:** "Saving" tags represent withdrawals from savings (negative amounts), while a percentage of salary is automatically allocated to savings.


## **`import_export_view.py`** - Import/Export Controller

The Import/Export view handles displaying the screen for database import/export operations and backup management. This module allows users to transfer their financial data in and out of the application, as well as create and restore backups for data safety.


The `ImportExport` module provides a graphical interface to:
- **Import** financial data from CSV files into the application database
- **Export** current database content to CSV format for external use
- **Backup** current database to a secure backup location
- **Restore** previous backups to recover lost or corrupted data



The `ImportExport` class inherits from `BaseView` and requires the following parameters:
- `parent`: Parent widget
- `controller`: Application controller
- `user`: User object for settings
- `database`: Database object for data operations



**Data References:**
- `data`: Local reference to database content (`database.local_db`)

**UI Components:**
- Text box displaying import/export instructions
- Import/Export buttons for data transfer operations
- Backup/Restore buttons for data safety operations

`setup_ui()`
Builds the graphical interface with:
- Header with "Import / Export Database" title
- Instructional text box with usage guidelines
- Import and Export buttons for data transfer
- Backup Current and Restore Backup buttons for data safety
- Responsive grid layout for optimal spacing

`import_event()`
Handles importing data from CSV files:
- Reads CSV file from predefined import folder path
- Validates each row for correct date format and numeric values
- Creates automatic backup before import operation
- Updates local database with imported data
- Restarts application to reflect changes
- Shows error messages for invalid data entries

`export_event()`
Handles exporting current database to CSV:
- Extracts data from local database (excluding internal IDs)
- Writes formatted data to CSV file in export folder
- Displays success confirmation to user
- Handles file writing errors gracefully

`backup_current_event()`
Creates backup of current database:
- Copies current database file to backup location
- Shows confirmation message upon successful backup
- Handles backup creation errors

`restore_backup_event()`
Restores database from backup:
- Checks if backup file exists
- Requests user confirmation before overwriting current data
- Copies backup file to main database location
- Restarts application to load restored data
- Shows appropriate error messages if backup not found



**`is_file_legal()`**: Validates entire CSV file structure and content

**`_is_valid_date()`**: Validates individual date entries using YYYY-MM-DD format



**Import Process:**
1. Reads CSV from `IMPORT_FOLDER_PATH`
2. Validates date format (YYYY-MM-DD) and numeric amounts
3. Creates automatic backup before import
4. Updates database with new data
5. Restarts application

**Export Process:**
1. Extracts current database content
2. Filters out internal database IDs
3. Writes clean data to `EXPORT_FOLDER_PATH`
4. Confirms successful export

**Backup Operations:**
- **Backup**: Copies database to `BACKUP_FOLDER_PATH`
- **Restore**: Overwrites current database with backup file

### Error Handling

- **File Not Found**: Shows appropriate error messages for missing files
- **Data Validation**: Identifies specific rows with invalid date or amount data
- **Import Errors**: Creates backup before import to prevent data loss
- **User Confirmation**: Requests confirmation for potentially destructive operations

### Visual Interface

- **Dark theme** consistent with application design
- **Instructional text box** with detailed usage guidelines
- **Centered button layout** for easy access to operations
- **Clear labeling** for import, export, backup, and restore functions
- **Responsive design** that adapts to different window sizes


## **`virtual_table.py`** - Virtual Table Controller

The Virtual Table is a scrollable table component created from database raw data using custom widgets. This module handles the display, interaction, and management of financial transactions in a table format with full CRUD (Create, Read, Update, Delete) operations.

The `VirtualTable` module provides a dynamic, interactive table interface to:
- **Display** financial transactions in a scrollable, responsive layout
- **Edit** transaction details through modal dialogs
- **Delete** transactions with confirmation prompts
- **Filter** transactions by income, expenses, date ranges, or search terms
- **Sort** transactions by date or amount in ascending/descending order
- **Calculate** real-time summaries of visible transactions


The `VirtualTable` class inherits from `BaseView` and requires:
- `parent`: Parent widget container
- `controller`: Application controller for dialog management
- `database`: Database object for data operations
- `user`: User object for settings (currency sign)

**Data Management:**
- `data`: Reference to database local data (`database.local_db`)
- `db_transactions`: Queue for batch database operations
- `currency_sign`: User's currency symbol from settings

**UI Components:**
- `widgets_list`: Stores all row frame widgets for dynamic management
- `edit_image`, `delete_image`: Icons for action buttons
- `summary_callback`: Callback function for summary updates

**Layout Structure:**
- `table_container`: Main container frame
- `scroll_frame`: Scrollable frame for transaction rows


`setup_ui()`
Creates the main table structure:
- Configures scrollable container with dark theme
- Sets up mouse wheel scrolling for all platforms (Windows, macOS, Linux)
- Generates individual row widgets from database data
- Establishes responsive grid layout

`create_row(data_row)`
Generates individual transaction row widgets:
- **Responsive columns**: Date (15%), Amount (15%), Tag (15%), Description (40%), Edit (5%), Delete (5%)
- **Color coding**: Green for income, red for expenses, custom colors for tags
- **Action buttons**: Edit and delete buttons with icons and hover effects
- **Proper alignment**: Left-aligned text fields, right-aligned amounts


#### Core Display Methods
- **`show_all()`**: Displays all transactions and resets scroll position
- **`hide_all()`**: Hides all transactions from view
- **`show_income(date, month)`**: Shows only positive amount transactions
- **`show_expenses(date, month)`**: Shows only negative amount transactions

#### Search and Filter
- **`show_searched(text)`**: 
  - Performs text search across all transaction fields
  - Special shortcuts: "-" shows expenses, "+" shows income
  - Case-insensitive search through date, amount, tag, and description

#### Date Filtering
- **`filter_dates(date_value, month_value)`**: Filters transactions by year and/or month
- **`get_dates()`**: Extracts unique years from data for filter dropdown menus

#### Delete Operations
**`__delete_button_event(idx)`**: Creates confirmation dialog with:
- Transaction details display with color-coded fields
- Confirmation and cancel buttons
- Automatic cleanup of existing dialogs

**`_ok_event(frame, idx)`**: Executes deletion and updates summary
**`_cancel_event(frame)`**: Cancels deletion operation

#### Edit Operations
**`__edit_button_event(idx)`**: Creates edit dialog with:
- Pre-populated entry fields with current values
- Real-time validation for date and amount formats
- Color and font updates based on new values

**`_confirm_edit(frame, idx)`**: Validates and applies changes:
- Date format validation (YYYY-MM-DD)
- Numeric amount validation
- Updates widget appearance and database queue

**`update_row_colors(amount, tag, idx)`**: Updates visual styling based on new values


#### `order_by_date(state=[False])`
- Toggles between ascending/descending date order
- Maintains current filter state
- Only affects visible transactions

#### `order_by_amount(state=[False])`
- Sorts by numeric amount value (not string)
- Preserves income/expense filtering
- Updates display without losing current filters


#### `register_summary_callback(callback_function)`
Registers callback for summary updates in parent view

#### `_notify_summary_changed()`
Triggers summary recalculation when data changes

#### `_calculate_summary()`
Calculates real-time statistics from visible transactions:
- Total transaction count
- Total income (positive amounts)
- Total expenses (negative amounts) 
- Current balance (income + expenses)


#### Batch Transaction System
**`save_db_modification(action, row_id, ...)`**: Queues database operations
- **DELETE**: Removes transaction by database ID
- **EDIT**: Updates transaction fields
- **ADD**: Creates new transaction entry

**`update_db()`**: Processes queued operations in batch
- Commits all changes to database
- Updates local data cache
- Clears transaction queue for performance

### Visual Interface Features

- **Dark theme** with consistent color scheme
- **Responsive design** adapting to window size changes
- **Color-coded** amounts (green for income, red for expenses)
- **Tag highlighting** with custom colors and bold fonts
- **Smooth scrolling** with mouse wheel support
- **Modal dialogs** for edit and delete confirmations
- **Real-time updates** of summaries and visual indicators
- **Hover effects** on action buttons for better user experience

## **`home_view.py`** - Home View Controller

The Home View serves as the main dashboard containing the transaction table, summary panel, and transaction controls. This module implements filtering, sorting, and CRUD operations for financial transactions, providing the primary interface for managing personal finances.


The `HomeView` module provides a comprehensive dashboard interface to:
- **Display** all financial transactions in a scrollable table format
- **Summarize** financial data with real-time statistics (income, expenses, balance)
- **Filter** transactions by date ranges, amounts, or search terms
- **Sort** transactions by date or amount in ascending/descending order
- **Add** new transactions through an integrated form
- **Manage** user preferences and filter states



The `HomeView` class inherits from `BaseView` and requires:
- `parent`: Parent widget container
- `controller`: Application controller for navigation
- `user`: User object for settings and preferences
- `database`: Database object for transaction data


**Core Dependencies:**
- `data`: Reference to database local data
- `currency_sign`: User's currency symbol from settings
- `label_text`: StringVar for status message display

**User Preferences:**
- `current_date_selection`: Currently selected year filter
- `current_month_selection`: Currently selected month filter

**UI Components:**
- `transactions_table`: VirtualTable instance for transaction display
- `summary_labels`: Dictionary of summary statistic labels
- `search_var`: StringVar for real-time search functionality



`setup_ui()`
Creates the main dashboard layout with:
- **Two-column layout**: Main content area (expandable) and summary panel (fixed width)
- **Main content components**: Search bar, sorting controls, transaction table, add form
- **Summary panel**: Statistics display and filter controls
- **Message box**: Status message display at bottom

#### Layout Structure
- **Left side**: Search, filters, table, transaction form (expandable)
- **Right side**: Summary statistics and filter controls (250px fixed width)
- **Responsive design**: Main content expands while summary stays consistent


#### `search_bar_frame()`
Creates real-time search interface:
- **Search entry**: Text input with magnifying glass icon
- **Real-time callback**: Uses StringVar trace for instant search results
- **Integration**: Directly calls VirtualTable search methods


#### `setup_summary_panel()`
Creates comprehensive statistics display:
- **Transaction count**: Total number of visible transactions
- **Income total**: Sum of positive amounts (green color)
- **Expenses total**: Sum of negative amounts (red color)
- **Balance calculation**: Income minus expenses with dynamic color coding

#### `on_summary_updated(summary_data)`
Callback function for real-time summary updates:
- Updates all summary labels with formatted currency values
- Applies dynamic color coding based on positive/negative balance
- Triggered automatically when table data changes



#### Tabbed Filter Interface
**Filter Tab:**
- **Amount filters**: Income, Expenses, All buttons
- **Quick access**: Single-click filtering with status messages

**Dates Tab:**
- **Year selector**: Dropdown with available years from data
- **Month selector**: Dropdown with all months plus "All" option
- **Persistent state**: Remembers user selections across sessions

#### Filter Event Handlers
- **`on_date_changed(value)`**: Updates year filter and refreshes display
- **`on_month_changed(value)`**: Updates month filter and refreshes display
- **`reset_data_filters()`**: Resets all filters to "All" state



#### Add Transaction Form
**`add_transaction_frame(main_frame)`**: Creates input form with:
- **Date entry**: YYYY-MM-DD format with placeholder
- **Amount entry**: Numeric input for transaction value
- **Category entry**: Tag/category for transaction
- **Description entry**: Optional description field
- **Submit button**: Processes and validates new transactions

#### `add_transaction()`
Processes new transaction submissions:
- **Input validation**: Checks required fields and date format
- **Database integration**: Queues transaction for batch processing
- **UI updates**: Refreshes table display and applies current filters
- **Error handling**: Shows appropriate error messages for invalid input
- **Form clearing**: Resets all input fields after successful submission



#### `message_box()`
Creates status message display area:
- **Dynamic messages**: Shows current operation status
- **Color coding**: Different colors for success, error, and info messages
- **Real-time updates**: Changes based on user actions

#### `change_message_home_view(new_message, new_color)`
Updates status messages with:
- Custom message text
- Color coding for message type
- Immediate visual feedback to users



#### `ordering_frame(main_frame)`
Creates table header with sorting controls:
- **Column headers**: Date, Amount, Tag, Description, Actions
- **Sort buttons**: Interactive buttons for Date and Amount columns
- **Responsive layout**: Proportional column widths matching table
- **Visual feedback**: Shows current sort status in messages


#### `on_closure()`
Handles application shutdown:
- **State persistence**: Saves current filter selections to user settings
- **Database commit**: Processes all queued database operations
- **Clean shutdown**: Ensures no data loss on application exit

#### `save_btn_event()`
Manual save functionality:
- **Batch processing**: Commits all pending database changes
- **User feedback**: Shows success message after save completion
- **Data integrity**: Ensures all modifications are persisted


**VirtualTable Integration:**
- **Callback registration**: Links summary updates to table changes
- **Filter coordination**: Synchronizes filter states between components
- **Data consistency**: Maintains synchronized view of transaction data

**User Settings Integration:**
- **Preference persistence**: Saves filter states and user choices
- **Currency formatting**: Uses user's preferred currency symbol
- **Cross-session continuity**: Restores previous session state

### Visual Interface

- **Dark theme**: Consistent with application design
- **Responsive layout**: Adapts to different window sizes
- **Color coding**: Green for income, red for expenses, dynamic balance colors
- **Status feedback**: Real-time messages for all user actions
- **Professional appearance**: Clean, organized layout with proper spacing
- **Accessibility**: Clear labels and logical tab order for keyboard navigation

-------------