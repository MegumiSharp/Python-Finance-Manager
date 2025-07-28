import datetime
from src import transactions
import sqlite3
import os
import json

"""
Expensia - Personal Finance Tracker
Entry point for the application
"""
from config.settings import (USER_SETTINGS_PATH, DATABASE_PATH, DEFAULT_USER_SETTINGS)

from src.core.app import App



def is_valid_date(date : str):
    try:
        date_str = date.strip()
        datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return False
    

# Check if the user_settings.json exist, if not it create one
def create_user_settings_json():
    if not os.path.exists(USER_SETTINGS_PATH) or os.path.getsize(USER_SETTINGS_PATH) == 0:
        with open(USER_SETTINGS_PATH, "w") as f:
            json.dump(DEFAULT_USER_SETTINGS, f, indent=4)


# Inizialize the application window, if some error is finded is writed in the CLI
def main():
    # Initialize json file
    create_user_settings_json()
    

    # Connessione al Database
    conn = sqlite3.connect(DATABASE_PATH)

    # Create the Object Transaction
    ts = transactions.Transactions(conn)

    try: 
        app = App(ts)
        app.mainloop()
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()                                            # Close the Database

# Make the script executed only when directily runned
if __name__ == "__main__":
    main()