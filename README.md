
<p align="center">
  <img src="assets/readme_images/banner.png" alt="Banner" />
</p>

# Expensia: A Personal Finance management appliction

## A small introduction to the project
Created as a project to sharpen my skillset on a real work environment, i spent roughly 130 hours on the project, (counted with a time tracking application) most of the time was spent on refactoring and learn to use the gui of python tkinter and his exstension customtkinter. The refactoring was largly done to make a better looking code and use some design pattern to create a better overall project. 

This project helped me reawaken my rusty programmer skill, and teached me the importance to plan ahead an application like this, beacuse, no matter how simple an application could seem to be, if you do  not plan ahead a lot of problems could accour. For an in-depth path of development check here : [here](docs/development_path.md)

Even if the application is functional, is far from perfect, and could benefit from more testing about the features and some feature added, however i decided to stop here, because i want to keep learning other technology and work on some other projects, however if some issues accour in the tab i will fix it.

Even if in relativly small part, for this project i used, sqlite3, json and csv files, and python as primary language, with customtkinter and tkinter library for the gui.



# What you can do with Expensia?

<p align="center">
  <img src="assets/readme_images/animation 1.gif" alt="animation" />
  <text> Live preview of the application<text>
</p>


Expensia is personal finance management application built in Python that helps you track expenses and giving you the power to filter this transactions and be able to see a budget rule, a way to handle where your moneys goes.

## 🚀 Features

- **Transaction Management**: Add, edit, and delete financial transactions with ease
- **Advanced Filtering**: Filter data by year, date, amount, expense type, income, and month for precise data visualization
- **SQLite Database**: All data is securely stored in a local SQLite database with automatic backup functionality
- **CSV Import/Export**: Import transactions from CSV files to database (creates automatic backup of previous database) and export data to CSV format
- **Fully Local**: All operations and data storage are completely local - no cloud dependency
- **Budget Planning**: Comprehensive budget view with the 50/30/20 rule implementation:
  - 50% for needs (essential expenses)
  - 30% for wants (lifestyle expenses) 
  - 20% for savings and debt repayment
  - **Customizable percentages** to fit your personal financial strategy
- **Data Backup**: Automatic database backup system to protect your financial data
- **Desktop GUI**: User-friendly graphical interface designed for intuitive desktop experience

## 🛠️ Technologies Used

- **Python**: Core programming language for application development
- **SQLite3**: Lightweight, local database engine for secure data storage and management
- **CSV Processing**: Built-in CSV module for seamless data import/export functionality
- **CustomTkinter**: Modern, customizable GUI framework for enhanced user interface design
- **Tkinter**: Native Python GUI toolkit providing foundational interface components
- **JSON**: Configuration file format for theme management and customization settings


## 📊 Screenshots


<p align="center">
  <text> Welcome View when starting the application<text>
  <img src="assets/readme_images/Welcome.png" />
    <text> Budget View<text>
  <img src="assets/readme_images/Budget View.png" />
      <text> Edit Button<text>
  <img src="assets/readme_images/edit.png" />
        <text> Backup View<text>
  <img src="assets/readme_images/Backup view.png" />
</p>





## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)


1. **Clone the repository**
   ```bash
   git clone git@github.com:MegumiSharp/Python-Finance-Manager.git
   cd Python-Finance-Manager
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python3 main.py
   ```

### Alternative Installation (without virtual environment)
If you prefer not to use a virtual environment:
```bash
pip install -r requirements.txt
python main.py
```

## Dependencies

This project uses the following main libraries:
- **customtkinter** - Modern UI library for tkinter
- **tkinter** - Built-in Python GUI library (included with Python)
- [List other major dependencies here]

## Troubleshooting

### Common Issues

**CustomTkinter not found:**
```bash
pip install customtkinter --upgrade
```

**Python version compatibility:**
- Ensure you're using Python 3.7+
- Check your Python version: `python --version`

**Virtual environment issues:**
- Make sure the virtual environment is activated
- Try recreating the virtual environment if problems persist

### Platform-Specific Notes

**Windows:**
- Use `python` and `pip` commands
- Activate venv with `venv\Scripts\activate`

**macOS/Linux:**
- Use `python3` and `pip3` if `python` points to Python 2
- Activate venv with `source venv/bin/activate`

## Development

To contribute or modify the project:

1. Fork the repository
2. Create a virtual environment and install dependencies
3. Make your changes
4. Test thoroughly
5. Submit a pull request





and from customtkinter theme builder by...




# Acknowledgements


Thanks to the **Python** community for creating and maintaining such a versatile programming language.  Thanks to the original **Tkinter** developers and maintainers for providing the foundation of Python’s standard GUI library. Thanks to the creators of **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** for modernizing Tkinter with beautiful, customizable widgets.  

Thanks to **[a13xe/CTkThemesPack](https://github.com/a13xe/CTkThemesPack)** for providing an excellent collection of themes to enhance the look and feel of CustomTkinter applications.  

-----------