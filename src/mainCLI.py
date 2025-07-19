import transactions
import sqlite3
import os


def main():
    # Ottieni il path assoluto alla directory corrente (cioè src/database/)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "database/transactions.db")

    # Connessione al Database
    conn = sqlite3.connect(db_path)

    # Create the Object Transaction
    ts = transactions.Transactions(conn)

    # Example
    ts.add_transaction("19/21/2024", 50, "Needs", "Bought fruit and vegetables")
    ts.add_transaction("19/01/2024", -20, "Needs", "Bus pass for the week")
    ts.add_transaction("12/03/2024", 1500, "Salary", "Monthly salary deposit")
    ts.add_transaction("13/02/2024", -40, "Wants", "Cinema and dinner")
    ts.print_trans()

    # Close the connection with the database
    conn.close()


main()