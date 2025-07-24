import datetime
import transactions
import sqlite3
import os
from gui.app import App
import json

def is_valid_date(date : str):
    try:
        date_str = date.strip()
        datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return False
    

# Check if the user_settings.json exist, if not it create one
def create_user_settings_json():
    user_settings_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../usersettings/user_settings.json")

    deafult_data = {
        "theme" : "Default"
    }

    if not os.path.exists(user_settings_path):
        with open(user_settings_path, "w") as f:
            json.dump(deafult_data, f, indent=4)


# Inizialize the application window, if some error is finded is writed in the CLI
def main():
    # Initialize json file
    create_user_settings_json()
    
    # Ottieni il path assoluto alla directory corrente (cioè src/database/)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "database/transactions.db")

    # Connessione al Database
    conn = sqlite3.connect(db_path)

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