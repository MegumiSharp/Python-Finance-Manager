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
    
    

def add_transaction_prompt():
    print("\n--- Aggiungi nuova transazione ---")
    

    data = input("Inserisci la data (es. 19/02/2025): ").strip()

    while True:
        try:
            soldi = float(input("Inserisci l'importo (es. 25.50): ").strip())
            break
        except ValueError:
            print("Errore: inserisci un numero valido.")

    tag = input("Inserisci il tag (es. spesa, stipendio, etc.): ").strip()

    descrizione = input("Inserisci una descrizione: ").strip()

    transazione = [data, soldi, tag, descrizione]

    print("Transazione aggiunta:", transazione)
    return transazione



def main():
    # Ottieni il path assoluto alla directory corrente (cioè src/database/)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "database/transactions.db")

    # Connessione al Database
    conn = sqlite3.connect(db_path)

    # Create the Object Transaction
    ts = transactions.Transactions(conn)

    add_transaction_prompt()
    # Example
    ts.add_transaction(None, 50, None, "Bought fruit and vegetables")
    ts.add_transaction("19/21/2024", 50, "Needs", "Bought fruit and vegetables")
    ts.print_trans()


    # Close the connection with the database
    conn.close()


main()