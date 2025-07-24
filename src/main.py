import datetime
import transactions
import sqlite3
import os
from gui.app import *

def is_valid_date(date : str):
    try:
        date_str = date.strip()
        datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return False
    

# Inizialize the application window, if some error is finded is writed in the CLI
def main():
    
    # Ottieni il path assoluto alla directory corrente (cioè src/database/)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "database/transactions.db")

    # Connessione al Database
    conn = sqlite3.connect(db_path)

    # Create the Object Transaction
    ts = transactions.Transactions(conn)

    # Example
    ts.add_transaction("19/06/2024", 50, "Needs", "Bought fruit and vegetables")
    ts.add_transaction("20/06/2024", 1200, "Income", "Freelance payment")
    ts.add_transaction("21/06/2024", 30, "Wants", "Cinema night")
    ts.add_transaction("22/06/2024", 75, "Needs", "Grocery shopping")
    ts.add_transaction("23/06/2024", 45, "Needs", "Gas for car")
    ts.add_transaction("24/06/2024", 15, "Wants", "Coffee and pastry")
    ts.add_transaction("25/06/2024", 200, "Income", "Sold old books")
    ts.add_transaction("26/06/2024", 65, "Needs", "Pharmacy")
    ts.add_transaction("27/06/2024", 25, "Wants", "Bought a T-shirt")
    ts.add_transaction("28/06/2024", 90, "Needs", "Utility bill")
    ts.add_transaction("29/06/2024", 55, "Wants", "Online game purchase")
    ts.add_transaction("30/06/2024", 1300, "Income", "Salary")
    ts.add_transaction("01/07/2024", 22, "Needs", "Lunch out")
    ts.add_transaction("02/07/2024", 40, "Wants", "Movie rental and snacks")
    ts.add_transaction("03/07/2024", 70, "Needs", "Monthly transport pass")
    ts.add_transaction("04/07/2024", 600, "Income", "Project milestone payment")
    ts.add_transaction("05/07/2024", 38, "Needs", "Laundry and cleaning supplies")
    ts.add_transaction("06/07/2024", 10, "Wants", "Ice cream")
    ts.add_transaction("07/07/2024", 22, "Needs", "Public transport")
    ts.add_transaction("08/07/2024", 400, "Income", "Refund from insurance")
    ts.add_transaction("09/07/2024", 60, "Needs", "Groceries")
    ts.add_transaction("10/07/2024", 15, "Wants", "Mobile game microtransaction")
    ts.add_transaction("11/07/2024", 90, "Needs", "Internet and phone bill")
    ts.add_transaction("12/07/2024", 300, "Income", "Sold used electronics")
    ts.add_transaction("13/07/2024", 18, "Needs", "Breakfast at café")
    ts.add_transaction("14/07/2024", 45, "Wants", "Dinner with friends")
    ts.add_transaction("15/07/2024", 28, "Needs", "Household items")
    ts.add_transaction("16/07/2024", 150, "Income", "Tutoring session")
    ts.add_transaction("17/07/2024", 55, "Needs", "Pet supplies")
    ts.add_transaction("18/07/2024", 80, "Wants", "Concert ticket")
    ts.add_transaction("19/07/2024", 25, "Needs", "Groceries")
    ts.add_transaction("20/07/2024", 100, "Income", "Reimbursed travel expense")
    ts.add_transaction("21/07/2024", 33, "Needs", "Weekly groceries")
    ts.add_transaction("22/07/2024", 12, "Wants", "Smoothie")
    ts.add_transaction("23/07/2024", 45, "Needs", "Train fare")
    ts.add_transaction("24/07/2024", 1100, "Income", "Monthly paycheck")
    ts.add_transaction("25/07/2024", 19, "Needs", "Toiletries")
    ts.add_transaction("26/07/2024", 50, "Wants", "Video game DLC")
    ts.add_transaction("27/07/2024", 66, "Needs", "Grocery store run")
    ts.add_transaction("28/07/2024", 17, "Wants", "Pizza night")
    ts.add_transaction("29/07/2024", 150, "Income", "Sold bicycle")
    ts.print_trans()

    try:
        app = App()
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