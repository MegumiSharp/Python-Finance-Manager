import sqlite3
import os

# Ottieni il path assoluto alla directory corrente (cioè src/database/)
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "transactions.db")

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Creo la tabella transactions se non esiste
c.execute(
    '''CREATE TABLE IF NOT EXISTS transactions (
        date TEXT,
        amount FLOAT,
        tag TEXT,
        desc TEXT
    )'''
)

# Dati da inserire
transactions_data = [
    ("19/21/2024", 50, "Needs", "Bought fruit and vegetables"),
    ("19/01/2024", -20, "Needs", "Bus pass for the week"),
    ("12/03/2024", 1500, "Salary", "Monthly salary deposit"),
    ("13/02/2024", -40, "Wants", "Cinema and dinner"),
]

# Inserimento dati
c.executemany("INSERT INTO transactions (date, amount, tag, desc) VALUES (?, ?, ?, ?)", transactions_data)

# Recupero tutte le righe per stampare
c.execute("SELECT * FROM transactions")
rows = c.fetchall()

# Stampa delle righe
for row in rows:
    print(row)

conn.commit()
conn.close()
