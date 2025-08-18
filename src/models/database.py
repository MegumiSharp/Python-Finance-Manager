import datetime
import sqlite3

from config.settings import DATABASE_PATH

# Convert a date string from 'YYYY-MM-DD' format to 'DD/MM/YYYY' format.
def norm_today():
    date = str(datetime.date.today())
    return f'{date[8:10]}/{date[5:7]}/{date[:4]}'


class DatabaseManager:
    def __init__(self):
        # Connessione al Database
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()
        self.local_db = []                                      # Altering the db is expensive, better to pass it on a list and save it on the database every now and than
  
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS transactions (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT,
                Amount FLOAT,
                Tag TEXT,
                Description TEXT
            )'''
        )
        self.conn.commit()
        
        self.update_local()                      # At the start of the bject, the databse is copied in a list of list


    def print_db(self):
        self.cursor.execute("SELECT * FROM transactions")

        # Fetch all rows
        rows = self.cursor.fetchall()

        # Optionally get column names
        column_names = [description[0] for description in self.cursor.description]
        print(" | ".join(column_names))
        print("-" * 40)

        # Print each row
        for row in rows:
            print(" | ".join(str(cell) for cell in row))

    # Update the list with all database entries
    def update_local(self):
        self.local_db = []
        self.cursor.execute('''SELECT * FROM transactions''')
        for t in self.cursor.fetchall():
            self.local_db.append([t[0], t[1], t[2], t[3], t[4]])
    
    def add_transaction(self, date = None, amount = None, tag = None, description = None):
        if date is None:
            date = norm_today()  # default dinamico per la data

        if amount is None:
            amount = 0
    
        if tag is None:
            tag = "None"
            
        if description is None:
            description = ""

        self.cursor.execute("INSERT INTO transactions (Date, Amount, Tag, Description) VALUES (?,?,?,?)",(date, amount, tag, description))
        self.conn.commit()
        self.update_local()

    def edit_transaction(self, idx, date=None, amount=None, tag=None, description=None):
        if date is None:
            date = norm_today()  # default dinamico per la data
        if amount is None:
            amount = 0
        if tag is None:
            tag = "None"
        if description is None:
            description = ""

        # Sintassi corretta per UPDATE
        self.cursor.execute(
            "UPDATE transactions SET Date = ?, Amount = ?, Tag = ?, Description = ? WHERE ID = ?",
            (date, amount, tag, description, idx)
        )
        self.conn.commit()
        self.update_local()

    def remove_transaction(self, id : int):
        self.cursor.execute("DELETE FROM transactions WHERE ID = ?",(id,))

        self.conn.commit()
        self.update_local()
        
    
    def print_trans(self):
        print(self.local_db)


