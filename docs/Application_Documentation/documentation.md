#  Documentation

Here is the documentation for the project, which delves into my approach to using customtkinter and explains how the various parts of the program work. The project is intended as a learning and organizational exercise rather than as a production-ready application.

One of the most important elements in the program is the grid system—the internal layout system used by Tkinter and adopted by CustomTkinter to position elements within the window. This is one of the most critical aspects to understand, as it effectively defines the structure of the window and the GUI.
For a deeper explanation of how it works and how to manage it, refer to this [section](/docs/Application_Documentation/the_grid_layout.md).

**File Tree:** 
```
(project root)
│
├── main.py
├── app_controller.py
├── config/
│   ├── settings.py
│   ├── textbox.py
│   └── __init__.py
├── assets/
├── themes/
├── docs/
├── user_settings.json
├── transactions.db
└── ...
```


# Index

1. [Why use Python for a CRUD application?](#why-use-python-for-a-crud-application)
2. [Pattern MVC](#mvc-design-pattern-implementation)
3. [Configuration: File e Directory](#configuration-files-and-directory)
4. [`settings.py` e `textbox.py`](#settingspy-e-textboxpy)
5. [`main.py`](#mainpy)
6. [`app_controller.py`](#app_controllerpy--application-controller-overview)


-------

# Why use Python for a CRUD application? 
First of all, I need to discuss the choice of implementing this *project in Python with a GUI*. I'll start by saying that Python is an extremely powerful language, and the libraries available online allow you to do virtually anything you want, but that doesn't mean it's the right thing to do or the best method to do it.
Just look at the graphical library I'm using: creating widgets and frames requires a considerable number of lines of code, which leads to less immediate code maintainability and comprehension.

While Python technically supports multi-threading, it's not very good at it due to some specific issues, like that only one thread can execute Python code at a time, threading is mostrly usefull for I/O-Bound taks, not CPU.

For this reason the GUI ends up being more **static than it appears**. This is because, apart from certain specific widgets, the GUI operations must run on the main thread to handle events properly.

A problem I encountered regarding this was the creation of rows for each transaction - an action that (for tables larger than 400 entries) increased the program's loading time up to 5 seconds. Fortunately, I found a less elegant but more optimized solution, which you can learn more about [here](#tableview.py).

CRUD (Create, Read, Update, Delete) applications are not particularly complex in themselves, but they are an excellent source of learning. My stubbornness, given my recent study of Python, led me to continue wanting to create such an application in this language even though it's not the optimal way to do it.

Python as i said is very powerfull, but is best suited for:
- Scripting and automation
- Web scraping and data analysis
- Rapid prototyping
- Backend development

I'm confident in saying that GUI libraries certainly don't expect the quantity of elements and frames that I've created and intend to create.

In short, the only reason I decided to continue down this path is because I'm less interested in the application itself and more interested in the journey of commitment and study I'm undertaking.

Technologies I'm learning through this project:

- Python with CustomTkinter library
- JSON file implementation
- SQLite3 database usage
- MVC design pattern implementation

These are all things I've never done before. Pushing in this direction, I believe that while it may not lead to an overly ambitious project (at least theoretically), it will certainly be a well-documented, structured, and composed project to demonstrate my commitment in this regard.


# MVC Design Pattern Implementation

The application demonstrates a thoughtful implementation of the **Model-View-Controller** design pattern, adapted specifically for GUI development with CustomTkinter. Rather than following a rigid textbook approach, the implementation shows a mature understanding of how MVC principles can be practically applied to real-world software development challenges.

The model layer in the application primarily consists of the `UserSettings` class and database integration components. The `UserSettings` serves as the central repository for application configuration, managing everything from user preferences like nickname and currency selection to complex budget rule percentages. This model handles the persistence of data through JSON file operations and provides a clean interface for other components to access and modify application state.

The database integration represents another aspect of my model layer, handling transaction data through `sqlite3`. The model provides methods for **creating**, **reading**, **updating**, and **deleting** financial transactions while maintaining data integrity and providing efficient access patterns for the user interface components.


The `AppController` serves as the central coordinator for the application, managing the overall application lifecycle and handling navigation between different views. This controller demonstrates the Front Controller pattern by providing a single entry point for all navigation decisions and view transitions.


My view architecture centers around the `BaseView` abstract class, which establishes a consistent interface for all user interface components. This abstract base class serves as more than just a common parent; it enforces architectural standards by requiring all views to implement the setup_ui method while providing common functionality for showing and hiding views.


The overall architecture provides a solid foundation for future development while remaining approachable for learning and maintenance. The clear structure and consistent patterns make the codebase accessible to other developers while the performance optimizations ensure the application remains responsive as it scales. This balance between theoretical soundness and practical effectiveness represents the hallmark of mature software architecture.


# Configuration Files and Directory

- `assets\` contains the background used in the `setup` and `welcome` views. It also includes icons and themes.  
- `themes\` contains JSON files with `customtkinter` variables and methods that change the color of all the widgets.  
- `config\` contains settings and textboxes used throughout the source code.  
- `transactions.db` is a database containing the user's transaction table. **It is created empty at the start of the application.**  
- `user_settings.json` is a simple way to store user settings, such as the currency symbol.  
- `docs\` contains the documentation, code of conduct, and other documents to make the project more professional.  


A brief explanation about `config`, and more precisely `settings.py` In the code, I often needed to declare paths to files and reuse many string values in different situations — such as the app name, version, etc. The `settings.py` file contains constants for all the strings and numbers used frequently in the source code.  
More information can be found in [this chapter](#settingspy-and-textboxpy).


The presence of `__init__.py` tells Python to treat the folder it is in as a package that can be imported.  
In this project, all these files are empty and are used solely to improve the readability of the package structure.



## `settings.py` and `textbox.py`

While writing the code using `customtkinter`, I frequently needed to handle various strings, sometimes to represent plain text, and other times to define file `paths`. Even when dealing with simple text strings, they were often tied to fundamental aspects of the application's configuration—such as `window_width` or `available_currencies`. These values are not meant to change dynamically during the execution of the application, **but they might reasonably change between versions or for different deployments**.

For instance, if I wanted to update the color used to represent expenses to a different shade of red in the future, I would need to manually search through every file where that color value is used—an inefficient and error-prone process.

To address this, I made what may be considered an unpopular design choice: I centralized all such configuration values into a single `settings.py` file. This file acts as a collection of `constants` used throughout the program. The benefit is clear—any significant behavior or style change can be made easily and safely in one place.

A potentially controversial aspect of this approach is how I handled default user settings. In `settings.py`, I created constants not only for the default values but also for the corresponding keys. This might appear unusual, but the motivation is straightforward: **avoiding typos**. By defining these strings as constants, any mistake in their usage becomes immediately detectable by the interpreter or static analysis tools.

At the end of the project, I plan to run performance tests to assess whether this approach has introduced any measurable slowdown. However, for the time being, I consider it a worthwhile trade-off in favor of readability and code maintainability—goals I have deliberately prioritized throughout the development process.

Similar to `settings.py`, the file `textbox.py` stores all the textboxes used throughout the application—essentially, very long strings. This centralization helps keep the code organized by grouping large blocks of text in one place, making them easier to manage and update.

>I won’t go into detail about the constants used in this file, as its content is straightforward and easy to understand for everyone.

## `Main.py`

The main function is used to start the application. As a debugging method, it uses the `traceback` module, which provides a history of the function calls that led to the point where an exception or error occurred. This allows any error that happens within the program to not only be caught, but also traced back to the main function. It's a very useful module for debugging purposes.

The `main` itself doesn't contain much logic: it simply creates an instance of the `AppController` class — which we’ll discuss later — and then calls the `mainloop()` function. This function is provided by the `customtkinter` module and is essential for managing the graphical interface of the application.

One of the most commone Python idioms is: `if __name__ == "__main__":` It controls when the cose is runs depending on how the Python file is used, onlyt run the `main()` if the script is being run directly and not when it's imported.



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


**`current_view`**:
  A variable that stores the currently displayed view. Initially, it's empty. When `__show_view()` is called, it is assigned the instance of the view to be shown.
  Each view inherits from an abstract class that defines `.show()` and `.hide()` methods to display or hide the view in the window.

**`_show_view()` and `self.views`**: At startup, a dictionary is created that maps view classes to their instances.

This dictionary is used by `_show_view()`.
  * If a view is currently active, it gets hidden.
  * If the requested view is already in the dictionary, it's reused.
  * If not, it's instantiated and added to the dictionary.
  * Finally, `current_view` is updated to the requested view.

This approach allows for the reuse of view instances from the beginning to the end of the application, enabling efficient switching through `switch_frame()`.

`_hide_or_destroy_current_view` is self explainatory, decide to hide a view or destroy based on if the view is needed or not after the first time.


## `BaseView.py`

This is a base class, or abstract class, for all views in the application. It provides a common interface and basic functionality for all views. Each view **inherits** from this class and implements the `setup_ui` method. The core features of this class are the `show` and `hide` methods.

Each view uses the `grid` functionality of **CustomTkinter** to arrange widgets in an invisible grid inside the window. Although it is generally best **not to mix** `pack` and `grid` (because `pack` stacks widgets one after another, either top to bottom or left to right), we only use the `pack` feature inside the base view.

Here’s how it works: when creating a view, like `SetupView`, it uses `grid` to position widgets **inside its frame**, but the frame itself is **not initially placed** anywhere in the window. The frame is just initialized and not yet added to the window.

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

Il seguente codice presente nel file:
```python
  self.grid_columnconfigure(0, weight=1)
  self.grid_rowconfigure(0, weight=1)
```
Crea una griglia con 1 colonna e una riga, a tutti gli effetti un rettangolo che si espande nella finestra
creata da customtkinter, riprendendo il disegnino in ascii, la griglia sará creata dentro le varie view e sará posizionato in riga 0 e colonna 0 a tutti gli effetti all'interno della finestra principale.


## `setup_view.py` - First Startup configuration for the User

Questo file si interessa di creare una view o un frame con all'interno degli elementi di configurazione del programma per l'utente. Questo tipo di configurazione riguardono il:

- Nickname - Utilizzato per la schermata di welcome
- Currencu Sign - Il simbolo da utilizzare nelle transazioni per identificare se si parla di euro, dollari o pounds
- Percentuali per il budget rule - Un sistema per l'organizzazione del budget dedicato a mettere da parte, spese necessarie tipo bollette e spese superflue

Inoltre in questa schermata ci sono delle informazioni utile come schermata introduttiva ed esplicativa al di fuori della repo github. É possibile che ulteriori elementi possano essere aggiunti.

![setup view](/assets/images/docs_image/setup_view1.png)

Per quanto riguarda il codice nel `__init__` si trova il codice necessario per ereditare dai parametri di quando l'istanza della classe verra chiamata, come controller e user_settings (json), oltre che l'ereditarietá di `BaseView`, generalemnte tutte le view hanno un aspetto simile.

```python
# This is the constructor of the SetupView class, it initializes the view and sets up the UI
def __init__(self, parent, controller=None, user=None):
    super().__init__(parent, controller, user)
    self.controller = controller
    self.user = user

    # Inherite the grid from the baseview and than expand on the window, this is done to have  a responsive frame
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

The code comments itself, but like the next view, we inherited the baseview grid and expand it on the windows, with pack, than we apply the grid we want, when we are tired of this view, doing .hide will hide the view.


## `welcome_view.py`

A simple view for the start of the program, welcome the user. The user can choose a theme before continue to the dashboard.

![Welcome View](/assets/images/docs_image/welcome_view1.png)

Like other view we use the self baseview grid to create a frame and the create a grid on top of it. This is a simple grid  0x0, like th ebaseview. It is impotant to notice that even if the grid is equal to the baseview, is **needed** to ensure the central bar scale according to the size of the windows

```python
# Create main content frame from the baseview
self.main_frame = ctk.CTkFrame(self, corner_radius=0)
self.main_frame.pack(fill="both", expand=True)

# Configure the main frame to use grid for sidebar and content area
self.main_frame.grid_rowconfigure(0, weight=1)
self.main_frame.grid_columnconfigure(0, weight=1)
self.main_frame.grid(row=0, column=0, sticky="nsew")

```

## `dashboard_controller.py` - Centralized application

Questo file é un controller della dashboard, benché sia anche una view effettiva dell'applicazione. Inizialmente era una view e basta che gestiva le altre view, ma mi é sembrato giusto renderla un controller poiché questo fa.

Una volta entrati nella dashboard, veniamo accolti dalla main home con tutte le transazioni da poter fare.

![Dashboard View](/assets/images/docs_image/dashboard_view1.png)

A sinistra abbiamo una sidebar per navigare all'interno della dashboard. 

```python
def __init__(self, parent, controller=None, user=None):
    super().__init__(parent)
    self.controller = controller
    self.user = user
    self.data = DatabaseManager()
    self.current_view = None
    self.views = {} 

    # Create main content frame
    self.main_frame = ctk.CTkFrame(self, corner_radius=0)
    self.main_frame.pack(fill="both", expand=True)
    
    # Configure the main frame to use grid for sidebar and content area
    self.main_frame.grid_rowconfigure(0, weight=1)
    self.main_frame.grid_columnconfigure(0, weight=0)  # Sidebar - fixed width
    self.main_frame.grid_columnconfigure(1, weight=1)  # Main content - expandable

    # Create a content container for the views (this will use pack)
    self.content_container = ctk.CTkFrame(self.main_frame, corner_radius=0)
    self.content_container.grid(row=0, column=1, sticky="nsew")

    self.setup_ui()   
```

Nella dashboard creiamo effettivament la connessione al `database`, questo é utile pe ruan delle view che andremo ad utilizzare poi. Come ogni altra view, la dashboard necessita di prendere da `baseview` e creare una grid sopra di essa. Questa grid ha 1 riga e 2 colonne, due colonne perché una conterrá la sidebar e una conterrá le varie view che potremo selezionare dalla sidebar. Da notare il `weight` delle due colonne, fatt e in questo modo cosi che la sidebar non prenda tutto lo spazio ma solo la grandezza che noi li diciamo.

Utilizziamo lo stesso metodo di app controller tenendo una variabile che indica la current-view e un dizionario di oggetti contenenti tutte le views, cosi da poterle cambiare a piacimento senza necessitá di ricrearle e quindi rendere piú veloce lo switch intra dashboard


One of the most strong feature of the dashboard_controller is the scalability, adding a button is easy as writing 5 lines of code. It probably could be further improved, but for now it's ok.

### How to create a New Button
Creating a new Button is very simple, let's say we need a tag button:

```python
#In the import
from src.views.budget_view import TagView

# In innit
self.icons = {
  ...
  TagView = ctk.CTkImage(Image.open(os.path.join(ICONS_PATH, "tag_view.png")), size=(20, 20))
}

self.views = {
  ...
  TagView = TagView(self.content_container, controller=self.controller, user=self.user, database=self.data)
}

# In setup_ui
...
# Tag button (remembter to increase row )
self.tag_button = self.__create_button(frame =self.navigation_frame, text = "Tag", istance = TagView,)
self.tag_button.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
self.buttons[TagView] = self.tag_button
```



## `home_view.py`