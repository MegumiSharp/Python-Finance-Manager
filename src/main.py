import datetime
import transactions
import sqlite3
import os


def is_valid_date(date : str):
    try:
        date_str = date.strip()
        datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return False
    
    
def main():
    # Ottieni il path assoluto alla directory corrente (cioè src/database/)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "database/transactions.db")

    # Connessione al Database
    conn = sqlite3.connect(db_path)

    # Create the Object Transaction
    ts = transactions.Transactions(conn)

    # Example
    ts.add_transaction(None, 50, None, "Bought fruit and vegetables")
    ts.add_transaction("19/21/2024", 50, "Needs", "Bought fruit and vegetables")
    ts.print_trans()


    # Close the connection with the database
    conn.close()


main()